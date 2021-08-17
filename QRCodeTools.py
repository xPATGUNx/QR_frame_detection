import glob
import os

import pyqrcode
import pyzbar.pyzbar as pyzbar
from PIL import Image
import numpy as np


def generate_qr_codes(frames):
    print('Beginning QR-Code generation...')
    leading_zeros = len(str(frames))
    format_str = '0' + str(leading_zeros) + 'd'
    for frame in range(frames):
        # print(frame)
        qr = pyqrcode.create(frame + 1)
        img_name = f'Images/QR_Code_Frame_{frame + 1:{format_str}}.png'
        qr.png(img_name, scale=5)
    print('QR-Codes have been generated for ' + str(frame + 1) + ' frames.')


def delete_generated_qr_codes():
    for filename in glob.glob('Images/*.png'):
        os.remove(filename)


def qr_code_scanner(frame: np.ndarray, return_position: bool = False):
    """
    A simple QR-Code scanner that can be used to either read the QR-Code or simply return its position.
    :param frame: numpy.ndarray`, `PIL.Image` or tuple (pixels, width, height)
    :param return_position: A boolean that toggles between the return of QR-Code data or its position.
    :return: Returns the encoded data from the QR-Code or its position in the frame.
    """
    if return_position:
        qr_code = pyzbar.decode(frame)
        for location in qr_code:
            (x, y, w, h) = location.rect
            return x, y, w, h
    else:
        qr_code = pyzbar.decode(frame)
        for code in qr_code:
            data = code.data.decode('utf-8')
            # print(data)
            return data


if __name__ == '__main__':
    generate_qr_codes(frames=5000)