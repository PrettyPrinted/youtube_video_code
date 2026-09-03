import sys
import json

def main():
    data = json.load(sys.stdin)
    with open("data.json", "w") as f:
        json.dump(data, f)
    print("I cannot allow you to do that.", file=sys.stderr)
    sys.exit(2)

if __name__ == "__main__":
    main()