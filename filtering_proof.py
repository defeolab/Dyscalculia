import math

# This function calculates the difficulty co-efficient wrt filtering hypothesis. The difficulty co-efficient is defined by an angle between the reference line and the line joining the point P(x,y).
# x = Normalized value of Numerical Dimension ( Number of chickens on both sides)
# y = Normalized value of Non Numerical Dimension ( Field Area : FA and Item Surface Area : ISA)
# k = angle between the line joining the point P(x,y) and x-axis
# a = (alpha) measure of difficulty co-efiicient. 
# If P(x,y) falls in 1st and 3rd quadrant, k = tanInverse(y/x)
# If P(x,y) falls in 2nd and 4th quadrant, k = pi-abs(tanInverse(y/x)) , where pi = 180 deg
# a = abs(pi/4 - k)
# Once we have the difficulty co-efficient calculated for all the trials, we need to sort the trails in ascending or descending order w.r.t the difficulty co-efficient value.
# Lower the value of 'a', less difficult will be the trail and vise versa.

def diff_coef(x, y):
    # If P(x,y) falls in 1st or 3rd Quadrant
    if (x > 0 and y >= 0) or (x < 0 and y <= 0):
        k = math.degrees(math.atan(y/x))
    # If P(x,y) falls in 2nd or 4th quadrant
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
