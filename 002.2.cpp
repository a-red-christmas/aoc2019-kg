// Santa's Intcode computer
// clang++ --std=c++17 002.1.cpp

#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>

class IntCodeComputer;
typedef void (IntCodeComputer::*IntCodeOp)();

struct OpCode
{
  size_t advance;
  IntCodeOp run;
};

class IntCodeComputer
{
public:
  IntCodeComputer()
  {
    opcodes[1] = {4, &IntCodeComputer::_add};
    opcodes[2] = {4, &IntCodeComputer::_mul};
    opcodes[99] = {0, &IntCodeComputer::_halt};
  }

  void load_core(std::vector<int> _program)
  {
    program = std::vector<int>(_program);
    program_counter = 0;
    running = true;
    error = false;
  }

  void set_noun_verb(size_t noun, size_t verb)
  {
    program[1] = noun;
    program[2] = verb;
  }

  void run()
  {
    while (running)
    {
      step();
    }
  }

  bool is_running() { return running; }
  bool has_error() { return error; }

  void step()
  {
    if (program_counter >= program.size())
    {
      running = false;
      error = true;
    }

    try
    {
      auto opcode = opcodes[program[program_counter]];
      (this->*opcode.run)();
      program_counter += opcode.advance;
    }
    catch (const std::out_of_range &e)
    {
      running = false;
      error = true;
    }
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
  bool running;
  bool error;
  std::unordered_map<int, OpCode> opcodes;

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

  void _halt()
  {
    running = false;
    error = false;
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

  for (int noun = 0; noun < 100; noun++)
  {
    for (int verb = 0; verb < 100; verb++)
    {
      computer.load_core(program);
      computer.set_noun_verb(noun, verb);
      computer.run();
      if (!computer.has_error())
      {
        if (computer.peek(0) == 19690720)
        {
          std::cout << noun << ", " << verb;
          break;
        }
      }
    }
  }

  // computer.core_dump();
  // std::cout << computer.peek(0);
  return 1;
}
