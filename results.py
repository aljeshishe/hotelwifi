import copy
import json
from pathlib import Path
import tqdm


class Results:
    def __init__(self, params):
        self.params = copy.deepcopy(params)
        self.totals = None
        self.pbar = tqdm.tqdm()

    def on_start(self, totals: int) -> None:
        self.pbar.total = totals

    def on_result(self, result) -> None:
        password, elapsed = result
        self.pbar.update()
        self.pbar.set_description(f"{password=} {elapsed=:.1f}s")
        file = Path("resume")
        self.params.start = password
        file.write_text(json.dumps(self.params))
