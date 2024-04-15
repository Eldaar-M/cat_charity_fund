from sqlalchemy import Column, String, Text

from app.constants import MAX_LENGTH_NAME_PROJECT
from app.models.base import BaseModel


class CharityProject(BaseModel):
    name = Column(
        String(MAX_LENGTH_NAME_PROJECT),
        unique=True,
        nullable=False
    )
    description = Column(Text, nullable=False)
