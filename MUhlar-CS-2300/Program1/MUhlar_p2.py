# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 15:33:23 2018

@author: Matt
"""

import numpy as np

#menu option to allow the user to repeat the selection and addition of matrices as many times as they'd like
menu = int(input("Please select an option \n1)Add two matrices \n2)Exit program \n"))
while menu != 2:
    
    #gets the first file name and the number following the file name
    inputMat1 = input("Enter filename: ")
    matNum1 = input("What is the mat's number:")
    #gets the second file name and the number following it
    inputMat2 = input("Enter the second filename: ")
    matNum2 = input("What is the second mat's number:")
    
    #reads the text in as matrices and sets them to variables
    loadMat1 = np.loadtxt(inputMat1)
    loadMat2 = np.loadtxt(inputMat2)
    #sets the name for the new file
    newMatName = ("Muhlar_mat" + matNum1 + matNum2 + ".txt")
    
    #prints the first matrix
    print ("\n\nThe first matrix is \n")
    print (loadMat1)
    #prints the second matrix
    print ("\n\nThe second matrix is \n")
    print (loadMat2)
    #checks to see if the matrices can be added
    if loadMat1.shape == loadMat2.shape:
        #if they can it adds them and sets them to a variable
        loadMat3 = np.add(loadMat1, loadMat2)
        #it then prints the matrix
        print("\n\nThe new matrix is \n")
        print (loadMat3)
        #writes new matrix to a file with new file name
        with open(newMatName, 'w+') as f:
            for line in loadMat3:
                np.savetxt(f, line, fmt=' %d ')
        f.close()
    #if they can't be added it prints an error statement
    else:
        print ("\n\nThese matrices have different shapes and cannot be added.")
        #prompts the menu again to give the user the option to repeat or exit
    menu = int(input("\n\nPlease select an option \n1)Add two matrices \n2)Exit program \n"))
    
#reads in all of the files and saves them to variables  
mat1 = np.loadtxt('Muhlar_mat1.txt')

mat2 = np.loadtxt('Muhlar_mat2.txt')

mat3 = np.loadtxt('Muhlar_mat3.txt')

mat4 = np.loadtxt('Muhlar_mat4.txt')

mat5 = np.loadtxt('Muhlar_mat5.txt')

mat6 = np.loadtxt('Muhlar_mat6.txt')


#Adds the 1st mat with each of the others
#prints out the first matrix
print ("The first matrix is \n")
print (mat1)
#prints out the second matrix
print ("\n\nThe second matrix is \n")
print (mat1)
#checks to see if the matrices can be added
if mat1.shape == mat1.shape:
    #if they can it adds them together
    loadMat3 = np.add(mat1, mat1)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    #it then writes a file with the new matrix
    with open('Muhlar_mat11.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    #if they can't be added it prints an error message
    print ("\n\nThese matrices have different shapes and cannot be added.")
    
    

print ("\n\nThe first matrix is \n")
print (mat1)
print ("\n\nThe second matrix is \n")
print (mat2)
if mat1.shape == mat2.shape:
    loadMat3 = np.add(mat1, mat2)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat12.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat1)
print ("\n\nThe second matrix is \n")
print (mat3)
if mat1.shape == mat3.shape:
    loadMat3 = np.add(mat1, mat3)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat13.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat1)
print ("\n\nThe second matrix is \n")
print (mat4)
if mat1.shape == mat4.shape:
    loadMat3 = np.add(mat1, mat4)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat14.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat1)
print ("\n\nThe second matrix is \n")
print (mat5)
if mat1.shape == mat5.shape:
    loadMat3 = np.add(mat1, mat5)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat15.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat1)
print ("\n\nThe second matrix is \n")
print (mat6)
if mat1.shape == mat6.shape:
    loadMat3 = np.add(mat1, mat6)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat16.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



#Adds the 2nd mat with each of the others
print ("The first matrix is \n")
print (mat2)
print ("\n\nThe second matrix is \n")
print (mat1)
if mat2.shape == mat1.shape:
    loadMat3 = np.add(mat2, mat1)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat21.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")
    
    

print ("\n\nThe first matrix is \n")
print (mat2)
print ("\n\nThe second matrix is \n")
print (mat2)
if mat2.shape == mat2.shape:
    loadMat3 = np.add(mat2, mat2)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat22.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat2)
print ("\n\nThe second matrix is \n")
print (mat3)
if mat2.shape == mat3.shape:
    loadMat3 = np.add(mat2, mat3)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat23.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat2)
print ("\n\nThe second matrix is \n")
print (mat4)
if mat2.shape == mat4.shape:
    loadMat3 = np.add(mat2, mat4)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat24.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat2)
print ("\n\nThe second matrix is \n")
print (mat5)
if mat2.shape == mat5.shape:
    loadMat3 = np.add(mat2, mat5)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat25.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat2)
print ("\n\nThe second matrix is \n")
print (mat6)
if mat2.shape == mat6.shape:
    loadMat3 = np.add(mat2, mat6)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat26.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



#Adds the 3rd mat with each of the others
print ("The first matrix is \n")
print (mat3)
print ("\n\nThe second matrix is \n")
print (mat1)
if mat3.shape == mat1.shape:
    loadMat3 = np.add(mat3, mat1)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat31.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")
    
    

print ("\n\nThe first matrix is \n")
print (mat3)
print ("\n\nThe second matrix is \n")
print (mat2)
if mat3.shape == mat2.shape:
    loadMat3 = np.add(mat3, mat2)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat32.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat3)
print ("\n\nThe second matrix is \n")
print (mat3)
if mat3.shape == mat3.shape:
    loadMat3 = np.add(mat3, mat3)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat33.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat3)
print ("\n\nThe second matrix is \n")
print (mat4)
if mat3.shape == mat4.shape:
    loadMat3 = np.add(mat3, mat4)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat34.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat3)
print ("\n\nThe second matrix is \n")
print (mat5)
if mat3.shape == mat5.shape:
    loadMat3 = np.add(mat3, mat5)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat35.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat3)
print ("\n\nThe second matrix is \n")
print (mat6)
if mat3.shape == mat6.shape:
    loadMat3 = np.add(mat3, mat6)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat36.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



#Adds the 4th mat with each of the others
print ("The first matrix is \n")
print (mat4)
print ("\n\nThe second matrix is \n")
print (mat1)
if mat4.shape == mat1.shape:
    loadMat3 = np.add(mat4, mat1)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat41.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")
    
    

print ("\n\nThe first matrix is \n")
print (mat4)
print ("\n\nThe second matrix is \n")
print (mat2)
if mat4.shape == mat2.shape:
    loadMat3 = np.add(mat4, mat2)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat42.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat4)
print ("\n\nThe second matrix is \n")
print (mat3)
if mat4.shape == mat3.shape:
    loadMat3 = np.add(mat4, mat3)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat43.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat4)
print ("\n\nThe second matrix is \n")
print (mat4)
if mat4.shape == mat4.shape:
    loadMat3 = np.add(mat4, mat4)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat44.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat4)
print ("\n\nThe second matrix is \n")
print (mat5)
if mat4.shape == mat5.shape:
    loadMat3 = np.add(mat4, mat5)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat45.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat4)
print ("\n\nThe second matrix is \n")
print (mat6)
if mat4.shape == mat6.shape:
    loadMat3 = np.add(mat4, mat6)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat46.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



#Adds the 5th mat with each of the others
print ("The first matrix is \n")
print (mat5)
print ("\n\nThe second matrix is \n")
print (mat1)
if mat5.shape == mat1.shape:
    loadMat3 = np.add(mat5, mat1)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat51.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")
    
    

print ("\n\nThe first matrix is \n")
print (mat5)
print ("\n\nThe second matrix is \n")
print (mat2)
if mat5.shape == mat2.shape:
    loadMat3 = np.add(mat5, mat2)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat52.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat5)
print ("\n\nThe second matrix is \n")
print (mat3)
if mat5.shape == mat3.shape:
    loadMat3 = np.add(mat5, mat3)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat53.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat5)
print ("\n\nThe second matrix is \n")
print (mat4)
if mat5.shape == mat4.shape:
    loadMat3 = np.add(mat5, mat4)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat54.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat5)
print ("\n\nThe second matrix is \n")
print (mat5)
if mat5.shape == mat5.shape:
    loadMat3 = np.add(mat5, mat5)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat55.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat5)
print ("\n\nThe second matrix is \n")
print (mat6)
if mat5.shape == mat6.shape:
    loadMat3 = np.add(mat5, mat6)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat56.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



#Adds the 6th mat with each of the others
print ("The first matrix is \n")
print (mat6)
print ("\n\nThe second matrix is \n")
print (mat1)
if mat6.shape == mat1.shape:
    loadMat3 = np.add(mat6, mat1)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat61.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")
    
    

print ("\n\nThe first matrix is \n")
print (mat6)
print ("\n\nThe second matrix is \n")
print (mat2)
if mat6.shape == mat2.shape:
    loadMat3 = np.add(mat6, mat2)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat62.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat6)
print ("\n\nThe second matrix is \n")
print (mat3)
if mat6.shape == mat3.shape:
    loadMat3 = np.add(mat6, mat3)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat63.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat6)
print ("\n\nThe second matrix is \n")
print (mat4)
if mat6.shape == mat4.shape:
    loadMat3 = np.add(mat6, mat4)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat64.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat6)
print ("\n\nThe second matrix is \n")
print (mat5)
if mat6.shape == mat5.shape:
    loadMat3 = np.add(mat6, mat5)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat65.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")



print ("\n\nThe first matrix is \n")
print (mat6)
print ("\n\nThe second matrix is \n")
print (mat6)
if mat6.shape == mat6.shape:
    loadMat3 = np.add(mat6, mat6)
    print("\n\nThe new matrix is \n")
    print (loadMat3)
    with open('Muhlar_mat66.txt', 'w+') as f:
        for line in loadMat3:
            np.savetxt(f, line, fmt=' %d ')
    f.close()
else:
    print ("\n\nThese matrices have different shapes and cannot be added.")
