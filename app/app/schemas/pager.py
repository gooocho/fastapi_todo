from typing import Optional

from pydantic import BaseModel, Field


class Pager(BaseModel):
    page: Optional[int] = Field(1, ge=1)
    per_page: Optional[int] = Field(100, ge=1, le=500)

    def offset(self):
        return (self.page - 1) * self.per_page
