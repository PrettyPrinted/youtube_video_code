a = {'id' : 5, 'username' : 'PythonUser', 'email' : 'pythonista@gmail.com'}
b = {'id' : 5, 'username' : 'PythonUser', 'email' : 'iluvpython@outlook.com'}

print(a | b)
{**b, **a}

#b.update(a)
#print(b)
a |= b
print(a)