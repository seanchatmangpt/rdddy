from pydantic import BaseModel, validator


class FastAPIRouteModel(BaseModel):
    path_param: str
    query_param: int
    request_body: str

    @validator("path_param")
    def validate_path_param(cls, v):
        # validation logic
        return v

    @validator("query_param")
    def validate_query_param(cls, v):
        # validation logic
        return v

    @validator("request_body")
    def validate_request_body(cls, v):
        # validation logic
        return v
