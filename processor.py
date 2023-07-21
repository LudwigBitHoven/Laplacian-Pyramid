from math import pi, e
import numpy as np
from skimage.io import imread, imshow
from skimage import img_as_float
from scipy.signal import convolve2d
from numpy.fft import fft2, fftshift

class ImgProcessor():
    def __init__(self):
        self.sigma = 0.33
        self.n_layers = 4

    def set_params(self, sigma, n_layers):
        if sigma and n_layers:
            self.sigma = float(sigma)
            self.n_layers = int(n_layers)
        else:
            self.sigma = 0.33
            self.n_layers = 4

    def conv(self, img, kernel):
        r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        r2, g2, b2 = convolve2d(r, kernel, mode='same'), convolve2d(g, kernel, mode='same'), convolve2d(b, kernel, mode='same')
        result = np.dstack((r2, g2, b2))
        return result

    def gauss(self, x, y, sigma):
        return (1 / ((2 * pi) * sigma**2) * e**((- x**2 - y**2) / (2 * sigma**2)))

    def gauss_pyramid(self, img):
        result = []
        k = int(round(6 * self.sigma + 1))
        core = np.array([[self.gauss(x, y, self.sigma) for x in range(-k, k + 1)] for y in range(-k, k + 1)])
        kernel = core / np.sum(core, axis=(0, 1))
        for i in range(self.n_layers):
            img = self.conv(img, kernel)
            img = np.clip(img, 0, 1)
            result.append(img)
        return np.array(result)

    def lap_pyramid(self, img):
        g_img = [img[:, :, :3]]
        g = self.gauss_pyramid(img)
        result = []
        for i in range(self.n_layers):
            g_img.append(g[i])
            pic = g_img[i] - g_img[i + 1]
            result.append(pic)
        result.append(g_img[-1])
        result = np.array(result)
        return result

    def open_img(self, path):
        img = imread(path)
        img = img_as_float(img)
        return img

    def img_to_byte(self, img_lst):
        result = []
        for i in img_lst:
            temp = (i * 255).astype(np.uint8)
            result.append(temp)
        return result


