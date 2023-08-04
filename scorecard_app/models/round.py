from typing import Optional

from pydantic import BaseModel, field_validator


class Round(BaseModel):
    round: int = 0
    b1_score: int = 0
    b2_score: int = 0
    note: Optional[str] = ""

    def __str__(self):
        return (self.b1_score, self.b2_score)

    @field_validator("b1_score", "b2_score")
    @classmethod
    def validate_scoring(cls, v):
        if v not in list(range(0, 11)):
            raise ValueError("Invalid Score: Score must be an integer 1-10")
        return v

    @field_validator("round")
    @classmethod
    def validate_round_number(cls, v):
        if v not in list(range(1, 13)):
            raise ValueError("Invalid Round: Round must be integer 1-12")
        return v
