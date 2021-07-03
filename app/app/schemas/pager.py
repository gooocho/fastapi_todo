from typing import Optional

from pydantic import BaseModel, Field


class Pager(BaseModel):
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 100

    page: Optional[int] = Field(DEFAULT_PAGE, ge=1)
    per_page: Optional[int] = Field(DEFAULT_PER_PAGE, ge=1, le=500)

    def offset(self):
        return (self.page - 1) * self.per_page
