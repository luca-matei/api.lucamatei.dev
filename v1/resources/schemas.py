from uuid import UUID

from pydantic import BaseModel, computed_field


class ResourceTreeResponse(BaseModel):
    id: UUID
    title: str
    parent_id: UUID | None
    child_count: int
    slug: str
    list_order: int

    @computed_field
    @property
    def href(self) -> str:
        return f"/resources/{self.id}/{self.slug}"

    class Config:
        from_attributes = True


class ResourceResponse(BaseModel):
    id: UUID
    title: str
    parent_id: UUID | None
    child_count: int
    slug: str
    list_order: int
    author_id: UUID
    content: str

    @computed_field
    @property
    def href(self) -> str:
        return f"/resources/{self.id}/{self.slug}"

    class Config:
        from_attributes = True
