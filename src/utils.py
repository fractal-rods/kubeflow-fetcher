from argparse import ArgumentParser
from dataclasses import dataclass
from src.version import VERSION


@dataclass
class ProgramArgs:
    action: str


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="Create, delete or check status of the fetcher pipeline."
    )
    parser.add_argument("-v", "--version", version=VERSION, action="version")
    parser.add_argument(
        "action",
        choices=["create", "delete", "status"],
        type=str,
    )
    return parser


def parse_args() -> ProgramArgs:
    parser = create_parser()
    return ProgramArgs(**vars(parser.parse_args()))
