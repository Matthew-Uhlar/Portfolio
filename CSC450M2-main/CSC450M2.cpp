#include <iostream>
#include <string>

int main() {
    std::string firstString, secondString, concatenatedString;

    for (int i = 1; i <= 3; ++i) {
        std::cout << "Enter first string for attempt " << i << ": ";
        std::getline(std::cin, firstString);

        std::cout << "Enter second string for attempt " << i << ": ";
        std::getline(std::cin, secondString);

        concatenatedString = firstString + secondString;
        std::cout << "Concatenated result: " << concatenatedString << "\n\n";
    }

    return 0;
}
