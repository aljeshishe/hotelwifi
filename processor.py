import logging
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from typing import Callable

import tqdm

from results import Results
from passwords import Passwords
from session import Session

log = logging.getLogger(__name__)


class Processor:
    RETRIES = 3

    def __init__(self, params, results: Results) -> None:
        self.results = results
        self.params = params
        self.sessions = Queue()
        for i in range(self.params.workers):
            self.sessions.put(Session(mac_address=params.mac_address))

    def _run(self, password: str) -> (str, int):
        start = time.time()
        exception = None
        for i in range(self.RETRIES):
            session = self.sessions.get(block=False, timeout=1)
            try:
                session.login(password=password)
                break
            except Exception as ex:
                exception = ex
                continue
            finally:
                self.sessions.put(session)
        if exception is not None:
            log.error(f"While processing {password=} got exception: {exception}")

        return password, time.time() - start

    def _results_consumer(self, futures):
        for result in self._as_results(futures):
            try:
                self.results.on_result(result)
            except Exception as ex:
                traceback.print_exc()

    def process(self) -> None:
        with ThreadPoolExecutor(max_workers=self.params.workers) as pool:
            passwords = Passwords(start=self.params.start, end=self.params.end, alphabet=self.params.alphabet)
            futures = []

            self.results.on_start(totals=passwords.total)
            pool.submit(self._results_consumer, futures=futures)

            for password in passwords.generator():
                futures.append(pool.submit(self._run, password=password))

    def _as_results(self, futures):
        for fut in futures:
            yield fut.result()
