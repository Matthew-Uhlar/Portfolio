#include <iostream>
using namespace std;

int main() {
    int a, b, c;
    
    // Ask the user to input three integer values
    cout << "Enter three integer values: ";
    cin >> a >> b >> c;
    
    // Dynamically allocate memory for each integer and initialize it
    int* ptrA = new int(a);
    int* ptrB = new int(b);
    int* ptrC = new int(c);
    
    // Display the values and the memory addresses stored in the pointers
    cout << "Value of a: " << a << ", Address in ptrA: " << ptrA << ", Value pointed by ptrA: " << *ptrA << endl;
    cout << "Value of b: " << b << ", Address in ptrB: " << ptrB << ", Value pointed by ptrB: " << *ptrB << endl;
    cout << "Value of c: " << c << ", Address in ptrC: " << ptrC << ", Value pointed by ptrC: " << *ptrC << endl;
    
    // Free the dynamically allocated memory
    delete ptrA;
    delete ptrB;
    delete ptrC;
    
    return 0;
}
