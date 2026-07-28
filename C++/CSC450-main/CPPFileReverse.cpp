#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>

using namespace std;

// Function to reverse the contents of the file
void reverseFileContents(const string& inputFile, const string& outputFile) {
    ifstream inFile(inputFile);
    if (!inFile) {
        cerr << "Error opening input file!" << endl;
        return;
    }
    
    string content((istreambuf_iterator<char>(inFile)), istreambuf_iterator<char>());
    inFile.close();
    
    reverse(content.begin(), content.end());
    
    ofstream outFile(outputFile);
    if (!outFile) {
        cerr << "Error opening output file!" << endl;
        return;
    }
    outFile << content;
    outFile.close();
    
    cout << "File contents reversed successfully!" << endl;
}

int main() {
    string userInput;
    string inputFile = "CSC450_CT5_mod5.txt";
    string outputFile = "CSC450-mod5-reverse.txt";
    
    cout << "Enter text to append to the file: ";
    getline(cin, userInput);
    
    // Append user input to the file
    ofstream outFile(inputFile, ios::app);
    if (!outFile) {
        cerr << "Error opening file for appending!" << endl;
        return 1;
    }
    outFile << userInput << endl;
    outFile.close();
    
    cout << "Text appended successfully!" << endl;
    
    // Reverse file contents
    reverseFileContents(inputFile, outputFile);
    
    return 0;
}
