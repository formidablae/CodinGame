import math
import sys

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())  # the number of temperatures to analyse
result = 0
if n != 0:
    result = 5527
    for i in input().split():
        # t: a temperature expressed as an integer ranging from -273 to 5526
        t = int(i)
        if abs(result) > abs(t):
            result = t
        elif abs(result) == t:
            result = t

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr)

print(result)
