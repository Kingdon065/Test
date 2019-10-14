#! python3
# _*_ coding:utf-8 _*_

dict={'obj':'world','name':'python'}
print('hello {names[obj]} i am {names[name]}'.format(names=dict))

print('{!r}国'.format('中'))
print('{!s:>10}国'.format('中'))
print('{!a}国'.format('中'))