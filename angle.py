import math

PI = math.pi

def sin(theta):
    return math.sin(theta)

def cos(theta):
    return math.cos(theta)

def atan2(y, x):
    return math.atan2(y, x)

def lerple(current, true, max_turn):
    change = (true - current - PI) % (2 * PI) - PI
    change = max(-max_turn, min(max_turn, change))
    #return min(max_turn, max(-max_turn, change))
    return change