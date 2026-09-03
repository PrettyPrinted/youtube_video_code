import sys

print(sys.stdin.read())

print("I cannot allow you to do that.", file=sys.stderr)

sys.exit(2)