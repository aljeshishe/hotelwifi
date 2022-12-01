import json
import logging
from pathlib import Path
from typing import Any

import click as click

import munch
import logging_config
from processor import Processor
from results import Results

log = logging.getLogger(__name__)


@click.command()
@click.option("-m", "--mac_address", help="Mac address.")
@click.option("-w", "--workers", help="Workers", default=3)
@click.option("-s", "--start", help="Password start", default="000000")
@click.option("-e", "--end", help="Password end", default="999999")
@click.option("-a", "--alphabet", help="Alphabet", default="0123456789")
@click.option('-v', '--verbose', count=True)
def main(**kwargs) -> None:

    params = munch.munchify(resume_or_new_params(**kwargs))
    level = logging.WARNING
    if params.verbose == 1:
        level = logging.INFO
    elif params.verbose > 1:
        level = logging.DEBUG
    config = logging_config.default_config(console_level=level)
    logging_config.configure(config=config)

    results = Results(params=params)
    processor = Processor(params=params, results=results)
    processor.process()


def resume_or_new_params(**new_params: Any) -> dict[str, Any]:
    file = Path("resume")
    if not file.exists():
        return new_params

    content = file.read_text()
    params = json.loads(content)
    if file.exists():
        answer = input(f"There is unfinished session with following params:\n{content}.\n"
                       f"c: continue unfinished session\n"
                       f"s: start new session\n"
                       f"d: delete unfinished session and start new\n"
                       f"x: exit\n")
        answer = answer.lower()
        if answer == "x":
            exit(0)
        if answer == "c":
            return params
        if answer == "d":
            file.unlink()
        if answer in ("d", "s"):
            return new_params


if __name__ == "__main__":
    main()
