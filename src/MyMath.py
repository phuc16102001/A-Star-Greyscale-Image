######################################
#                                    #
# Project name: A* for greyscale img #
# Author: Do Vuong Phuc              #
# Author: Hoang Nhu Thanh            #
# Date: 07/12/2021                   #
# Contact: phuc16102001@gmail.com    #
# * Please do not copy the source *  #
#                                    #
######################################

import math  #sqrt

#Take the absolute value of a number
#Input: x = float number
#Output: Absolute value of x
def abs(x):
    if (x<0):
        return -x
    return x

#Take the sign function of x
#sign(x) = -1 (x<0)
#sign(x) = 0  (x=0)
#sign(x) = 1  (x>0)
#Input: x = float number
#Output: Sign function result of x
def sign(x):
    if (x<0):
        return -1
    elif (x>0):
        return 1
    return 0
