import binascii, cv2
import numpy as np
import sewar
from matplotlib import pyplot as plt

def convertStringToBinary(string):
    return bin(int.from_bytes(string.encode(), 'big'))

def convertBinaryToString(binary):
    n = int(binary, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

print("\nThis code is going to hide data into 'photo.bmp'.(3 cahnnels LSB). If you don't want this photo to hide your data, add your own photo and rename it as 'photo.bmp'\n")

imageName = 'photo.bmp'

originalImage = cv2.imread(imageName)
image = cv2.imread(imageName)
height, width = image.shape[:2]
bitsCapacity = (height * width) * 3
bytesCapacity = bitsCapacity / 8
print('You can hide', bitsCapacity, 'bits(', int(bytesCapacity), 'character(s) ) into this image.\n')

message = input('Enter a message to hide: ')
# with open('message.txt', 'r') as file:
#     message = file.read()
print(message)

binaryMessage = convertStringToBinary(message)

#Calculating message size in bits
bitsMessageSize = 0
for i in binaryMessage[2::]:
    bitsMessageSize += 1

if bitsMessageSize > bitsCapacity:
    print('\nError: Message size is greater than the image capacity.')
    exit()

print('Binary encoded message:', binaryMessage[2::], '\n')

index = 0
messageIndex = 2
percentPart = 100 / bitsMessageSize
percentage = 0
print(str(int(percentage))+"% complete", end="\r")

for i in range(height):
    if index >= bitsMessageSize:
        break
    for j in range(width):
        if index >= bitsMessageSize:
            break
        pixelValues = image[i,j]
        #print('Original pixel values:', 'h:', i, 'w:', j, ':', pixelValues)
        #BGR
        for l in range(3):
            if (messageIndex - 2) >= bitsMessageSize:
                break
            elif l == 0:
                print(str(int(percentage))+"% complete", end="\r")
                #print('Orig:', bin(image[i, j][0]))
                if binaryMessage[messageIndex] == '1':
                    image[i, j][0] = image[i, j][0] | int('0b1', 2)
                else:
                    image[i, j][0] = image[i, j][0] & int('0b11111110', 2)
                #print('Chan:', bin(image[i, j][0]))
                percentage += percentPart
            elif l == 1:
                print(str(int(percentage))+"% complete", end="\r")
                #print('Orig:', bin(image[i, j][1]))
                if binaryMessage[messageIndex] == '1':
                    image[i, j][1] = image[i, j][1] | int('0b1', 2)
                else:
                    image[i, j][1] = image[i, j][1] & int('0b11111110', 2)
                #print('Chan:', bin(image[i, j][1]))
                percentage += percentPart
            elif l == 2:
                print(str(int(percentage))+"% complete", end="\r")
                #print('Orig:', bin(image[i, j][2]))
                if binaryMessage[messageIndex] == '1':
                    image[i, j][2] = image[i, j][2] | int('0b1', 2)
                else:
                    image[i, j][2] = image[i, j][2] & int('0b11111110', 2)
                #print('Chan:', bin(image[i, j][2]))
                percentage += percentPart
            messageIndex += 1

        index += 1
        pixelValues = image[i, j]
        #print('Changed pixel values:', 'h:', i, 'w:', j, ':', pixelValues)

print("100% complete")
print('You hid', bitsMessageSize, 'bits')
cv2.imwrite('hidden.bmp', image)

#Calculating the metrics
print('MSE:', round(sewar.mse(originalImage, image), 5))
print('PSNR:', round(sewar.psnr(originalImage, image), 5))
print('UIQI:', round(sewar.uqi(originalImage, image), 5))
(ssimValue, csValue) = sewar.ssim(originalImage, image)
print('SSIM:', round(ssimValue, 5))

numpy_horizontal = np.hstack((originalImage, image))
cv2.namedWindow("Original vs Hidden", cv2.WINDOW_NORMAL)
cv2.imshow('Original vs Hidden', numpy_horizontal)
cv2.waitKey()

#Plotting histograms
color = ('b','g','r')
plt.figure(figsize = (11, 5))
plt.subplot(1, 2, 1)
for i,col in enumerate(color):
    histr = cv2.calcHist([originalImage],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])
plt.grid()
plt.tight_layout()

plt.subplot(1, 2, 2)
for i,col in enumerate(color):
    histr = cv2.calcHist([image],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])
plt.grid()
plt.tight_layout()
plt.show()
