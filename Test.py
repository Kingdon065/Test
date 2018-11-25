#! python3
# _*_ coding: utf-8 _*_

numbers = [2, 6, 3, 8, 10]
for n in numbers:
    if n % 2 == 1:
        print('Odd exist')
        break
else:
    print('Odd not exist')

a = 10
print(f'a = {a}')
