# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 12:57:24 2018

@author: Matthew Uhlar
"""

import numpy as np

#creates the matrix with the set dimentions
Mat1 = range(1, 36)
Mat1 = np.reshape(Mat1,(7,5)) 

#prints the matrix
print ("\n\nThe next matrix is \n")
print(Mat1) 

#sets variable equal to the new matrix
mat1 = np.matrix(Mat1)
#creates and writes the matrix to a file
with open('MUhlar_mat1.txt', 'w+') as f:
    for line in mat1:
        np.savetxt(f, line, fmt=' %d ')
f.close()



Mat2 = range(3, 108, 3)
Mat2 = np.reshape(Mat2,(5,7)) 

print ("\n\nThe next matrix is \n")
print(Mat2) 

mat2 = np.matrix(Mat2)
with open('MUhlar_mat2.txt', 'w+') as f:
    for line in mat2:
        np.savetxt(f, line, fmt=' %d ')
f.close()



Mat3 = range(3, 108, 3)
#order=f has it iterate over the colums first
Mat3 = np.reshape(Mat3,(5,7), order='F')

print ("\n\nThe next matrix is \n")
print(Mat3) 

mat3 = np.matrix(Mat3)
with open('MUhlar_mat3.txt', 'w+') as f:
    for line in mat3:
        np.savetxt(f, line, fmt=' %d ')
f.close()


#linspace fills the array with a set number of values between the start and end which allows you to fill it with floats
Mat4 = np.linspace(0.2, 10.4, 35)
Mat4 = np.reshape(Mat4,(5,7)) 

print ("\n\nThe next matrix is \n")
print(Mat4) 

mat4 = np.matrix(Mat4)
with open('MUhlar_mat4.txt', 'w+') as f:
    for line in mat4:
        np.savetxt(f, line, fmt=' %.1f ')
f.close()



Mat5 = range(2, 310, 2)
Mat5 = np.reshape(Mat5,(11,14)) 

print ("\n\nThe next matrix is \n")
print(Mat5) 

mat5 = np.matrix(Mat5)
with open('MUhlar_mat5.txt', 'w+') as f:
    for line in mat5:
        np.savetxt(f, line, fmt=' %d ')
f.close()




Mat6 = range(-7, 147, 1)
Mat6 = np.reshape(Mat6,(11,14), order='F') 

print ("\n\nThe next matrix is \n")
print(Mat6) 

mat6 = np.matrix(Mat6)
with open('MUhlar_mat6.txt', 'w+') as f:
    for line in mat6:
        np.savetxt(f, line, fmt=' %d ')
f.close()