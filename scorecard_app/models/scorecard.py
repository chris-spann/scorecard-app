from typing import List

import click
import pandas as pd
from models.round import Round
from pydantic import BaseModel, validator
from tabulate import tabulate


class ScorecardBase(BaseModel):
    b1: str
    b2: str
    rounds: int
    scores: List[Round] = []

    @validator("rounds")
    def validate_fight_length(cls, v):
        if v not in list(range(3, 13)):
            return 12
        return v

    @validator("scores", always=True)
    def populate_scores(cls, v, values):
        res = []
        for i in range(values["rounds"]):
            res.append(Round(round=i + 1))
        return res


class ScorecardCli(ScorecardBase):
    def reset_card(self):
        res = []
        for i in range(self.rounds):
            res.append(Round(round=i + 1))
        self.scores = res
        self.show_scorecard()

    def reset_round(self, round: int):
        is_reset_complete = False
        for i, score in enumerate(self.scores):
            if score.round == round:
                self.scores[i] = Round(round=round, b1_score=0, b2_score=0)
                is_reset_complete = True
        if not is_reset_complete:
            click.echo("Error: Did not reset round")
        self.show_scorecard()

    def complete_round(self, result: Round):
        i = result.round - 1
        for i, score in enumerate(self.scores):
            if score.round == result.round:
                self.scores[i] = result

    def get_df(self) -> pd.DataFrame:
        dfs = []
        for score in self.scores:
            df = pd.DataFrame(
                {self.b1: score.b1_score, self.b2: score.b2_score}, index=[score.round]
            )
            dfs.append(df)
        combined_df = pd.concat(dfs)
        combined_df.loc["Total"] = combined_df.sum()
        return combined_df

    def show_scorecard(self):
        df = self.get_df()
        result = tabulate(
            df.reset_index().values.tolist(),
            headers=["Round", self.b1, self.b2],
            tablefmt="pretty",
        )
        return result

    def determine_winner(self):
        winner = "N/A"
        result_msg = "And we go to the cards...The winner is "
        df = self.get_df()
        b1, b2 = self.b1, self.b2
        if df[b1]["Total"] > df[b2]["Total"]:
            winner = b1
        if df[b1]["Total"] < df[b2]["Total"]:
            winner = b2
        result_msg += winner + "."
        return winner, result_msg
