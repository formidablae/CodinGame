import math
import sys

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
# ---
# Hint: You can use the debug stream to print initialTX and initialTY, if Thor seems not follow your orders.

# light_x: the X position of the light of power
# light_y: the Y position of the light of power
# initial_tx: Thor's starting X position
# initial_ty: Thor's starting Y position
light_x, light_y, initial_tx, initial_ty = [int(i) for i in input().split()]

# game loop
while True:
    # The remaining amount of turns Thor can move. Do not remove this line.
    remaining_turns = int(input())

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    if light_x == initial_tx:
        if light_y == initial_ty:
            break
        elif light_y > initial_ty:
            print("S")
            initial_ty = initial_ty + 1
        else:
            print("N")
            initial_ty = initial_ty - 1
    elif light_x > initial_tx:
        initial_tx = initial_tx + 1
        if light_y == initial_ty:
            print("E")
        elif light_y > initial_ty:
            print("SE")
            initial_ty = initial_ty + 1
        else:
            print("NE")
            initial_ty = initial_ty - 1
    else:
        initial_tx = initial_tx - 1
        if light_y == initial_ty:
            print("W")
        elif light_y > initial_ty:
            print("SW")
            initial_ty = initial_ty + 1
        else:
            print("NW")
            initial_ty = initial_ty - 1

    # A single line providing the move to be made: N NE E SE S SW W or NW
