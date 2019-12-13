import sys


class Moon:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def update(self):
        self.pos = [p + v for p, v in zip(self.pos, self.vel)]

    def pe(self):
        return sum(abs(p) for p in self.pos)

    def ke(self):
        return sum(abs(v) for v in self.vel)

    def te(self):
        return self.pe() * self.ke()

    def __str__(self):
        return f"p={self.pos} v={self.vel} te={self.te()}"


def apply_gravity(moons):
    for i in range(len(moons) - 1):
        for j in range(i + 1, len(moons)):
            for n in [0, 1, 2]:
                if moons[i].pos[n] == moons[j].pos[n]:
                    continue
                elif moons[i].pos[n] < moons[j].pos[n]:
                    dv = 1
                else:
                    dv = -1

                moons[i].vel[n] += dv
                moons[j].vel[n] -= dv


def simulate(moons, n_steps, print_system=False):
    for n in range(n_steps):
        if print_system:
            print()
            for moon in moons: print(moon)

        apply_gravity(moons)
        for moon in moons:
            moon.update()


def main():
    with open(sys.argv[1], "r") as f:
        pos = [[int(x) for x in p.strip().split(",")] for p in f.readlines()]

    moons = [Moon(p, [0, 0, 0]) for p in pos]
    simulate(moons, 1000)

    print(sum(moon.te() for moon in moons))


main()
