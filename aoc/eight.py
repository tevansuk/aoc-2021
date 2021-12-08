from pathlib import Path

Reading = frozenset
Readings = list[Reading]
Data = list[tuple[Readings, Readings]]
SIZE_TO_NUM = {2: 1, 3: 7, 4: 4, 7: 8}


class SignalMap(dict[int, Reading]):
    @classmethod
    def from_observations(cls, observations: Readings) -> "SignalMap":
        sigmap = cls()
        two_three_five = Readings()
        nought_six_nine = Readings()
        # Get the values for 1, 4, 7, 8 and potentials for others
        for elem in observations:
            # I'd like to use match / case here, but mypy needs time to catch up!
            elem_size = len(elem)
            if elem_size == 5:
                two_three_five.append(elem)
            elif elem_size == 6:
                nought_six_nine.append(elem)
            else:
                sigmap[SIZE_TO_NUM[elem_size]] = elem
        sigmap._determine_235(two_three_five)
        sigmap._determine_069(nought_six_nine)
        return sigmap

    def _determine_235(self, observations: Readings) -> None:
        for elem in observations:
            if len(elem - self[7]) == 2:
                self[3] = elem
            elif len(elem - (self[4] - self[1])) == 3:
                self[5] = elem
            else:
                self[2] = elem

    def _determine_069(self, observations: Readings) -> None:
        for elem in observations:
            if len(elem - self[1]) == 5:
                self[6] = elem
            elif len(elem - self[4]) == 2:
                self[9] = elem
            else:
                self[0] = elem


def main(datafile: Path) -> None:
    data = parse_data(datafile)
    print(f"Q1: {count_simple_outputs(data)=}")
    print(f"Q2: {sum_output_readings(data)=}")


def count_simple_outputs(data: Data) -> int:
    return sum(1 for _, output in data for val in output if len(val) in SIZE_TO_NUM)


def sum_output_readings(data: Data) -> int:
    return sum(calculate_output_reading(obs, output) for obs, output in data)


def calculate_output_reading(obs: Readings, output: Readings) -> int:
    # Reverse the map to make it easier to turn output in to numbers
    sigmap = {v: k for k, v in SignalMap.from_observations(obs).items()}
    return sum(sigmap[el] * 10 ** (len(output) - idx - 1) for idx, el in enumerate(output))


def parse_data(datafile: Path) -> Data:
    data = Data()
    with datafile.open() as fp:
        for line in fp.readlines():
            all_vals = [Reading(word) for part in line.split("|") for word in part.split()]
            data.append((all_vals[0:10], all_vals[-4:]))
    return data
