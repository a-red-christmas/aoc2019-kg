# Given the small scope of the problem, I'm ok with
# a simple brute force solution
# here we just check the three adjacents for dupes


def is_valid(n):
    num = str(n)
    has_double = False
    for i in range(1, 6):
        if num[i - 1] == num[i]:
            left_ok = True
            right_ok = True
            if i > 1:
                left_ok = num[i - 2] != num[i - 1]
            if i < 5:
                right_ok = num[i] != num[i + 1]

            if left_ok and right_ok:
                has_double = True

        if num[i - 1] > num[i]:
            return False
    return has_double


def main():
    cnt = 0
    for n in range(271973, 785961 + 1):
        if is_valid(n):
            cnt += 1
    print(cnt)


main()
