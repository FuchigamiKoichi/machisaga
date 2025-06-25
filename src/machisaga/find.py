import numpy as np
import cv2

img1 = cv2.imread('./images/data1.png')
img2 = cv2.imread('./images/data2.png')

def findDifference(img1, img2, v, h, t):
    h1,w1 = img1.shape[:2]
    h2,w2 = img2.shape[:2]

    results = []

    if h1 < h2:
        d = h2 - h1
        img2 = img2[:-d,:]
    elif h1 != h2:
        d = h1 - h2
        img1 = img1[:-d,:]
        
    if w1 < w2:
        d = w2 - w1
        img2 = img2[:,:w2-d]
    elif w1 != w2:
        d = w1 - w2
        img1 = img1[:,:w1-d]

    result = cv2.absdiff(img1,img2)
        
    for i in range(int(min([w1,w2])*h)):
        i += 1
        img1_data = img1[:,i:]
        img2_data = img2[:,:-i]
        cap = cv2.absdiff(img1_data,img2_data)
        if np.sum(cap)/np.size(cap) < np.sum(result)/np.size(result):
            result = cap
        for j in range(int(min([h1,h2])*v)):
            j += 1
            img1_d = img1_data[j:,:]
            img2_d = img2_data[:-j,:]
            cap = cv2.absdiff(img1_d,img2_d)
            if np.sum(cap)/np.size(cap) < np.sum(result)/np.size(result):
                result = cap

    for i in range(int(min([w1,w2])*h)):
        i += 1
        img1_data = img1[:,i:]
        img2_data = img2[:,:-i]
        cap = cv2.absdiff(img1_data,img2_data)
        if np.sum(cap)/np.size(cap) < np.sum(result)/np.size(result):
            result = cap
        for j in range(int(min([h1,h2])*v)):
            j += 1
            img1_d = img1_data[:-j,:]
            img2_d = img2_data[j:,:]
            cap = cv2.absdiff(img1_d,img2_d)
            if np.sum(cap)/np.size(cap) < np.sum(result)/np.size(result):
                result = cap

    for i in range(int(min([w1,w2])*h)):
        i += 1
        img1_data = img1[:,:-i]
        img2_data = img2[:,i:]
        cap = cv2.absdiff(img1_data,img2_data)
        if np.sum(cap)/np.size(cap) < np.sum(result)/np.size(result):
            result = cap
        for j in range(int(min([h1,h2])*v)):
            j += 1
            img1_d = img1_data[:-j,:]
            img2_d = img2_data[j:,:]
            cap = cv2.absdiff(img1_d,img2_d)
            if np.sum(cap)/np.size(cap) < np.sum(result)/np.size(result):
                result = cap

    for i in range(int(min([w1,w2])*h)):
        i += 1
        img1_data = img1[:,:-i]
        img2_data = img2[:,i:]
        cap = cv2.absdiff(img1_data,img2_data)
        if np.sum(cap)/np.size(cap) < np.sum(result)/np.size(result):
            result = cap
        for j in range(int(min([h1,h2])*v)):
            j += 1
            img1_d = img1_data[j:,:]
            img2_d = img2_data[:-j,:]
            cap = cv2.absdiff(img1_d,img2_d)
            if np.sum(cap)/np.size(cap) < np.sum(result)/np.size(result):
                result = cap

    result_show = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    ret, result_show = cv2.threshold(result_show, t, 255, cv2.THRESH_BINARY)
    return result_show