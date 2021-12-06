class State:
    depth = 0
    aim = 0
    horiz = 0

    def __call__(self, verb, count):
        if verb == "forward":
            self.horiz += count
            self.depth += self.aim * count
        elif verb == "up":
            self.aim -= count
        elif verb == "down":
            self.aim += count
        else:
            raise ValueError(f"Unknown action: {verb}")


def main(data):
    state = State()
    with data.open() as fp:
        for line in fp.readlines():
            verb, count = line.split()
            state(verb, int(count))
    print(f"Depth: {state.aim}\tHorizontal: {state.horiz}")
    print(f"Q1: {state.aim * state.horiz}")
    print(f"Depth: {state.depth}\tHorizontal: {state.horiz}\tAim: {state.aim}")
    print(f"Q2: {state.depth * state.horiz}")
