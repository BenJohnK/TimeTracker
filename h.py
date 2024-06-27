import os

os.environ["TOKEN"] = "toke"

if "TOKEN" in os.environ:
    print("yes")
else:
    print("no")