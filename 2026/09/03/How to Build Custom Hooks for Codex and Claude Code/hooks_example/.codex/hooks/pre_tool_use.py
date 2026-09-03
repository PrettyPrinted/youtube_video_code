import sys
import json
from time import time

def main():
    data = json.load(sys.stdin)
    with open(f"data_{time()}.json", "w") as f:
        json.dump(data, f)

    if "ls" in data["tool_input"]["command"]:
        print("I cannot allow you to do that.", file=sys.stderr)
        sys.exit(2)
    

if __name__ == "__main__":
    main()