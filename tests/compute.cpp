#include <cstdint>
#include <iostream>
#include <string>

int main() {
    std::string op;
    std::uint32_t a, b;
    if (!(std::cin >> op >> a >> b)) return 2;

    std::uint32_t result = 0;
    if (op == "add") result = a + b;
    else if (op == "sub") result = a - b;
    else if (op == "mul") result = a * b;
    else if (op == "and") result = a & b;
    else if (op == "or") result = a | b;
    else if (op == "xor") result = a ^ b;
    else if (op == "shl") result = a << (b % 32);
    else if (op == "shr") result = a >> (b % 32);
    else return 3;

    std::cout << result << '\n';
    return 0;
}
