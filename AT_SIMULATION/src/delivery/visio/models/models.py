from pydantic import BaseModel


class Node(BaseModel):
    id: int
    pos_x: int
    pos_y: int
    height: int
    width: int
    color: str


class Edge(BaseModel):
    id: int
    from_node: int
    to_node: int
