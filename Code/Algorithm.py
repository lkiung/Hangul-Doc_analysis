# -*- coding: utf-8 -*-
"""
@author: Kiwoong Lee
"""

import math
import cv2
import numpy as np

# Function based C_means Clustering
def LUT2label(im,LUT):
    Imin = np.min(im)
    Imax = np.max(im)
    I =np.array(range(Imin,Imax+1))
    I = I.reshape([I.shape[0],1])
    L = np.zeros([im.shape[0],im.shape[1]],dtype=int)
    for k in range(np.max(LUT)+1):
        i = np.where(LUT==k)[0]
        i1 = int(i[0])
        
        if(i.size>1):
            i2=int(i[-1])
        else:
            i2=i1
        
        bw = np.where((im>I[i1]) & (im<I[i2]))
        for j in range(bw[0].size):
            L[bw[0][j],bw[1][j]] = k

    return L
 
# C_means Clustering    
def FastCmeans(im,c=2):
    Imin = np.min(im)
    Imax = np.max(im)
    I =np.array(range(Imin,Imax+1))
    I = I.reshape([I.shape[0],1])
    H = np.zeros([I.shape[0],1],dtype=int)
    k = im.shape[0]*im.shape[1]
    imshap =im.shape
    im = im.reshape([im.shape[0]*im.shape[1],1])
    for i in range(k):
        H[im[i]-Imin]=H[im[i]-Imin]+1 
        
    dl=(Imax-Imin)/c
    C=np.arange(Imin+dl/2,Imax,dl)
    IH = np.multiply(H,I)
    dC = float("inf")
    
    while(dC>1e-6):
        C0 =C
        D = np.ndarray([I.shape[0],0])
        for i in range(C.shape[0]):
            D = np.concatenate((D,np.subtract(I,C[i])),axis=1)
        
        D = np.abs(D)
        LUT = np.argmin(D,axis=1)
        C = np.double(C)
        for i in(range(c)):
            C[i]=np.sum(np.uint(IH[LUT==i]))/np.sum(np.uint(H[LUT==i]))
            
        dC = np.max(np.abs(np.subtract(C,C0))) 

    L =LUT2label(im,LUT)
    L = L.reshape(imshap)
    return L,C,LUT    

            
        

#load image    
#Options = dict(defaultextension = '.jpg',filetypes = [('Imag','*.jpg *.png *.bmp *.JPG *.PNG *.BMP *.TIF '),('All files','*.*')])
#file_path = tkF.askopenfilename(**Options)
#imag = cv2.imread(str(file_path.encode('euc-kr')),0) #?먮쾲夷?蹂?? color異뺤쓽 媛?닔
#
imag = cv2.imread("Test2.jpg",0)
imag = cv2.resize(imag,(imag.shape[1]/4,imag.shape[0]/4),interpolation=cv2.INTER_CUBIC)
rows,cols= imag.shape
imag = np.uint8(255*np.ones([rows,cols]) - imag)
#cv2.imshow('firstimag',imag)
#cv2.waitKey(0)


#[L,C,LUT] = FastCmeans(imag)
#onenum = np.where(L==1)[0].size
#zeronum = np.where(L==0)[0].size

#Assume Background pixels are many than foregraound pixels
#if(onenum > zeronum):
#    L = np.ones(L.shape)-L
#Cmeans =np.uint8(np.multiply(L,imag)) 


## we need function to binary image using SIS(simple image Statics)


###### making closing image###### 
kernel = np.ones((5,5),np.uint8)
closing = cv2.morphologyEx(imag,cv2.MORPH_CLOSE,kernel)


binaryimg = closing/255
imagesum = np.sum(binaryimg)/(float)(rows*cols)
stripwidth = 0
if(imagesum>=0.2):
    stripwidth = 0.05*cols
elif(imagesum>0.1):
    stripwidth = 0.1*cols
else:
    stripwidth = 0.25*cols

stripwidth = int(math.ceil(stripwidth))
proj = np.zeros([rows,int(math.ceil(cols/(float)(stripwidth)))])
rangemat = range(0,cols,stripwidth)
for i in range(0,cols/stripwidth):
    proj[:,i]=np.sum(closing[:,rangemat[i]:rangemat[i]+stripwidth-1],axis=1)    
    
proj[:,-1] = np.uint(np.sum(closing[:,rangemat[i+1]:],axis=1))

proj2 = np.zeros([proj.shape[0]+6,proj.shape[1]])
proj2[3:-3,:]= proj
for i in range(rows):
    proj[i,:] = np.sum(proj2[i-3:i+3,:],axis=0)
    
proj = proj/7
