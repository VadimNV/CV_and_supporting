#!/usr/bin/python
"""
folloring YouTube Richard White
"""

class Person(object):
    # Constructor
    def __init__(self,theName):
        self.name = theName
    # Accesser (getter)
    def getName(self):
        return self.name

    # Mutator  (setter) 
    def setName(self,newName):
        self.name = newName

def main():
    print "Hello world"
    friend1 = Person("John")
    friend2 = Person("Barbara")

    print friend1.getName()
    friend2.setName("Eleonor")
    print friend2.getName()

if __name__ == "__main__":
    main()
