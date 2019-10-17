def multiply_then_add(x, y, z, /, print_this='Nothing'):
    print(print_this)
    return x * y + z

print(multiply_then_add(5, 10, 20, print_this='Something'))