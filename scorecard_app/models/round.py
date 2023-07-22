from typing import Optional

from pydantic import BaseModel, validator


class Round(BaseModel):
    round: int = 0
    b1_score: int = 0
    b2_score: int = 0
    note: Optional[str] = ""

    @validator("b1_score", "b2_score")
    def validate_scoring(cls, v):
        if v not in list(range(0, 11)):
            raise ValueError("Invalid Score: Score must be an integer 1-10")
        return v

    @validator("round")
    def validate_round_number(cls, v):
        if v not in list(range(1, 13)):
            raise ValueError("Invalid Round: Round must be integer 1-12")
        return v
