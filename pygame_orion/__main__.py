from __future__ import annotations
import typer


cli = typer.Typer()


def intro():
    typer.echo("Welcome to Orion.")


if __name__ == '__main__':
    typer.run(intro)
