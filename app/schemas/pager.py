from typing import Optional

from pydantic import BaseModel

class Pager(BaseModel):
    page: Optional[int] = 1
    per_page: Optional[int] = 100

    def offset(self):
        return (self.page - 1) * self.per_page
