from typing import List

import click
import pandas as pd
from models import Boxer, Round
from pydantic import BaseModel, field_validator, model_validator
from tabulate import tabulate


class ScorecardBase(BaseModel):
    b1: Boxer
    b2: Boxer
    rounds: int
    scores: List[Round] = []

    @model_validator(mode="after")
    def populate_scores(self):
        self.scores = []
        for i in range(self.rounds):
            self.scores.append(Round(round=i + 1))
        return self

    @field_validator("rounds")
    @classmethod
    def validate_fight_length(cls, v):
        if v not in list(range(3, 13)):
            return 12
        return v


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
                {self.b1.name: score.b1_score, self.b2.name: score.b2_score}, index=[score.round]
            )
            dfs.append(df)
        combined_df = pd.concat(dfs)
        combined_df.loc["Total"] = combined_df.sum()
        return combined_df

    def show_scorecard(self):
        df = self.get_df()
        result = tabulate(
            df.reset_index().values.tolist(),
            headers=["Round", self.b1.name, self.b2.name],
            tablefmt="pretty",
        )
        return result

    def determine_winner(self):
        winner = "N/A"
        result_msg = "And we go to the cards...The winner is "
        df = self.get_df()
        b1, b2 = self.b1, self.b2
        if df[b1.name]["Total"] > df[b2.name]["Total"]:
            winner = b1.name
        if df[b1.name]["Total"] < df[b2.name]["Total"]:
            winner = b2.name
        result_msg += winner + "."
        return winner, result_msg
