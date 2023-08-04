from pydantic import BaseModel


class Boxer(BaseModel):
    name: str

    def __str__(self) -> str:
        return self.name
