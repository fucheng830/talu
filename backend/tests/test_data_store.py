from app.api.data_store import get_tree
from app.database import SessionLocal


def test_get_tree():
    # 测试用例
    with SessionLocal() as db:
        user_id = "598a7fd4-6bff-4f07-918a-f07e452ab050"
        tree = get_tree(user_id, db)
        print(tree)