import sys

lst = []
for line in sys.stdin:
    if line == '\n':
        break
    else:
        lst.append(line.split(','))
#print(lst)

def calculate_grades(two_dimensional_list):
    new_list1 = []

    for each in two_dimensional_list:
        new_list2 = [each[0]]
        total = 0
        
        for i in range(1,len(each)):
            total += int(each[i])
            
        new_list2.append(total/4)
        new_each = tuple(new_list2)
        new_list1.append(new_each)
        
    new_tuple = tuple(sorted(new_list1))

    return new_tuple

result = calculate_grades(lst)
print(result)
