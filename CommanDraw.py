def invertEndianess(str):
    invertedStr=""
    i = 0
    while i < len(str):
        invertedStr=invertedStr+str[len(str)-2-i]
        invertedStr=invertedStr+str[len(str)-1-i]
        i+=2
    return invertedStr 

def decimalToHex32Str(int):
    return (str(hex(int)).replace("0x","")).zfill(8)

#opening file
fo = open(raw_input("Enter the name of the file you want to edit(\"imageName.bmp\"):\n"),"wb")

#writing header field
hexHeader = ""
additional="0000000036000000" #hardcoding the pixelArray for the BITMAPINFOHEADER
dibHeader = ""
pixelArray = ""

hexHeader  = hexHeader + "424D"

dibHeader=dibHeader+"28000000" #hardcoding the size for this header, TO-DO!
width = input("Enter the width in pixels: ")
height = input("Enter the height in pixels: ")

invertedWidth=invertEndianess(decimalToHex32Str(width))
invertedHeight=invertEndianess(decimalToHex32Str(height))
print("w: "+invertedWidth)
print("h: "+invertedHeight)
#each line must have a number of byte dividable by 4
padding = 0
while ((padding+width*3)%4!=0):
    padding+=1
print("Bytes for padding per line "+str(padding))

dibHeader=dibHeader+invertedWidth+invertedHeight+"0100180000000000"#01 00 | 18 00 | 00 00 00 00
rawDataSize = invertEndianess(decimalToHex32Str((width*3+padding) * (height))) #multiply by 3 because it is 24 bit color, 24b = 3B
dibHeader=dibHeader+rawDataSize+"130B0000130B00000000000000000000"

#pixel array data
print("Please pay attention! Pixel indexing starts from the bottom left corner!")
backgroundColor = invertEndianess(raw_input("Enter background color\n")) 
Matrix = [[backgroundColor for i in range(height)] for j in range(width)] 

x=0
y=0
while 1==1:
    print("Enter a negative coordinate to close and save")
    x = input("Enter the x coordinate: ")
    y = input("Enter the y coordinate: ")
    if(x<0 or y<0):
        break
    Matrix[x][y]=invertEndianess(raw_input("Enter color for pixel("+str(x)+", "+str(y)+") in hex\n"))

x=0
y=0
while y<height:
    while x<width: 
        pixelArray=pixelArray+Matrix[x][y]
        x+=1
    pixelArray=pixelArray+("00"*padding)
    x=0
    y+=1
#setting size before writing
size = invertEndianess(decimalToHex32Str(len(hexHeader)/2+4+len(additional)/2+len(dibHeader)/2+len(pixelArray)/2))#we divide by two because size is in byte and 1 byte = 2 hex 
print("Size with reversed endianess "+size+"\n")

#writing all the info in the file
fo.write((hexHeader+size+additional+dibHeader+pixelArray).decode('hex'))
fo.close()

