# Given the small scope of the problem, I'm ok with
# a simple brute force solution


def is_valid(n):
    num = str(n)
    has_double = False
    d0 = num[0]
    for d in num[1:]:
        if d0 == d:
            has_double = True
        if d0 > d:
            return False
        d0 = d
    return has_double


def main():
    cnt = 0
    for n in range(271973, 785961 + 1):
        if is_valid(n):
            cnt += 1
    print(cnt)


main()
