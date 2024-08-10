import logging
import orjson

from uuid import UUID

from v1.workers.worker import dramatiq
from v1.clients.notion import notion, parse_notion_to_markdown
from v1.clients.redis import RedisSession
from v1.clients.postgres import PostgresSession
from v1.config import settings
from v1.resources.schemas import ResourceTreeResponse
from v1.resources.models import Resource


def sanitize_slug(slug: str):
    return slug.lower().replace(" ", "-").replace(".", "-").replace("/", "-").strip("-")


@dramatiq.actor(queue_name="resources", max_retries=0)
def refresh_pages():
    child_pages = []

    def fetch_child_pages(page_id: UUID, parent_id: UUID = None):
        logging.info(f"Fetching page {page_id}")
        if parent_id == settings.NOTION_ROOT_PAGE_ID:
            parent_id = None
        # Fetch the page itself
        page = notion.pages.retrieve(page_id)
        title = (
            page["properties"]["title"]["title"][0]["plain_text"]
            if "title" in page["properties"]
            else "Untitled"
        )
        response = notion.blocks.children.list(page_id)
        child_count = sum(
            1 for block in response.get("results", []) if block["type"] == "child_page"
        )
        slug = sanitize_slug(title)
        child = ResourceTreeResponse(
            **{
                "id": page["id"],
                "title": title,
                "parent_id": parent_id,
                "child_count": child_count,
                "slug": slug,
                "list_order": 0,
            }
        ).model_dump()

        if page["id"] != settings.NOTION_ROOT_PAGE_ID:
            child_pages.append(child)

        upsert_page.send(child)

        # Fetch the children of the page
        for block in response.get("results", []):
            if block["type"] == "child_page":
                child_id = block["id"]
                fetch_child_pages(child_id, page_id)  # Recursively fetch sub-pages

    with PostgresSession() as session:
        session.query(Resource).delete()

    fetch_child_pages(settings.NOTION_ROOT_PAGE_ID)

    with RedisSession() as redis:
        redis.delete("lmdev:page_tree")
        redis.sadd("lmdev:page_tree", *[orjson.dumps(c) for c in child_pages])


@dramatiq.actor(queue_name="resources", max_retries=0)
def upsert_page(page_props: dict):
    page_id = page_props["id"]
    logging.info(f"Upserting page {page_id}")

    blocks = notion.blocks.children.list(page_id)
    markdown = parse_notion_to_markdown(blocks)

    # Use session.merge()
    with PostgresSession() as session:
        resource = Resource(
            id=page_id,
            title=page_props["title"],
            parent_id=page_props["parent_id"],
            child_count=page_props["child_count"],
            slug=page_props["slug"],
            author_id=settings.DEFAULT_AUTHOR_ID,
            content=markdown,
            list_order=page_props["list_order"],
        )
        session.merge(resource)
