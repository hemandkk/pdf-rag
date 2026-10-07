from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.chat import MessageResponse


class ConversationCreate(BaseModel):
    title: str = Field(
        default="New conversation",
        min_length=1,
        max_length=200,
    )


class ConversationResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: str
    knowledge_base_id: str
    title: str
    created_at: datetime
    updated_at: datetime


class ConversationDetailResponse(BaseModel):
    id: str
    knowledge_base_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: list[MessageResponse]