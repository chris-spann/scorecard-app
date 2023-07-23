from pydantic import BaseModel


class Boxer(BaseModel):
    name: str

    def __repr__(self) -> str:
        return self.name
