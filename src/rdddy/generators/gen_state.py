from pydantic import BaseModel, Field

import dspy
from rdddy.generators.gen_pydantic_instance import GenPydanticInstance


class State(BaseModel):
    name: str = Field(..., description="The name of the state")
    abbreviation: str = Field(..., description="The two-letter postal abbreviation for the state")
    capital: str = Field(..., description="The capital city of the state")


class USA(BaseModel):
    states: list[State]


def main():
    lm = dspy.OpenAI(max_tokens=3000)
    dspy.settings.configure(lm=lm)

    model_module = GenPydanticInstance(root_model=USA, child_models=[State])
    model_inst = model_module(prompt="All of the states")
    print(model_inst)


if __name__ == "__main__":
    main()
