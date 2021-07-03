import pytest

from app.schemas.pager import Pager

class TestPager:
    @pytest.mark.parametrize("page, per_page, offset", [
        (1, 10, 0),
        (2, 10, 10),
        (3, 7, 14),
        (6, 20, 100),
        (13, 17, (13 - 1) * 17)
    ])
    def test_pager_offset(self, page, per_page, offset) -> None:
        pager = Pager(page=page, per_page=per_page)
        assert pager.offset() == offset
