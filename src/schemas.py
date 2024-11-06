import uuid
from datetime import datetime

from pydantic import BaseModel


class Identifier(BaseModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
