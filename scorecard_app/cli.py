from time import sleep

import click
from models import Round, ScorecardCli
from models.boxer import Boxer


def fight_sequence(scorecard: ScorecardCli):
    click.clear()
    click.echo("LET'S GET READY TO RUMBLE!!!")
    click.echo("\n" * 2)
    sleep(1)
    click.pause("Press any key to continue...")
    click.clear()
    curr_round = 1
    while curr_round <= len(scorecard.scores):
        click.echo(f"Round {curr_round}")
        click.echo("\n")
        sleep(1)
        click.echo(scorecard.show_scorecard())
        click.echo("\n")
        click.secho(message='** Enter "11" if boxer has earned a stoppage **\n', fg="yellow")
        sleep(1)
        round_scores = []
        for boxer in [scorecard.b1, scorecard.b2]:
            score = click.prompt(f"Score for {boxer}", type=click.IntRange(0, 11), err=True)
            click.echo("\n")
            if score == 11:
                click.echo(f"{boxer} has earned a stoppage.")
                sleep(1)
                click.clear()
                click.echo("The fight is over.")
                sleep(1)
                click.echo("\n")
                click.echo(f"{boxer} wins by KO/TKO in round {curr_round}.")
                click.echo("\n")
                click.echo(scorecard.stoppage_ending())
                click.echo("\n")
                click.echo(scorecard.show_scorecard())
                sleep(1)
                click.echo("\n")
                click.pause()
                click.clear()
                return
            round_scores.append(score)
        click.secho(
            message=f"Round {curr_round}: {scorecard.b1} ({round_scores[0]}) - "
            f"{scorecard.b2} ({round_scores[1]})",
            fg="red",
        )

        if click.confirm("Is this correct?"):
            result = Round(round=curr_round, b1_score=round_scores[0], b2_score=round_scores[1])
            scorecard.complete_round(result)
            curr_round += 1
            sleep(1)
            click.clear()
        else:
            click.clear()
    else:
        click.echo("Fight has concluded.")
        sleep(2)
        click.echo("\n")
        click.echo(scorecard.show_scorecard())
        click.echo("\n" * 2)
        winner, msg = scorecard.determine_winner()
        if winner != "N/A":
            click.echo(msg)
        else:
            click.echo("We've got a tie.")
        click.echo("\n" * 2)
        click.pause()
        click.clear()


def get_boxer_info() -> ScorecardCli:
    b1 = Boxer(name=click.prompt("Who is fighting?", type=str, default="Evander Holyfield").strip())
    b2 = Boxer(name=click.prompt(b1.name + " vs ?", type=str, default="Mike Tyson").strip())
    rounds = click.prompt("How many rounds?", type=int, default=12)
    click.echo("\n")
    sleep(1)
    return ScorecardCli(b1=b1, b2=b2, rounds=rounds)


@click.command()
def cli():
    click.clear()
    click.secho("Boxing Scorecard CLI", bg="green", fg="black")
    sleep(1)
    click.echo("\n")
    click.secho("A simple CLI to score boxing matches in real time.", italic=True)
    click.echo("\n")
    sleep(1)
    scorecard = get_boxer_info()
    click.clear()
    sleep(1)
    fight_sequence(scorecard)


if __name__ == "__main__":
    cli()
