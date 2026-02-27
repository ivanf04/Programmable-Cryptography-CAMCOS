#basic sandbox for mode in FHE
import random

#sign function 
def sign(x: int) -> int:
    if(x <= 0):
        return 0
    return 1

#function to determine if two values are equal 
def is_equal(x: int, y: int) -> bool: 
    if (sign(x - y) == 0 and sign(y-x) == 0):
        return True
    return False

#function to cycle a list, start at the end of the list and shift values 
def cycle(step: int, ct: list):
    copy = ct
    last_index = len(ct) - 1
    for j in range(step):
        temp = copy[last_index]
        for i in range(len(ct)):
            copy[last_index - i] = copy[last_index  - i - 1]
        copy[0] = temp
    return copy



#test functions
x = 10 
x1 = 10
y = -1 
z = 0 

# print(sign(x))
# print(sign(y))
# print(sign(z))
# print(is_equal(x,y))
# print(is_equal(x, x1))
 
#generate list of 10 random numbers, rage is (1,9) which gaurentees a duplicate 
list_length = 10
min_value = 1
max_value = 9 

#cypher text which has the data where we would like to find the mode
ct1 = [random.randint(min_value, max_value) for _ in range(list_length)]
print(ct1)

ct2 = cycle(1, ct1)
print(ct2)
print(ct1)

#create ct with all zeros which will store frequencies of data
frequencies = [0] * 10

