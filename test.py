original_list = [i for i in range(100)]
sublists = [original_list[i:i + 7] for i in range(0, len(original_list), 7)]

for i in sublists[0]:
    print(i)