#!/usr/bin/env python
################################################################################
#                                                                              #
#                                 Matrix Class                                 #
#                                                                              #
################################################################################
#
#

import math

class Matrix():

    def __init__(self, rows, columns):

        self.rows    = rows
        self.columns = columns
        self.element = []

        for i in range(0, self.rows):

            self.element.append([])

            for j in range(0, self.columns):

                self.element[i].append(0)


    def load(self, numarray):

        for i in range(0, self.rows):

            for j in range(0, self.columns):

                self.element[i][j] = numarray[i][j]

        return self


    def copy(self, Matrix1):

        self.rows    = Matrix1.rows
        self.columns = Matrix1.columns

        for i in range(0, self.rows):

            for j in range(0, self.columns):

                self.element[i][j] = Matrix1.getelement(i,j)

        return self



    def getelement(self, i, j):

        return self.element[i][j]

    def getcolumn(self,j):

        row = []

        for i in range (0, self.columns + 1):

            row.append(self.getelement(i, j))

        return row

    def getrow(self,i):

        column = []

        for j in range (0, self.rows + 1):

            column.append(self.getelement(i, j))

        return column



    def add(self, Matrix1):

        for i in range(0, self.rows):

            for j in range(0, self.columns):

                self.element[i][j] = self.getelement(i,j) + Matrix1.getelement(i,j)

        return self



    def transpose(self):

        newarray = []


        for i in range(0, self.columns):

            newarray.append([])

            for j in range(0, self.rows):

                newarray[i].append(self.element[j][i])

        self.load(newarray)

        return self



    def sub(self, Matrix1):

        temp = Matrix(Matrix1.rows, Matrix1.columns)

        temp.copy(Matrix1)

        temp.multiply(-1)

        self.add(temp)

        del temp

        return self



    def multiply(self, factor):

        if type(factor) == Matrix or type(factor) == SqrMatrix or type(factor) == FourVector:

            self.__Matrixmultiply(factor)


        else:

            self.__scalemultiply(factor)

        return self



    def __Matrixmultiply(self, Matrix1):

        temp = Matrix(self.rows, Matrix1.columns)

        for i in range(0, self.rows):

            for j in range(0, Matrix1.columns):

                eval = 0

                for k in range(0, self.columns):

                    eval = eval + self.getelement(i,k) * Matrix1.getelement(k,j)

                temp.element[i][j] = eval

        self.copy(temp)

        del temp

        return self



    def __scalemultiply(self,factor):

        for i in range(0, self.rows):

            for j in range(0, self.columns):

                self.element[i][j] = self.getelement(i,j) * factor

        return self



    def __str__(self):

        string = ""

        for i in range(0, self.rows):

            for j in range(0, self.columns):

                string = string + str(self.element[i][j]) + "\t"

            string = string + "\n"

        return string






class SqrMatrix(Matrix):

    def __init__(self, order):

        Matrix.__init__(self,order, order)

        self.order = order


    def det(self):

        if self.order ==1:

            determinant = self.getelement(0,0)

        else:

            determinant = 0

            for i in range(0, self.columns):

                sign = (-1) ** i

                val  = self.getelement(0, i)

                subarray=[]

                for j in range(1, self.rows):

                    subarray.append([])

                    for k in range(0, self.columns):

                        if k != i :

                            subarray[j-1].append(self.getelement(j, k))

                subMatrix = SqrMatrix(self.columns - 1)

                subMatrix.load(subarray)


                determinant = determinant + sign * val * subMatrix.det()

                del subMatrix

                del subarray

        return determinant



    def inverse(self):

        z = 1 / self.det()

        self.cofactor().transpose().multiply(z)

        return self





    def cofactor(self):

        temp = SqrMatrix(self.order)

        for i in range(0, self.rows):

            for j in range(0, self.columns):

                sign = (-1)**i * (-1)**j

                subarray=[]

                for k in range(0, self.rows):

                    if k != i:

                        subarray.append([])

                        for l in range(0, self.columns):

                            if l != j :

                                subarray[len(subarray) - 1].append(self.getelement(k, l))

                subMatrix = SqrMatrix(self.columns - 1)

                subMatrix.load(subarray)

                temp.element[i][j] = sign * subMatrix.det()

                del subMatrix

                del subarray

        self.copy(temp)

        del temp

        return self



class LambdaMatrix(Matrix):

    def __init__(self, rows, columns):

        self.rows    = rows
        self.columns = columns

        Matrix.__init__(self, self.rows, self.columns)


    def setMatrix(self, *args):

        if self.rows == self.columns:

            temp = SqrMatrix(self.rows)

        else:

            temp = Matrix(self.rows, self.columns)


        for i in range(0, self.rows):

            for j in range(0, self.columns):

                temp.element[i][j] = self.getelement(i,j)(*args)

        return temp


class FourVector(Matrix):

    def __init__(self):

        Matrix.__init__(self,4, 1)

        self.load([[0], [0], [0], [1]])


    def scalarproduct(self, vector):

        scalar = (self.getelement(0,0) * vector.getelement(0,0) +
                  self.getelement(1,0) * vector.getelement(1,0) +
                  self.getelement(2,0) * vector.getelement(2,0) )

        return scalar



    def vectorproduct(self, vector):

        x = self.getelement(1,0) * vector.getelement(2,0) - self.getelement(2,0) * vector.getelement(1,0)

        y = self.getelement(2,0) * vector.getelement(0,0) - self.getelement(0,0) * vector.getelement(2,0)

        z = self.getelement(0,0) * vector.getelement(1,0) - self.getelement(1,0) * vector.getelement(0,0)

        self.load([[x], [y], [z], [1]])

        return self

    def magnitude(self):

        mag = math.sqrt(self.getelement(0,0)**2 + self.getelement(1,0)**2 + self.getelement(2,0)**2)

        return mag

    def normalise(self):

        mag = self.magnitude()

        if mag >0:

            x = self.getelement(0,0)/mag
            y = self.getelement(1,0)/mag
            z = self.getelement(2,0)/mag

            self.load([[x], [y], [z], [1]])

        return self

    def threevector(self):

        x = self.getelement(0,0)
        y = self.getelement(1,0)

        return Matrix(3,1).load([[x], [y], [1]])


    def __str__(self):

        string = "( "

        for i in range(0, self.rows):

            string = string + "%3.1f" % (self.element[i][0]) + ", "

        string = string + ")"

        return string


