// clang++ -O3 --std=c++17 016.2.1.cpp

/*
Our naive computation is N^2.

Now, looking at the structure of the coefficients

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

One idea would be to compute each digit as a sum of groups. Each group is a
"glider" a cluster of 1s or -1s (N) that "glides" across. 

The first glider is a cluster of 1s that starts at the first digit and advances
by one, growing by 1.

The next glider is a cluster of -1 that starts in multiples of 3 and grows by 1

The next is a cluster of 1 that starts in multiples of 5 and grows by 1

Cluster of -1, starts in multiples of 7, grows by 1

The computation of each cluster can be made constant time by computing the
cumulative sum and using that.

**Another interesting observation is that the nth digit only depends on the the
values of the nth digit onwards.**

*/

#include <cstddef>
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <string>

int array_sum(const std::vector<u_char> &number, size_t i, size_t j)
{
  int sum = 0;
  for (size_t k = i; k < j and k < number.size(); k++)
  {
    sum += number[k];
  }
  return sum;
}

std::vector<u_char> str_to_number(const std::string &_number, size_t repeats = 1)
{
  std::vector<u_char> number;
  number.resize(_number.size() * repeats);
  for (size_t i = 0; i < _number.size(); i++)
  {
    number[i] = _number[i % _number.size()] - '0';
  }
  return number;
}

std::string load_number_from_file(const std::string fname)
{
  std::ifstream t(fname);
  std::stringstream buffer;
  buffer << t.rdbuf();
  return buffer.str();
}

void print_number(const std::vector<u_char> &number, size_t offset, size_t size)
{
  for (size_t i = offset; i < offset + size; i++)
  {
    std::cout << std::to_string(number[i]);
  }
  std::cout << std::endl;
}

struct Range
{
  size_t start;
  size_t end;
};

struct Glider
{
  size_t slope;
  size_t size;
  Range range;
  bool add;
  int sum;

  Glider(size_t _start, int _sum, size_t _slope, bool _add)
  {
    slope = _slope;
    add = _add;
    size = 1;
    range.start = _start;
    range.end = _start + 1;
    sum = _sum;
  }

  int get_sum()
  {
    return add ? sum : -sum;
  }

  bool done(const std::vector<size_t> &number)
  {
    return range.start >= number.size();
  }

  int next(const std::vector<size_t> &cum_sum)
  {
    size++;
    range = {range.start + slope, range.start + slope + size};
    if (done(cum_sum))
      return 0;

    sum = cum_sum[std::min(range.end - 1, cum_sum.size() - 1)] - cum_sum[range.start - 1];
    return get_sum();
  }
};

void print_gliders(std::vector<Glider> &gliders, size_t len)
{
  std::vector<u_char> coeffs;
  coeffs.resize(len, 0);

  for (size_t d = 0; d < len; d++)
  {
    for (size_t i = 0; i < gliders.size(); i++)
    {
      for (size_t k = gliders[i].range.start; k < gliders[i].range.end && k < len; k++)
      {
        coeffs[k] = gliders[i].add ? 1 : 3;
      }
    }
  }
  print_number(coeffs, 0, len);
}

struct FFT
{
  std::vector<u_char> buf[2];
  std::vector<size_t> cum_sum;
  size_t buf_no;

  FFT(const std::string &_number, size_t repeats = 1)
  {
    buf[0] = str_to_number(_number, repeats);
    buf[1].resize(buf[0].size());
    cum_sum.resize(buf[0].size());
    buf_no = 0;
  }

  const std::vector<u_char> &get_number()
  {
    return buf[buf_no];
  }

  const std::vector<u_char> &compute(bool diagnostic = false)
  {
    const auto &in = buf[buf_no];
    auto &out = buf[1 - buf_no];

    cum_sum[0] = in[0];
    for (size_t i = 1; i < in.size(); i++)
    {
      cum_sum[i] = in[i] + cum_sum[i - 1];
    }

    size_t glider_count = 0;
    bool add = true;
    size_t slope = 1;
    std::vector<Glider> gliders;
    int sum = 0;
    for (size_t d = 0; d < in.size(); d += 2)
    {
      gliders.push_back(Glider(d, in[d], d + 1, add));
      sum += gliders[glider_count].get_sum();
      add = !add;
      glider_count += 1;
    }
    out[0] = std::abs(sum) % 10;

    for (size_t d = 1; d < in.size(); d++)
    {
      if (diagnostic)
        print_gliders(gliders, in.size());
      sum = 0;
      for (size_t i = 0; i < glider_count; i++)
      {
        sum += gliders[i].next(cum_sum);
        // std::cout << gliders[i].get_sum() << ", ";
      }
      // std::cout << std::endl;
      out[d] = std::abs(sum) % 10;
      // This is the magic that makes things NlogN : remove unused gliders
      if (gliders[glider_count - 1].done(cum_sum))
        glider_count--;
    }

    if (diagnostic)
      print_gliders(gliders, in.size());

    buf_no = 1 - buf_no;
    return out;
  }
};

void multiplicand_diagnostic()
{
  FFT fft("1234567890123456789012345678901234567890");
  fft.compute(true);
}

void test0()
{
  FFT fft("12345678");
  print_number(fft.get_number(), 0, 8);
  print_number(fft.compute(), 0, 8);
  print_number(fft.compute(), 0, 8);
  print_number(fft.compute(), 0, 8);
}

void test1()
{
  FFT fft("69317163492948606335995924319873");

  print_number(fft.get_number(), 0, 8);
  for (size_t i = 0; i < 100; i++)
  {
    print_number(fft.compute(), 0, 8);
  }
}

void test2()
{
  std::string number_str = "03081770884921959731165446850517";
  FFT fft(number_str, 10000);
  size_t offset = std::stoi(number_str.substr(0, 7));
  print_number(fft.get_number(), 0, 8);
  for (size_t i = 0; i < 100; i++)
  {
    std::cout << "." << std::flush;
    fft.compute();
  }
  print_number(fft.get_number(), offset, 8);
}

void main_problem()
{
  std::string number_str = load_number_from_file("016.1.input.txt");
  size_t offset = std::stoi(number_str.substr(0, 7));

  FFT fft(number_str, 10000);
  print_number(fft.get_number(), offset, 8);
  for (size_t i = 0; i < 100; i++)
  {
    std::cout << "." << std::flush;
    fft.compute();
  }
  std::cout << std::endl;
  print_number(fft.get_number(), offset, 8);
}

int main(int argc, char *argv[])
{
  // multiplicand_diagnostic();
  // test0();
  // test1();
  test2();
  // main_problem();
  return 0;
}