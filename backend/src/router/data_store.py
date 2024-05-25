from sqlalchemy.orm import Session
from sqlalchemy import text

from ..models import Node, NodeRelationship



def build_tree(data, parent_node=None):
    tree = []
    for node in data:
        if node['parent_id'] == parent_node:
            children = build_tree(data, node['node_id'])
            if children:
                node['children'] = children
            tree.append(node)
    return tree


def get_tree(user_id, db: Session):
    query = """
    WITH RECURSIVE tree AS (
        SELECT node_id, name, node_type, description, data, parent_id
        FROM data_store.nodes
        LEFT JOIN data_store.node_relationships ON node_id = child_id
        WHERE user_id = :user_id AND parent_id IS NULL
        UNION ALL
        SELECT n.node_id, n.name, n.node_type, n.description, n.data, r.parent_id
        FROM data_store.nodes n 
        JOIN data_store.node_relationships r ON n.node_id = r.child_id
        JOIN tree t ON t.node_id = r.parent_id
    )
    SELECT * FROM tree;
    """

    # 执行 SQL 语句并获取结果
    result = db.execute(text(query), {"user_id": user_id})

    # 将结果转换为字典列表
    data = []
    for row in result:
        data.append({
            'node_id': row[0],
            'name': row[1],
            'node_type': row[2],
            'description': row[3],
            'data': row[4],
            'parent_id': row[5]
        })

    # 构建树
    tree = build_tree(data)
    return tree
