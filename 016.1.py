def multipliers(digit):
    seed = [0, 1, 0, -1]
    index = 0
    first = True
    while 1:
        for c in range(digit):
            if first:
                first = False
                continue
            yield seed[index]
        index = (index + 1) % 4


def fft(number: list):
    return [
        abs(sum(n * m for n, m in zip(number, multipliers(i + 1)))) % 10
        for i in range(len(number))
    ]


def split_input(inp: str):
    return [int(i) for i in inp]


def seq_as_str(inp: list):
    return "".join(str(i) for i in inp)


def test():
    p = split_input("12345678")
    for _ in range(4):
        p = fft(p)
        print(seq_as_str(p))


def test2():
    p = split_input("80871224585914546619083218645595")
    for _ in range(100):
        p = fft(p)
    print(seq_as_str(p)[:8])


def main():
    with open("016.1.input.txt", "r") as f:
        p = split_input(f.read().strip())
        for _ in range(100):
            p = fft(p)
        print(seq_as_str(p)[:8])


main()
