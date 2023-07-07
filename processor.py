from math import pi, e
import numpy as np
from skimage.io import imread, imshow
from skimage import img_as_float
from scipy.signal import convolve2d
from numpy.fft import fft2, fftshift

class ImgProcessor():
    def __init__(self):
        pass

    def conv(self, img, kernel):
        r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        r2, g2, b2 = convolve2d(r, kernel, mode='same'), convolve2d(g, kernel, mode='same'), convolve2d(b, kernel, mode='same')
        result = np.dstack((r2, g2, b2))
        return result

    def gauss(self, x, y, sigma):
        return (1 / ((2 * pi) * sigma**2) * e**((- x**2 - y**2) / (2 * sigma**2)))

    def gauss_pyramid(self, img, sigma, n_layers):
        result = []
        k = int(round(6 * sigma + 1))
        core = np.array([[gauss(x, y, sigma) for x in range(-k, k + 1)] for y in range(-k, k + 1)])
        kernel = core / np.sum(core, axis=(0, 1))
        for i in range(n_layers):
            img = conv(img, kernel)
            img = np.clip(img, 0, 1)
            result.append(img)
        return np.array(result)

    def show_gauss(self, img, sigma, n_layers):
      fig, ax = plt.subplots(n_layers, 2, figsize=(20, 30))
      for i in range(n_layers):
        # ax[i][0].imshow(img[i])
        freq = get_freq(img[i])
        # ax[i][1].imshow(freq, cmap='gray')

    def lap_pyramid(self, img, sigma, n_layers):
        g_img = [img]
        g = gauss_pyramid(img, sigma, n_layers)
        result = []
        for i in range(n_layers):
            g_img.append(g[i])
            pic = g_img[i] - g_img[i + 1]
            result.append(pic)
        result.append(g_img[-1])
        result = np.array(result)
        return result

    def show_laplas(self, img, sigma, n_layers):
        fig, ax = plt.subplots(n_layers - 1, 2, figsize=(20, 30))
        for i in range(1, n_layers):
          # ax[i - 1][0].imshow(np.clip(30 * img[i], 0, 1))
          freq = get_freq(img[i-1])
          freq2 = get_freq(img[i])
          # ax[i - 1][1].imshow(freq - freq2, cmap='gray')

    def get_freq(self, img):
        r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        Y = 0.299 * r + 0.587 * g + 0.114 * b
        freq = 20 * np.log(1 + abs(fftshift(fft2(Y))))
        return freq
