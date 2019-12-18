// clang++ --std=c++17 016.2.cpp

#include <cstddef>
#include <vector>
#include <iostream>

int compute_fft_digit(const std::vector<int> &number, size_t _digit)
{
  const size_t digit = _digit + 1;
  int result = 0;
  size_t d = 0;
  size_t c = 1;
  size_t index = 0;
  const char seed[] = "010N";
  while (d < number.size())
  {
    if (c >= digit)
    {
      c = 0;
      index = (index + 1) % 4;
    }

    // std::cout << seed[index];

    switch (seed[index])
    {
    case '1':
      result += number[d];
      break;

    case 'N':
      result -= number[d];
    }

    c++;
    d++;
  }
  // std::cout << std::endl;

  return std::abs(result) % 10;
}

std::vector<int> compute_fft(const std::vector<int> &number)
{
  std::vector<int> result;
  result.resize(number.size());
  for (size_t d = 0; d < number.size(); d++)
  {
    result[d] = compute_fft_digit(number, d);
  }
  return result;
}

std::vector<int> load_number(const std::string &_number)
{
  std::vector<int> number;
  number.resize(_number.size());
  for (size_t i = 0; i < _number.size(); i++)
  {
    number[i] = _number[i] - '0';
  }
  return number;
}

void print_number(std::vector<int> &number, size_t offset, size_t size)
{
  for (size_t i = offset; i < offset + size; i++)
  {
    std::cout << number[i];
  }
  std::cout << std::endl;
}

void test1()
{
  std::vector<int> number = load_number("69317163492948606335995924319873");
  for (size_t i = 0; i < 100; i++)
  {
    number = compute_fft(number);
  }
  print_number(number, 0, 8);
}

int main(int argc, char *argv[])
{
  // std::vector<int> number = load_number("12345678");
  // auto result = compute_fft(number);
  // print_number(result, 0, result.size());
  test1();
  return 0;
}