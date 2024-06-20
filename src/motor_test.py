#import motor_controls
import math

#motor_controls.auto_run(25600, 0.000003, 0.05, 2)

def round_up(number, decimals):
    multiplier = 10 ** decimals
    return math.ceil(number * multiplier) / multiplier


print(round_up((1 / (5 * 2 / (0.003175 / 16))), 8))