from typing import Optional

from pydantic import BaseModel, Field

DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 100

class Pager(BaseModel):

    page: Optional[int] = Field(DEFAULT_PAGE, ge=1)
    per_page: Optional[int] = Field(DEFAULT_PER_PAGE, ge=1, le=500)

    def offset(self):
        page = self.page if self.page is not None else DEFAULT_PAGE
        per_page = self.per_page if self.per_page is not None else DEFAULT_PER_PAGE
        return (page - 1) * per_page
