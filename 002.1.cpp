// Santa's Intcode computer
// clang++ --std=c++17 002.1.cpp

#include <iostream>
#include <fstream>
#include <vector>

const int ADD = 1;
const int MUL = 2;
const int HLT = 99;

class IntCodeComputer
{
public:
  IntCodeComputer()
  {
    program_counter = 0;
  }

  void load_core(std::vector<int> _program)
  {
    program = _program;
  }

  int step()
  {
    if (program_counter >= program.size())
    {
      return 0;
    }

    switch (program[program_counter])
    {
    case HLT:
      return 0;
    case ADD:
      _add();
      break;
    case MUL:
      _mul();
      break;
    default:
      return 0;
    }

    program_counter += 4;
    return 1;
  }

  int peek(size_t i)
  {
    return program[i];
  }

  void core_dump()
  {
    for (int v : program)
    {
      std::cout << v << ",";
    }
  }

private:
  std::vector<int> program;
  size_t program_counter;

  void _add()
  {
    int i = program[program_counter + 1];
    int j = program[program_counter + 2];
    int k = program[program_counter + 3];
    int a = program[i];
    int b = program[j];
    program[k] = a + b;
  }

  void _mul()
  {
    int i = program[program_counter + 1];
    int j = program[program_counter + 2];
    int k = program[program_counter + 3];
    int a = program[i];
    int b = program[j];
    program[k] = a * b;
  }
};

std::vector<int> read_program()
{
  std::vector<int> program;
  std::string opcode;
  while (std::getline(std::cin, opcode, ','))
  {
    program.push_back(std::stoi(opcode));
  }
  return program;
}

int main(int argc, char *argv[])
{
  IntCodeComputer computer;
  std::vector<int> program = read_program();

  // Comment out for testing
  program[1] = 12;
  program[2] = 2;

  computer.load_core(program);

  while (computer.step())
  {
  }

  computer.core_dump();
  // std::cout << computer.peek(0);
  return 1;
}
