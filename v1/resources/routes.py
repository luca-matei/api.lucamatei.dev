import orjson

from uuid import UUID
from fastapi import APIRouter

from v1.clients.postgres import PostgresSession
from v1.clients.redis import RedisSession
from v1.resources.tasks import refresh_pages
from v1.resources.models import Resource
from v1.resources.schemas import ResourceTreeResponse, ResourceResponse

router = APIRouter(prefix="/resources")


@router.get("/tree")
async def get_page_tree():
    with RedisSession() as redis:
        page_tree = redis.smembers("lmdev:page_tree")
        return [ResourceTreeResponse(**orjson.loads(p)) for p in page_tree]


@router.get("/{resource_id}")
async def get_resource(resource_id: UUID):
    with PostgresSession() as session:
        resource = session.query(Resource).filter(Resource.id == resource_id).first()
        return ResourceResponse.model_validate(resource)


dev_router = APIRouter(prefix="/dev/resources")


@dev_router.get("/refresh")
async def refresh_page_tree():
    refresh_pages.send()
    return {"message": "Triggered page refresh"}
