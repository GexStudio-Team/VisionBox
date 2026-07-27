from pydantic import BaseModel

class SystemResponse(BaseModel):
    project: str
    version: str
    status: str