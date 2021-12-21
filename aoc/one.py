def main(datafile):
    data = [int(line) for line in datafile.read_text().strip().split("\n")]
    incs = sum(data[i] > data[i - 1] for i in range(1, len(data)))
    print(f"Number of depth increases: {incs}")
    wincs = sum(sum(data[i : i + 3]) > sum(data[i - 1 : i + 2]) for i in range(1, len(data) - 2))
    print(f"Number of window depth increases: {wincs}")
