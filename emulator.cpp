#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <typeinfo>
#include <sstream>

using namespace std;

template<typename T2, typename T1>
inline T2 lexical_cast(const T1 &in) {
    T2 out;
    std::stringstream ss;
    ss << in;
    ss >> out;
    return out;
}

void decToBinary(int n) 
{ 
    // array to store binary number 
    int binaryNum[32]; 
  
    // counter for binary array 
    int i = 0; 
    while (n > 0) { 
  
        // storing remainder in binary array 
        binaryNum[i] = n % 2; 
        n = n / 2; 
        i++; 
    } 
  
    // printing binary array in reverse order 
    for (int j = i - 1; j >= 0; j--) 
        cout << binaryNum[j]; 
} 

int main(int argc, char const *argv[])
{
    ifstream in;

    in.open("assembled/raw.swag", ios::in | ios::binary);

    if(in.is_open())
    {
        // get the starting position
        streampos start = in.tellg();

        // go to the end
        in.seekg(0, std::ios::end);

        // get the ending position
        streampos end = in.tellg();

        // go back to the start
        in.seekg(0, std::ios::beg);

        // create a vector to hold the data that
        // is resized to the total size of the file    
        std::vector<char> contents;
        contents.resize(static_cast<size_t>(end - start));

        // read it in
        in.read(&contents[0], contents.size());

        // print it out (for )
        for (int i = 0; i < contents.size(); i++) {
            const char* swag = ("%02X\n", (const char*)(contents.at(i))); //&0xFF
            unsigned int x = lexical_cast<unsigned int>(swag); 
            cout << x << endl;
            //printf("\n");
        }
    }
    return 0;
}
