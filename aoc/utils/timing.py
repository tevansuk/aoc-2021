from time import perf_counter


class catchtime:
    t: float
    thing: str

    def __init__(self, thing="Time taken: "):
        self.thing = thing

    def __enter__(self):
        self.t = perf_counter()
        return self

    def __exit__(self, type, value, traceback):
        self.t = perf_counter() - self.t

    def __str__(self) -> str:
        return f"{self.thing} {self.t:.4f}s"
