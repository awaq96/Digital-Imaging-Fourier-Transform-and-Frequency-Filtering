# For this part of the assignment, You can use inbuilt functions to compute the fourier transform
# You are welcome to use fft that are available in numpy and opencv

import numpy as np
import math

class Filtering:

    def __init__(self, image, filter_name, cutoff, order = 0):
        """initializes the variables frequency filtering on an input image
        takes as input:
        image: the input image
        filter_name: the name of the mask to use
        cutoff: the cutoff frequency of the filter
        order: the order of the filter (only for butterworth
        returns"""
        self.image = image
        if filter_name == 'ideal_l':
            self.filter = self.get_ideal_low_pass_filter
        elif filter_name == 'ideal_h':
            self.filter = self.get_ideal_high_pass_filter
        elif filter_name == 'butterworth_l':
            self.filter = self.get_butterworth_low_pass_filter
        elif filter_name == 'butterworth_h':
            self.filter = self.get_butterworth_high_pass_filter
        elif filter_name == 'gaussian_l':
            self.filter = self.get_gaussian_low_pass_filter
        elif filter_name == 'gaussian_h':
            self.filter = self.get_gaussian_high_pass_filter

        self.cutoff = cutoff
        self.order = order


    def get_ideal_low_pass_filter(self, shape, cutoff):
        """Computes a Ideal low pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the ideal filter
        returns a ideal low pass mask"""
        low_pass = np.zeros(shape)
        for u in range(0, shape[0]):
            for v in range(0, shape[1]):
                P = pow((u - (shape[0]/2)), 2)
                Q = pow((v - (shape[1]/2)), 2)

                Duv = math.sqrt(P + Q)
                if Duv <= cutoff:
                    low_pass[u, v] = 1
                else:
                    low_pass[u, v] = 0

        return low_pass

    def get_ideal_high_pass_filter(self, shape, cutoff):
        """Computes a Ideal high pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the ideal filter
        returns a ideal high pass mask"""
        lowpass = self.get_ideal_low_pass_filter(shape, cutoff)
        highpass = np.zeros(shape)
        for u in range(0, shape[0]):
            for v in range(0, shape[1]):
                highpass[u, v] = 1 - lowpass[u, v]


        #Hint: May be one can use the low pass filter function to get a high pass mask

        return highpass

    def get_butterworth_low_pass_filter(self, shape, cutoff, order):
        """Computes a butterworth low pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the butterworth filter
        order: the order of the butterworth filter
        returns a butterworth low pass mask"""
        blpf = np.zeros(shape)

        for u in range(0, shape[0]):
            for v in range(0, shape[1]):
                P = pow((u - (shape[0]/2)), 2)
                Q = pow((v - (shape[1]/2)), 2)

                Duv = math.sqrt(P + Q)

                blpf[u, v] = 1/ (1 + pow((Duv/cutoff), 2 * order))


        return blpf

    def get_butterworth_high_pass_filter(self, shape, cutoff, order):
        """Computes a butterworth high pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the butterworth filter
        order: the order of the butterworth filter
        returns a butterworth high pass mask"""
        lowpassblpf = self.get_butterworth_low_pass_filter(shape, cutoff, order)
        highpassblpf = np.zeros(shape)

        for u in range(0, shape[0]):
            for v in range(0, shape[1]):
                highpassblpf[u, v] = 1 - lowpassblpf[u, v]

        #Hint: May be one can use the low pass filter function to get a high pass mask

        return 0

    def get_gaussian_low_pass_filter(self, shape, cutoff):
        """Computes a gaussian low pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the gaussian filter (sigma)
        returns a gaussian low pass mask"""
        lowpassG = np.zeros(shape)

        for u in range(0, shape[0]):
            for v in range(0, shape[1]):
                P = pow((u - (shape[0]/2)), 2)
                Q = pow((v - (shape[1]/2)), 2)

                Duv = math.sqrt(P + Q)

                exponent = -1 * pow(Duv, 2) / (2 * pow(cutoff, 2))
                lowpassG[u, v] = pow(math.e, exponent)
        return lowpassG

    def get_gaussian_high_pass_filter(self, shape, cutoff):
        """Computes a gaussian high pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the gaussian filter (sigma)
        returns a gaussian high pass mask"""
        lowpass = self.get_gaussian_low_pass_filter(shape, cutoff)
        highpassG = np.zeros(shape)
        for u in range(0, shape[0]):
            for v in range(0, shape[1]):
                highpassG[u, v] = 1 - lowpass[u, v]
        #Hint: May be one can use the low pass filter function to get a high pass mask

        return highpassG

    def post_process_image(self, image):
        """Post process the image to create a full contrast stretch of the image
        takes as input:
        image: the image obtained from the inverse fourier transform
        return an image with full contrast stretch
        -----------------------------------------------------
        1. Full contrast stretch (fsimage)
        2. take negative (255 - fsimage) (Only if needed)
        """
        a = 0 # lower limit
        b = 255 # upper limit
        c = 255 # lowest pixel value in image
        d = 0 # largest pixel value in image
        # Find c and d value
        for x in range(len(image)):
            for y in range(len(image[0])):
                if image[x, y] < c:
                    c = image[x, y]
                if image[x, y] > d:
                    d = image[x, y]

        for x in range(len(image)):
            for y in range(len(image[0])):
                image[x, y] = ((image[x, y] -c) * ((b-a) / (d-c))) + a

        return image

    def filtering(self):
        """Performs frequency filtering on an input image
        returns a filtered image, magnitude of DFT, magnitude of filtered DFT
        ----------------------------------------------------------
        You are allowed to used inbuilt functions to compute fft
        There are packages available in numpy as well as in opencv
        Steps:
        1. Compute the fft of the image
        2. shift the fft to center the low frequencies
        3. get the mask (write your code in functions provided above) the functions can be called by self.filter(shape, cutoff, order)
        4. filter the image frequency based on the mask (Convolution theorem)
        5. compute the inverse shift
        6. compute the inverse fourier transform
        7. compute the magnitude
        8. You will need to do a full contrast stretch on the magnitude and depending on the algorithm you may also need to
        take negative of the image to be able to view it (use post_process_image to write this code)
        Note: You do not have to do zero padding as discussed in class, the inbuilt functions takes care of that
        filtered image, magnitude of DFT, magnitude of filtered DFT: Make sure all images being returned have grey scale full contrast stretch and dtype=uint8
        """
        # Convert to freq domain
        fft_image = np.fft.fft2(self.image)
        np.fft.fftshift(fft_image)
        shape = (len(self.image), len(self.image[0]))
        # Get filter mask
        mask = self.filter(shape, self.cutoff)

        magnitude_Dft = np.zeros(shape, dtype=np.uint8)
        for u in range(len(fft_image)):
            for v in range(len(fft_image[0])):
                magnitude_Dft[u, v] = math.sqrt((pow(fft_image[u, v].real, 2)) + pow(fft_image[u, v].imag, 2))

        # Convolution
        convoluted_img = np.zeros(shape, dtype=np.uint8)
        for u in range(shape[0]):
            for v in range(shape[1]):
                convoluted_img[u, v] = fft_image[u,v] * mask[u,v]

        # Inverse conversion
        np.fft.ifftshift(convoluted_img)
        filtered_image = np.fft.ifft2(convoluted_img)
        filtered_image_asInt = np.zeros(shape, dtype=np.uint8)
        filtered_image_asInt[:] = filtered_image

        # magnitude of filtered dft
        magnitude_filtered_DFT = np.zeros(shape, dtype=np.int8)

        for i in range(len(magnitude_filtered_DFT)):
            for j in range(len(magnitude_filtered_DFT[0])):
                magnitude_filtered_DFT[i, j] = math.sqrt(pow(filtered_image[i, j].real, 2) + pow(filtered_image[i, j], 2))

        magnitude_filtered_DFT = self.post_process_image(magnitude_filtered_DFT)


        return [filtered_image_asInt, magnitude_Dft, magnitude_filtered_DFT]
