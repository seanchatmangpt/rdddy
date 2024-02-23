import ast
import inspect
import dspy
from typing import Type, TypeVar, Optional

from pydantic import BaseModel

from experiments.low_api.requirement_model import (
    Requirement,
    FunctionalRequirementsSpec,
)
from rdddy.generators.gen_pydantic_instance import GenPydanticInstance

T = TypeVar("T", bound=BaseModel)


class GeneratePydanticInstance(dspy.Module):
    def __init__(self):
        super().__init__()

    def forward(
        self,
        prompt,
        root_model: type[T],
        child_models: Optional[list[type[BaseModel]]] = None,
    ):
        models = [root_model]  # Always include root_model in models list

        if child_models:
            models.extend(child_models)

        model_sources = "\n".join([inspect.getsource(model) for model in models])

        # Validate and create an instance of the Pydantic class
        output_key = f"kwargs_dict_for_{root_model.__name__}"
        classify = dspy.Predict(
            f"root_model_name, models_source, prompt -> {output_key}"
        )
        response = classify(
            root_model_name=root_model.__name__,
            models_source=model_sources,
            prompt=prompt,
        )
        res_str = response[output_key]
        res_dict = ast.literal_eval(res_str)
        return root_model.model_validate(res_dict)


input_prompt = """
      - raw: >
          The TCS will provide the hardware and software necessary to allow
          the operator to conduct the following major functions 1) mission
          planning, 2) mission control and monitoring, 3) payload product
          management, 4) targeting, and 5) C4I system interface.
      - raw: >
          The TCS shall have the functionality to allow the operator to
          generate a UAV mission plan.
      - raw: >
          The TCS shall have the functionality to receive and process UAV
          mission plans from service specific mission planning systems.
      - raw: >
          The TCS Mission plan shall include all necessary information
          required to be interoperable with the service specific mission
          planning systems including the Tactical Aircraft Mission Planning
          System(TAMPS), Aviation Mission Planning System (AMPS), and Air
          Force Mission Support System (AFMSS)."""


def main():
    lm = dspy.OpenAI(max_tokens=2000)
    dspy.settings.configure(lm=lm)

    # Assume `generate_instance` is an instance of `GeneratePydanticInstance`
    instance = GeneratePydanticInstance()(root_model=FunctionalRequirementsSpec, child_models=[Requirement], prompt=input_prompt)

    # Print the instance
    print(f"Generated Pydantic Instance: {type(instance)}\n{repr(instance)}")


if __name__ == "__main__":
    main()
