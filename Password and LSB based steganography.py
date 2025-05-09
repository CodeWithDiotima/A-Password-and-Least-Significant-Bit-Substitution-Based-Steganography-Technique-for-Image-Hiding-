# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 15:07:26 2023

@author: Diotima
"""

import numpy as np
import cv2
from PIL import Image

cover=cv2.imread(r"C:\Users\Diotima\Documents\1.png")
secret=cv2.imread(r"C:\Users\Diotima\Documents\t1.jpg")
#cover=np.ones((128,64,3),dtype=np.uint8)*255
#secret=np.zeros((2,2,3),dtype=np.uint8)
cv2.imwrite("secret.jpg",secret)
secret1=Image.open("secret.jpg")

cv2.imshow("Cover",cover)
cv2.waitKey(0)

pwd=str(input("Enter password of 8 character: "))
if(len(pwd)!=8):
    print("Please Enter password containing only 8 character")
    exit(0)

bin_val=[]
for symbol in pwd:
    bin_val.append(np.binary_repr(ord(symbol),width=8))
#print(bin_val)

bin_key1=""
for i in range(len(bin_val)):
    for j in range(len(bin_val[i])):
        if i==j:
            bin_key1+=bin_val[i][j]
key1=int(bin_key1,2)
#print(key1)

bin_key2=""
for i in range((len(bin_val)-1),-1,-1):
    for j in range(len(bin_val[i])):
        if j==((len(bin_val)-1)-i):
            bin_key2+=bin_val[j][i]
key2=int(bin_key2,2)
#print(key2)

tot_rem_pxl=(cover.shape[1]*(cover.shape[0]-key1-1))+(cover.shape[1]-key2)
req_pxl=8*secret.shape[0]*secret.shape[1]

if(tot_rem_pxl<req_pxl or key1>cover.shape[0] or key2>cover.shape[1]):
    print("Steganography is not possible. Recommended minimum size of secret image need to be 255*255 or try with bigger cover image")
else:
    for k in range(3):
      x,y=key1,key2
      #count=0
      for i in range(secret.shape[0]):
          for j in range(secret.shape[1]):
              binary_s=np.binary_repr(secret[i][j][k],width=8)
              for l in range(8):
                if(x<cover.shape[0] and y<cover.shape[1]):
                  binary_c=np.binary_repr(cover[x][y][k],width=8)
                  x1,y1,k1=x,y,k
                  y=y+1
                  #count+=1
                elif(y>=cover.shape[1]):
                  x=x+1
                  y=0
                  #count+=1
                  binary_c=np.binary_repr(cover[x][y][k],width=8)
                  x1,y1,k1=x,y,k
                  y=y+1
                #print(binary_c[7],end=" ")
                c=[n for n in binary_c]
                s1=""
                c[7]=binary_s[l]
                s1=''.join([str(el) for el in c])
                cover[x1][y1][k1]=int(s1,2)
                #print(c[7])
                #print(count)
    cv2.imshow("Cover",cover)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    pixel=[]
    pixel_r=[]
    pixel_g=[]
    pixel_b=[]
    i=key1
    j=key2
    #count=0
    #print(x1,y1)
    while(j!=(y1+1) or i!=x1):
        r=""
        g=""
        b=""
        if (j<cover.shape[1]):
            r+=np.binary_repr(cover[i][j][0],width=8)
            g+=np.binary_repr(cover[i][j][1],width=8)
            b+=np.binary_repr(cover[i][j][2],width=8)
            j+=1
        else:
            i+=1
            j=0
            r+=np.binary_repr(cover[i][j][0],width=8)
            g+=np.binary_repr(cover[i][j][1],width=8)
            b+=np.binary_repr(cover[i][j][2],width=8)
            j+=1
        pixel_r.append(r[7])
        pixel_g.append(g[7])
        pixel_b.append(b[7])
        if(len(pixel_r)==8 and len(pixel_g)==8 and len(pixel_b)==8):
            rs=""
            rs=''.join([str(elem) for elem in pixel_r])
            gs=""
            gs=''.join([str(elem) for elem in pixel_g])
            bs=""
            bs=''.join([str(elem) for elem in pixel_b])
            pixel_r.clear()
            pixel_g.clear()
            pixel_b.clear()
            pixel.append(tuple([int(bs,2), int(gs,2), int(rs,2)]))
#print(pixel)
#print(count)
ret_img=Image.new(secret1.mode,secret1.size)
print(secret1.mode)
ret_img.putdata(pixel)
ret_img.save("ret_img.jpg")
#ret_img=np.array(pixel,dtype=np.uint8)
#cv2.imshow("Img",ret_img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
