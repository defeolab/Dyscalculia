import math

def diff_coef(x, y):
    if (x > 0 and y >= 0) or (x < 0 and y <= 0):
        k = math.degrees(math.atan(y/x))
    elif (x < 0 and y > 0) or (x > 0 and y < 0):
        k = math.pi - abs(math.atan(y/x))
    a = math.degrees(abs((math.pi/4)-k))
    return k, a

x = int(input("x: "))
y = int(input("y: "))

while x != 'e' and y != 'e':
    k, a = diff_coef(x, y)
    print("k: {} - alpha: {} \n".format(k, a))
    
    x = int(input("x: "))
    y = int(input("y: "))