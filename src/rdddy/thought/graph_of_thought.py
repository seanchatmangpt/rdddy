from typing import Optional

import dspy
from pydantic import BaseModel, Field

from dspy import Module
# from experiments.web.mer import create_mermaid
from rdddy.generators.gen_pydantic_instance import GenPydanticInstance


class GraphNode(BaseModel):
    id: str = Field(..., description="Unique identifier for the node")
    content: str = Field(
        ..., description="Content or question associated with the node"
    )
    answer: Optional[str] = Field(
        None, description="Answer or result of the node's reasoning step"
    )


class GraphEdge(BaseModel):
    source_id: str = Field(..., description="Source node ID")
    target_id: str = Field(..., description="Target node ID")
    relationship: str = Field(
        ..., description="Description of the relationship or reasoning link"
    )


class GraphOfThoughtModel(BaseModel):
    nodes: list[GraphNode] = Field(..., description="List of nodes in the graph")
    edges: list[GraphEdge] = Field(..., description="List of edges linking the nodes")


class GraphOfThought(Module):
    def __init__(self):
        super().__init__()

    def forward(self, prompt) -> GraphOfThoughtModel:
        return GenPydanticInstance(
            root_model=GraphOfThoughtModel, child_models=[GraphNode, GraphEdge]
        ).forward(prompt)


def main():
    lm = dspy.OpenAI(max_tokens=1000)
    dspy.settings.configure(lm=lm)

    # prompt = (
    #     "Decision Model Notation for cancer diagnosis in a 5 step circle with branches"
    # )

    prompt = "BPMN for ordering a sandwich"
    # prompt = "Explain the water cycle step by step."

    result_graph = GraphOfThought().forward(prompt)
    print(result_graph)


if __name__ == "__main__":
    main()


# import asyncio


# async def main():
#     prompt = (
#         "Imagine the interactible elements of the Linkedin homepage"
#     )
#
#     result = await create_mermaid(prompt)
#
#     print(result)


# if __name__ == "__main__":
#     asyncio.run(main())
