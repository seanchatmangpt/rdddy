import inspect

import dspy
from rdddy.generators.gen_pydantic_instance import GenPydanticInstance

lm = dspy.OpenAI(max_tokens=500)
dspy.settings.configure(lm=lm)


import json
from typing import Any, Optional

from pydantic import BaseModel, Field

from rdddy.generators.gen_python_primitive import GenStr

cli_description = """

Service: Get Current Weather
Action: Retrieve
Path: /weather/current
Description: Fetches the latest weather information.
Parameters: { "location": "Specify a location as text" }
Output: Provides a JSON-based weather report with all the details.

"""


class APIEndpoint(BaseModel):
    method: str = Field(..., description="HTTP method of the API endpoint")
    url: str = Field(..., description="URL of the API endpoint")
    description: str = Field(..., description="Description of what the API endpoint does")
    response: str = Field(..., description="Response from the API endpoint")
    query_params: Optional[dict[str, Any]] = Field(None, description="Query parameters")


def main():
    generate_answer = dspy.ChainOfThought("model, prompt -> model_dict")

    # result = generate_answer(model=inspect.getsource(APIEndpoint), prompt=cli_description)

    # print(result.model_dict)

    # cli_data = APIEndpoint.model_validate_json(result.model_dict)

    generate_answer = dspy.ChainOfThought(f"model, prompt -> {APIEndpoint.__name__.lower()}_dict")

    result = generate_answer(model=inspect.getsource(APIEndpoint), prompt=cli_description)

    print(result.get(f"{APIEndpoint.__name__.lower()}_dict"))

    cli_data = APIEndpoint.model_validate_json(result.get(f"{APIEndpoint.__name__.lower()}_dict"))

    endpoint_name = GenStr()(cli_description + "\nEndpoint URL")

    # endpoint_names = GenList()(cli_description + "\nEndpoint Names?")

    dot = GenPydanticInstance(root_model=APIEndpoint, child_models=[APIEndpoint])

    api_dict = dot.forward(cli_description)

    print(json.dumps(api_dict, indent=2))

    cli_data = APIEndpoint(**api_dict)

    print(cli_data)


if __name__ == "__main__":
    main()
