import dspy
import json
from typing import Dict, Any, Optional

import inspect
from dspy import Module, Assert

from pydantic import BaseModel, Field, ValidationError
from typing import List

from rdddy.generators.gen_module import GenModule
from rdddy.generators.gen_python_primitive import GenDict

def strip_text_before_first_open_brace(input_text):
    if "{" in input_text:
        return input_text[input_text.index("{"):]
    else:
        return input_text

class GenPydanticModel(GenModule):
    def __init__(self, root_model, models: list = None):
        if models is None:
            models = [root_model]
        elif root_model not in models:
            models.append(root_model)

        super().__init__(f"{root_model.__name__.lower()}_model_validate_json_dict", input_keys=["inspect_getsource", "prompt"])
        self.root_model = root_model
        self.models = models
        self.model_sources = '\n'.join([inspect.getsource(model) for model in self.models])

    def validate_root_model(self, output) -> bool:
        try:
            return isinstance(self.root_model.model_validate_json(output), self.root_model)
        except (ValidationError, TypeError) as error:
            return False

    def validate_output(self, output):
        output = strip_text_before_first_open_brace(str(output))

        Assert(
            self.validate_root_model(output),
            f"""You need to create a dict for {self.root_model.__name__}, 
            You will be penalized for not returning only a {self.root_model.__name__} dict for {self.output_key}""",
        )

        return self.root_model.model_validate_json(output)
    
    def forward(self, **kwargs):
        # spec = dspy.ChainOfThought("prompt, source -> instance")

        # result = spec.forward(prompt=f'{kwargs["prompt"]}\nalign the prompt with the source', source=self.model_sources).instance

        # return super().forward(inspect_getsource=self.model_sources, prompt=result)

        return super().forward(inspect_getsource=self.model_sources, prompt=kwargs["prompt"])

        # Create a detailed instruction for prompt refinement
        # refinement_instruction = (
        #     "Below are the Pydantic model definitions:\n{}\n\n"
        #     "Based on these models, restructure the following description to align with the models:\n{}\n"
        #     "Restructured Description:"
        # ).format(self.model_sources, kwargs["prompt"])
        #
        # # Use ChainOfThought for prompt refinement
        # refined_prompt_result = dspy.ChainOfThought("prompt -> refined_prompt")
        # refined_prompt = refined_prompt_result.forward(prompt=refinement_instruction).get("refined_prompt")
        #
        # # Proceed with the refined prompt
        # return super().forward(inspect_getsource=self.model_sources, prompt=refined_prompt)


api_description = """

Service: Get Current Weather
Action: Retrieve
Path: /weather/current
Description: Fetches the latest weather information.
Parameters: { "location": "Specify a location as text" }
Output: Provides a JSON-based weather report with all the details.

APIEndpoint.model_validate_json(your_output)
"""

class APIEndpoint(BaseModel):
    method: str = Field(..., description="HTTP method of the API endpoint")
    url: str = Field(..., description="URL of the API endpoint")
    description: str = Field(..., description="Description of what the API endpoint does")
    response: str = Field(..., description="Response from the API endpoint")
    query_params: Optional[Dict[str, Any]] = Field(None, description="Query parameters")


def main():
    dot = GenPydanticModel(root_model=APIEndpoint)
    result = dot.forward(prompt=api_description)
    print(result)


if __name__ == '__main__':
    main()
    