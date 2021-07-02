from app.schemas.pager import Pager


def test_pager_offset() -> None:
    pager1 = Pager(page=3, per_page=7)
    assert pager1.offset() == 14
