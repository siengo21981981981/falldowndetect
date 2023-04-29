import re
print(re.match("sir", "hello, sir"))
print(re.search("sir", "hello, sir"))

patten = re.compile('\d{4}-\d{6}')
print(patten)
print(patten.match('123-456'))
print(patten.match('0936-279195'))
