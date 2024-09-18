from pydantic import BaseModel


class Node(BaseModel):
    id: int
    name: str
    type: str
    pos_x: int
    pos_y: int
    width: int
    height: int
    color: str


class Edge(BaseModel):
    id: int
    from_node: Node
    to_node: Node


class MoveNodeRequest(BaseModel):
    delta_x: int
    delta_y: int


class UpdateNodeResponse(BaseModel):
    id: int
    name: str
    type: str
    pos_x: int
    pos_y: int
    width: int
    height: int
    color: str