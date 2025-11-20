import numpy as np
import cv2

def composite_images(google_img, capture_img):
    g_hight, g_width, g_channel = google_img.shape
    c_hight, c_width, c_channel = capture_img.shape
    print(google_img.shape)
    print(capture_img.shape)

    for x in range(g_width):
        for y in range(g_hight):
            g, b, r = google_img[y, x]
            # もし白色(255,255,255)だったら置き換える
            if (b, g, r) == (255, 255, 255):
                yy = y % c_hight
                xx = x % c_width
                google_img[y, x] = capture_img[yy, xx]
    
    result_img = google_img
    return result_img   

    