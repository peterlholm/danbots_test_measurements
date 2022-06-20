import numpy as np
from sklearn.linear_model import LinearRegression
import math

def linear_regress(dataarray):
    x=[]
    y=[]
    for d in dataarray:
        x.append(d[0])
        y.append(d[1])
    xx = np.array(x).reshape((-1,1))
    yy = np.array(y)

    model = LinearRegression()

    model.fit(xx,yy)
    #r_sq = model.score(xx, yy)
    #print('coefficient of determination:', r_sq)
    #print('intercept:', model.intercept_)
    #print('slope:', model.coef_)
    deg = math.atan(model.coef_/1.0)
    degree=360*deg/(2*math.pi)
    return degree

if __name__ == "__main__":
    print ("test")
    arr = [(0,0),(1,1),(2,2)]
    res = linear_regress(arr)
    print ("slope",res)
