import math


def logModel(x1, x2):
    if (x2 > math.log(x1)):
        return True
    else:
        return False


def circleModel(x1, x2):
    if ((x1-12.5)*(x1-12.5)+x2*x2<100 or (x1+12.5)*(x1+12.5)+x2*x2<100):
        return True
    else:
        return False


def polynomialModel(x1, x2):
    if (x2 > x1 * x1 * x1 + x1 * x1 + x1):
        return True
    else:
        return False

def polycircleModel(center, radius, x):
    for i in range(len(center)):
        pointradius = 0
        for j in range(len(x)):
            pointradius += (x[j]-center[i][j])*(x[j]-center[i][j])
        if (pointradius < radius[i]):
            return True
    return False