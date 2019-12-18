// clang++ -O3 --std=c++17 016.2.cpp

/*
Exploit structure of coefficients as follows:

10N010N010N010N010N010N010N010N010N010N010N010N010N010N010N010N010N010N010N010N0
01100NN001100NN001100NN001100NN001100NN001100NN001100NN001100NN001100NN001100NN0
00111000NNN000111000NNN000111000NNN000111000NNN000111000NNN000111000NNN000111000
00011110000NNNN000011110000NNNN000011110000NNNN000011110000NNNN000011110000NNNN0
00001111100000NNNNN000001111100000NNNNN000001111100000NNNNN000001111100000NNNNN0
00000111111000000NNNNNN000000111111000000NNNNNN000000111111000000NNNNNN000000111
00000011111110000000NNNNNNN000000011111110000000NNNNNNN000000011111110000000NNNN
00000001111111100000000NNNNNNNN000000001111111100000000NNNNNNNN00000000111111110
00000000111111111000000000NNNNNNNNN000000000111111111000000000NNNNNNNNN000000000
00000000011111111110000000000NNNNNNNNNN000000000011111111110000000000NNNNNNNNNN0
00000000001111111111100000000000NNNNNNNNNNN000000000001111111111100000000000NNNN
00000000000111111111111000000000000NNNNNNNNNNNN000000000000111111111111000000000
00000000000011111111111110000000000000NNNNNNNNNNNNN00000000000001111111111111000
00000000000001111111111111100000000000000NNNNNNNNNNNNNN0000000000000011111111111
00000000000000111111111111111000000000000000NNNNNNNNNNNNNNN000000000000000111111
00000000000000011111111111111110000000000000000NNNNNNNNNNNNNNNN00000000000000001
00000000000000001111111111111111100000000000000000NNNNNNNNNNNNNNNNN0000000000000
00000000000000000111111111111111111000000000000000000NNNNNNNNNNNNNNNNNN000000000


for digit d (0, 1, 2, ..) the pattern is 
starting with offset d
sum d digits
skip d digits
subtract d digits
repeat until out of digits

*/

#include <cstddef>
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>

u_char compute_fft_digit(const std::vector<u_char> &number, size_t _digit)
{
  const size_t digit = _digit + 1;
  int result = 0;
  bool add = true;
  size_t d = digit - 1; // start at offset
  while (d < number.size())
  {
    if (add)
    {
      size_t end = d + digit;
      while (d < end && d < number.size())
      {
        result += number[d];
        d++;
      }
      d += digit;
      add = false;
      continue;
    }
    else
    {
      size_t end = d + digit;
      while (d < end && d < number.size())
      {
        result -= number[d];
        d++;
      }
      d += digit;
      add = true;
      continue;
    }
  }
  // std::cout << std::endl;

  return std::abs(result) % 10;
}

std::vector<u_char> compute_fft(const std::vector<u_char> &number)
{
  std::vector<u_char> result;
  result.resize(number.size());
  for (size_t d = 0; d < number.size(); d++)
  {
    result[d] = compute_fft_digit(number, d);
  }
  return result;
}

std::vector<u_char> str_to_number(const std::string &_number)
{
  std::vector<u_char> number;
  number.resize(_number.size());
  for (size_t i = 0; i < _number.size(); i++)
  {
    number[i] = _number[i] - '0';
  }
  return number;
}

void print_number(std::vector<u_char> &number, size_t offset, size_t size)
{
  for (size_t i = offset; i < offset + size; i++)
  {
    std::cout << number[i];
  }
  std::cout << std::endl;
}

void test1()
{
  auto number = str_to_number("69317163492948606335995924319873");
  for (size_t i = 0; i < 100; i++)
  {
    number = compute_fft(number);
  }
  print_number(number, 0, 8);
}

void test2()
{
  std::ifstream t("016.1.input.txt");
  std::stringstream buffer;
  buffer << t.rdbuf();

  auto number = str_to_number(buffer.str());
  for (size_t i = 0; i < 100; i++)
  {
    number = compute_fft(number);
  }
  print_number(number, 0, 8);
}

std::string load_repeated_number(const std::string fname)
{
  std::ifstream t(fname);
  std::stringstream buffer;
  buffer << t.rdbuf();
  const std::string number_templ = buffer.str();
  std::string number;
  for (size_t i = 0; i < 10000; i++)
  {
    number.append(number_templ);
  }
  return number;
}

int main(int argc, char *argv[])
{
  //test2();
  std::string number_str = load_repeated_number("016.2.test2.txt");
  auto number = str_to_number(number_str);
  size_t offset = std::stoi(number_str.substr(0, 7));

  for (size_t i = 0; i < 100; i++)
  {
    std::cout << i << std::endl;
    number = compute_fft(number);
  }
  print_number(number, offset, 8);

  return 0;
}