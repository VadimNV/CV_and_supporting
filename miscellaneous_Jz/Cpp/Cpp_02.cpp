#include <iostream>
 
using namespace std;

//~copy/pasted from [1]
template<typename T>
class Counter {
public:
    Counter() { ++count; }
    Counter(const Counter&) { ++count; }
    ~Counter() { --count; }
 
    static size_t nobjs()
    { return count; }
 
private:
    static size_t count;
};
 
template<typename T>
size_t
Counter<T>::count = 0;

// Example class Window
class Window {
   public:
      void setWidth(int w){
         width = w;       }

      int getWidth(void)  {
         return width;    }

      //static size_t nobjs()               {
      int nobjs()               {
         //casts output to int
         return Counter<Window>::nobjs(); }
      
   protected:
      int width;
   private:
      Counter<Window> c;
             };


//ASSUMPTION: nobody will call a copy-constructor. This will create a new object but won't be counted.
//This is bad practice in general[2]
int main(void) {
   Window w1;
   Window w2;
   Window w3;

   cout << "number of Window objects " << w1.nobjs() << endl;

   return 0;
               }

//[1] http://www.drdobbs.com/cpp/counting-objects-in-c/184403484
//[2] https://stackoverflow.com/questions/7097679/simplest-way-to-count-instances-of-an-object
