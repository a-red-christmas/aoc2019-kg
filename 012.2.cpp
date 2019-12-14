// Since the cycle maybe long, storing the past states in a set and
// testing them may be infeasible. We can probably use the tortoise and
// hare trick here: we do two simulations in parallel. One goes one step
// at a time and the other two steps. When the two step simulation coincides
// or jumps over the single step simulation, we have a cycle.
// I haven't thought of a faster way to do the simulation, so I'm just going to
// write the code in C++ and see what happens

// clang++ -Oz --std=c++17 012.2.cpp
#include <iostream>
#include <cstdlib>

struct Moon
{
  long x, y, z;
  long vx, vy, vz;

  void update()
  {
    x += vx;
    y += vy;
    z += vz;
  }

  int te()
  {
    int pe = std::abs(x) + std::abs(y) + std::abs(z);
    int ke = std::abs(vx) + std::abs(vy) + std::abs(vz);
    return pe * ke;
  }

  bool operator==(const Moon &moon) const
  {
    return x == moon.x && y == moon.y && z == moon.z && vx == moon.vx && vy == moon.vy && vz == moon.vz;
  }
};

Moon *example1()
{
  Moon *moons = new Moon[4]{
      {-1, 0, 2, 0, 0, 0},
      {2, -10, -7, 0, 0, 0},
      {4, -8, 8, 0, 0, 0},
      {3, 5, -1, 0, 0, 0}};
  return moons;
}

Moon *example2()
{
  Moon *moons = new Moon[4]{
      {-8, -10, 0, 0, 0, 0},
      {5, 5, 10, 0, 0, 0},
      {2, -7, 3, 0, 0, 0},
      {9, -8, -3, 0, 0, 0}};
  return moons;
}

Moon *initial_state()
{
  Moon *moons = new Moon[4]{
      {-4, -9, -3, 0, 0, 0},
      {-13, -11, 0, 0, 0, 0},
      {-17, -7, 15, 0, 0, 0},
      {-16, 4, 2, 0, 0, 0}};
  return moons;
}

struct Simulation
{
  Moon *moons;

  Simulation()
  {
    moons = initial_state();
    // moons = example1();
    // moons = example2();
  }

  void step()
  {
    apply_gravity();
    for (int i = 0; i < 4; i++)
    {
      moons[i].update();
    }
  }

  void apply_gravity()
  {
    for (int i = 0; i < 3; i++)
    {
      for (int j = i + 1; j < 4; j++)
      {
        if (moons[i].x < moons[j].x)
        {
          moons[i].vx++;
          moons[j].vx--;
        }
        else if (moons[i].x > moons[j].x)
        {
          moons[i].vx--;
          moons[j].vx++;
        }

        if (moons[i].y < moons[j].y)
        {
          moons[i].vy++;
          moons[j].vy--;
        }
        else if (moons[i].y > moons[j].y)
        {
          moons[i].vy--;
          moons[j].vy++;
        }

        if (moons[i].z < moons[j].z)
        {
          moons[i].vz++;
          moons[j].vz--;
        }
        else if (moons[i].z > moons[j].z)
        {
          moons[i].vz--;
          moons[j].vz++;
        }
      }
    }
  }

  int compute_dv(int x0, int x1)
  {
    if (x0 == x1)
      return 0;
    if (x0 < x1)
      return 1;
    return -1;
  }

  bool operator==(const Simulation &sim) const
  {
    return moons[0] == sim.moons[0] && moons[1] == sim.moons[1] && moons[2] == sim.moons[2] && moons[3] == sim.moons[3];
  }
};

void simulate_test()
{
  Simulation sim;
  for (int i = 0; i < 1000; i++)
    sim.step();

  int te = 0;
  for (int i = 0; i < 4; i++)
  {
    te += sim.moons[i].te();
  }

  std::cout << te << std::endl;
}

int main(int argc, char *argv[])
{
  // simulate_test();

  Simulation sim1, sim2;
  sim1.step();
  sim2.step();
  sim2.step();

  size_t s1 = 1, s2 = 2;
  for (;;)
  {
    sim1.step();
    s1 += 1;

    sim2.step();
    s2 += 1;
    if (sim1 == sim2)
    {
      break;
    }

    sim2.step();
    s2 += 1;
    if (sim1 == sim2)
    {
      break;
    }

    // if (s1 % 1000000 == 0)
    // {
    //   std::cout << s1 << std::endl;
    // }
  }

  std::cout << s2 - s1;

  return 0;
}
