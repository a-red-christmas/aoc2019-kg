// Feed in the list of module weights via stdin
// Output is via stdout

#include <iostream>


int fuel(int mass) {
   if(mass < 9) return 0;
   int f = mass / 3 - 2;
   return f + fuel(f);
}


int main(int argc, char *argv[]) {
   int total_fuel = 0;
   std::string mass;
   while(std::getline(std::cin, mass)) {
       total_fuel += fuel(std::stoi(mass));
   }
   std::cout << total_fuel;
}
