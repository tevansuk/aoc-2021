from collections import Counter


def main(datafile):
    data = datafile.read_text().strip().split("\n")
    idata = [int(d, 2) for d in data]
    bits = len(data[0])

    gamma = mlcb(idata, bits=bits)
    epsilon = mlcb(idata, bits=bits, lcb=True)
    print(f"{gamma=} {epsilon=} {gamma * epsilon=}")
    ogen = find(idata, bits=bits)
    co_scrub = find(idata, bits=bits, lcb=True)
    print(f"{ogen=} {co_scrub=} {ogen * co_scrub=}")


def mlcb(data, lcb=False, bits=5, sig=None):
    sig = sig or bits
    bits_ = range(bits - 1, bits - sig - 1, -1)
    c = Counter(bit for entry in data for bit in bits_ if entry & 1 << bit)
    comp = "__lt__" if lcb else "__ge__"
    return sum(1 << bit for bit in bits_ if getattr(2 * c[bit], comp)(len(data)))


def find(data, lcb=False, bits=5):
    for bit in range(bits - 1, -1, -1):
        comp = mlcb(data, lcb=lcb, bits=bit + 1, sig=1)
        data = [elem for elem in data if elem & 1 << bit == comp]
        if len(data) == 1:
            return data[0]
