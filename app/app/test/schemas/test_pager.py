from app.schemas.pager import Pager

class TestPager:
    def test_pager_offset(self) -> None:
        pager = Pager(page=3, per_page=7)
        assert pager.offset() == 14
