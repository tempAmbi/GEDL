# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 17:52:02 2019

@author: 79060
"""

import tensorflow as tf
import numpy as np
from math import log10, floor
import hashlib
import matplotlib.pyplot as plt
import seaborn as sns
import input_data
mnist = input_data.read_data_sets("Mnist_data/", one_hot=True)
images = mnist.train.images

validNum = 16
m = hashlib.sha256()
reader = tf.train.NewCheckpointReader('save/model.ckpt')
reader1 = tf.train.NewCheckpointReader('save/model1.ckpt')
variables = reader.get_variable_to_shape_map()
variables1 = reader1.get_variable_to_shape_map()
k = 0
for ele in variables:
    if(k==0):
        tensor = reader.get_tensor(ele).reshape(1,-1)
        tensor1 = reader1.get_tensor(ele).reshape(1,-1)
    else:
        tensor = np.concatenate((tensor,reader.get_tensor(ele).reshape(1,-1)),axis=1)
        tensor1 = np.concatenate((tensor1,reader1.get_tensor(ele).reshape(1,-1)),axis=1)
    k = k+1
k = 0
    
shape = tensor.shape
s = 1
for i in shape:
    s = s*i
s = s-s%(28*28*5)
#resevered hash
rh = tensor[0,s:s+5]
rVector = str(int(rh[0]*10**(-int(floor(log10(abs(rh[0]))))+validNum-1)))
for i in range(1,5):
    rVector += str(int(rh[i]*10**(-int(floor(log10(abs(rh[i]))))+validNum-1)))
m.update(rVector.encode('utf-8'))
rh = m.hexdigest()

rh1 = tensor1[0,s:s+5]
rVector1 = str(int(rh1[0]*10**(-int(floor(log10(abs(rh1[0]))))+validNum-1)))
for i in range(1,5):
    rVector1 += str(int(rh1[i]*10**(-int(floor(log10(abs(rh1[i]))))+validNum-1)))
m.update(rVector1.encode('utf-8'))
rh1 = m.hexdigest()
#loop hash
tensor = tensor[0,0:s]
dimension = tensor.size//5
newVector = [1]*(dimension)   #dimension of hash vector
for i in range(0,tensor.size):
    temp = tensor[i]
    if i % 5 == 0:
        newVector[i//5] = str(int(temp*10**(-int(floor(log10(abs(temp))))+validNum-1)))
    else:
        newVector[i//5] += str(int(temp*10**(-int(floor(log10(abs(temp))))+validNum-1)))
        
tensor1 = tensor1[0,0:s]
newVector1 = [1]*(dimension)   #dimension of hash vector
for i in range(0,tensor1.size):
    temp = tensor1[i]
    if i % 5 == 0:
        newVector1[i//5] = str(int(temp*10**(-int(floor(log10(abs(temp))))+validNum-1)))
    else:
        newVector1[i//5] += str(int(temp*10**(-int(floor(log10(abs(temp))))+validNum-1)))
#feed to SHA256, and divide the 256 bits into 64*8bits
row = 0
col = 0
tensor = np.zeros((dimension*32//(28*28),28*28), dtype = np.uint8) #32 = 256/8
for i in range(0,dimension):
    m.update(newVector[i].encode('utf-8'))
    h = m.hexdigest()
    for j in range(0,32):
        ht = h[2*j:2*j+2]  #8bit
        ht = int(ht,16)
        tensor[row][col] = ht
        col += 1
        if col == 28*28:
            col = 0
            row += 1
print(tensor.shape)

row = 0
col = 0
tensor1 = np.zeros((dimension*32//(28*28),28*28), dtype = np.uint8) #32 = 256/8
for i in range(0,dimension):
    m.update(newVector1[i].encode('utf-8'))
    h = m.hexdigest()
    for j in range(0,32):
        ht = h[2*j:2*j+2]  #8bit
        ht = int(ht,16)
        tensor1[row][col] = ht
        col += 1
        if col == 28*28:
            col = 0
            row += 1
print(tensor1.shape)
#XOR
images = np.rint(images*255).astype(np.uint8)
bound = min(images.shape[0],tensor.shape[0])

#output = np.zeros((bound,28*28),np.uint8)
#output1 = np.zeros((bound,28*28),np.uint8)
output = np.zeros((bound,28*28),np.int16)
output1 = np.zeros((bound,28*28),np.int16)
npcr = np.zeros(bound)
naci = np.zeros(bound)
cab = np.zeros(bound)
for i in range(0,bound):
    output[i] = tensor[i]^images[i]
#sensitivity
    output1[i] = tensor1[i]^images[i]
    npcr[i] = sum(output1[i]!=output[i])/output[i].size
    naci[i] = sum(abs(output1[i]-output[i]))/(output[i].size*255)

oimage = output[0].reshape(28,28)

plt.imshow(images[0].reshape(28,28),cmap=plt.cm.gray) 
fig = plt.gcf() # 'get current figure'
fig.savefig('original.eps')
plt.imshow(oimage,cmap=plt.cm.gray)
fig = plt.gcf() # 'get current figure'
fig.savefig('encrypted.eps')
re = oimage^(tensor[0].reshape(28,28))
plt.imshow(re,cmap=plt.cm.gray)
fig = plt.gcf() # 'get current figure'
fig.savefig('decrypted.eps')

#correlation
#    timg = images[i].reshape(-1)
#    tout = output[i].reshape(-1)
#    ori_average = sum(timg)/timg.size
#    des_average = sum(tout)/tout.size
#    cab[i] = sum((timg - ori_average) * (tout - des_average))/np.sqrt((sum((timg - ori_average)*(timg - ori_average))*sum((tout - des_average)*(tout - des_average))))

#mean_npcr = np.mean(npcr)
#mean_naci = np.mean(naci)
#fig,axes=plt.subplots(1,2) 
#sns.set_palette("hls")
#sns.distplot(npcr,bins='auto',kde=True,hist=False ,kde_kws={"label":"pdf"}, axlabel = 'NPCR',ax=axes[0])
#sns.distplot(naci,bins='auto',kde=True,hist=False ,kde_kws={"label":"pdf"}, axlabel = 'NACI',ax=axes[1])
#
#plt.legend(loc='upper left')
#fig = plt.gcf() # 'get current figure'
#fig.savefig('sen_key_image.eps')
#plt.show()

#images = images.reshape(-1)
#output = output.reshape(-1)
#sns.set_palette("hls")
#sns.distplot(images,color='b',bins='auto',kde=True,hist=False ,kde_kws={"label":"Plaintext"})
#sns.distplot(output,color='r',bins='auto',kde=True,hist=False ,kde_kws={"label":"Ciphertext"})
#plt.xlabel("Pixel value")

#plt.ylabel("Frequency")

#plt.legend(loc='upper left')
#fig = plt.gcf() # 'get current figure'
#fig.savefig('Frequency_image.eps')
#plt.show()
