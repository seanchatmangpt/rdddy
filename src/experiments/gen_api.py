import dspy

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from rdddy.generators.gen_pydantic_instance import GenPydanticInstance

api_description = """
Imagine a digital portal where users can inquire about meteorological conditions. 
This portal is accessible through a web interface that interacts with a backend service. 
The service is invoked by sending a request to a specific endpoint. 
This request is crafted using a standard protocol for web communication. 
The endpoint's location is a mystery, hidden within the path '/forecast/today'. 
Users pose their inquiries by specifying a geographical area of interest, 
though the exact format of this specification is left to the user's imagination. 
Upon successful request processing, the service responds with a structured 
summary of the weather, encapsulating details such as temperature, humidity, 
and wind speed. However, the structure of this response and the means of 
accessing the weather summary are not explicitly defined.
"""


class APIEndpoint(BaseModel):
    method: str = Field(..., description="HTTP method of the API endpoint")
    url: str = Field(..., description="URL of the API endpoint")
    description: str = Field(
        ..., description="Description of what the API endpoint does"
    )
    response: str = Field(..., description="Response from the API endpoint")
    query_params: Optional[Dict[str, Any]] = Field(None, description="Query parameters")


def main():
    lm = dspy.OpenAI(max_tokens=1000)
    dspy.settings.configure(lm=lm)

    gpm = GenPydanticInstance(root_model=APIEndpoint)
    result = gpm.forward(prompt=api_description)
    print(result)


if __name__ == "__main__":
    main()
