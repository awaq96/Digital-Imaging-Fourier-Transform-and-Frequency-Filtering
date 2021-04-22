# For this part of the assignment, please implement your own code for all computations,
# Do not use inbuilt functions like fft from either numpy, opencv or other libraries
import numpy as np
import math
class DFT:

    def forward_transform(self, matrix):
        """Computes the forward Fourier transform of the input matrix
        takes as input:
        matrix: a 2d matrix
        returns a complex matrix representing fourier transform"""
        complex_matrix = np.zeros((len(matrix), len(matrix[0])), dtype=complex)
        points = []
        j_points = []

        for j in range(0, len(matrix[0])-1):
            j_points.append(j)
        for i in range(0, len(matrix)-1):
            for j in j_points:
                points.append([i, j])

        for u in range(0, len(complex_matrix)):
            for v in range(0, len(complex_matrix[0])):
                summation = 0 + 0j
                for I in points:
                    i = I[0]
                    k = I[1]
                    complex_root = -1j
                    exponent = complex_root*(2*math.pi/len(matrix))*(u*i+v*k)
                    summation += matrix[i,k] * pow(math.e, exponent)
                complex_matrix[u, v] = summation
        return complex_matrix

    def inverse_transform(self, matrix):
        """Computes the inverse Fourier transform of the input matrix
        matrix: a 2d matrix (DFT) usually complex
        takes as input:
        returns a complex matrix representing the inverse fourier transform"""
        inverse_matrix = np.zeros((len(matrix), len(matrix[0])), dtype=complex)
        v_points = []
        for v in range(0, len(matrix[0])):
            v_points.append(v)
        points = []
        for u in range(0, len(matrix)):
            for v in v_points:
                points.append([u, v])
        for i in range(len(inverse_matrix)):
            for k in range(len(inverse_matrix[0])):
                summation = 0
                for F in points:
                    u = F[0]
                    v = F[1]
                    complex_root = 1j
                    exponent = complex_root * ((2*math.pi) / len(matrix)) * (u*i+v*k)
                    summation += matrix[u, v] * exponent
                inverse_matrix[i, k] = summation

        return inverse_matrix


    def discrete_cosine_tranform(self, matrix):
        """Computes the discrete cosine transform of the input matrix
        takes as input:
        matrix: a 2d matrix
        returns a matrix representing discrete cosine transform"""
        cos_matrix = np.zeros((len(matrix), len(matrix[0])))

        points = []
        j_points = []

        for j in range(0, len(matrix[0])):
            j_points.append(j)
        for i in range(0, len(matrix)):
            for j in j_points:
                points.append([i, j])

        for u in range(0, len(cos_matrix)):
            for v in range(0, len(cos_matrix[0])):
                summation = 0
                for I in points:
                    i = I[0]
                    j = I[1]
                    frac = (2*math.pi)/ len(matrix)
                    frac *= u*i + v*j
                    summation += matrix[i, j] * math.cos(frac)
                cos_matrix[u, v] = summation

        return cos_matrix


    def magnitude(self, matrix):
        """Computes the magnitude of the DFT
        takes as input:
        matrix: a 2d matrix
        returns a matrix representing magnitude of the dft"""
        mag_matrix = np.zeros((len(matrix), len(matrix[0])))
        j_points = []
        for j in range(0, len(matrix[0])):
            j_points.append(j)
        points = []
        for i in range(0,len(matrix)):
            for j in j_points:
                points.append([i, j])

        for u in range(0, len(mag_matrix)):
            for v in range(0, len(mag_matrix[0])):
                summation = complex(0,0)
                for I in points:
                    i = I[0]
                    k = I[1]
                    fraction = ((2 * math.pi)/len(matrix)) * (u*i + v*k)
                    cos_portion = math.cos(fraction)
                    complex_num = 1j
                    sin_portion = math.sin(fraction) * complex_num
                    summation += matrix[i, k] * (cos_portion - sin_portion)
                magnitude = math.sqrt(pow(summation.real, 2) + pow(summation.imag, 2))
                mag_matrix[u, v] = magnitude
        return mag_matrix
