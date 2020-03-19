#Reading data
import binascii, cv2

def convertStringToBinary(string):
    return bin(int.from_bytes(string.encode(), 'big'))

def convertBinaryToString(binary):
    n = int(binary, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

imageName = 'hidden.bmp'

originalImage = cv2.imread(imageName)
image = cv2.imread(imageName)
height, width = image.shape[:2]

bitsMessageSize = int(input('Enter the hidden message size in bits: '))

index = 0
messageIndex = 2
binaryMessage = '0b'
percentPart = 100 / bitsMessageSize
percentage = 0
print(str(int(percentage))+"% complete", end="\r")

for i in range(height):
    if index >= bitsMessageSize:
        break
    for j in range(width):
        pixelValues = image[i,j]
        #print(pixelValues)
        if index >= bitsMessageSize:
            break
        for l in range(3):
            if (messageIndex - 2) >= bitsMessageSize:
                break
            elif l == 0:
                print(str(int(percentage))+"% complete", end="\r")
                binaryMessage += bin(image[i, j][0])[-1]
                percentage += percentPart
            elif l == 1:
                print(str(int(percentage))+"% complete", end="\r")
                binaryMessage += bin(image[i, j][1])[-1]
                percentage += percentPart
            elif l == 2:
                print(str(int(percentage))+"% complete", end="\r")
                binaryMessage += bin(image[i, j][2])[-1]
                percentage += percentPart
            messageIndex += 1

        index += 1

print("100% complete")
print('Binary message:', binaryMessage[2::])
print('Hidden data:', convertBinaryToString(binaryMessage[2::]))
