from notion_client import Client, AsyncClient

from v1.config import settings

notion = Client(auth=settings.NOTION_API_KEY)
async_notion = AsyncClient(auth=settings.NOTION_API_KEY)


def parse_notion_to_markdown(notion_json):
    markdown_lines = []

    def parse_rich_text(rich_text):
        text = ""
        for item in rich_text:
            content = item["text"]["content"]
            annotations = item["annotations"]
            if annotations["bold"]:
                content = f"**{content}**"
            if annotations["italic"]:
                content = f"*{content}*"
            if annotations["strikethrough"]:
                content = f"~~{content}~~"
            if annotations["underline"]:
                content = f"<u>{content}</u>"
            if annotations["code"]:
                content = f"`{content}`"
            text += content
        return text

    def parse_block(block):
        block_type = block["type"]
        if block_type == "heading_2":
            text = parse_rich_text(block["heading_2"]["rich_text"])
            markdown_lines.append(f"## {text}\n")
        elif block_type == "numbered_list_item":
            text = parse_rich_text(block["numbered_list_item"]["rich_text"])
            markdown_lines.append(f"1. {text}\n")
        elif block_type == "paragraph":
            text = parse_rich_text(block["paragraph"]["rich_text"])
            if text:
                markdown_lines.append(f"{text}\n")
        elif block_type == "code":
            code_content = parse_rich_text(block["code"]["rich_text"])
            language = block["code"]["language"]
            markdown_lines.append(f"```{language}\n{code_content}\n```\n")

    for block in notion_json["results"]:
        parse_block(block)

    return "\n".join(markdown_lines)
