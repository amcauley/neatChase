import math
import random
import neatChase
import Common

''' Transfer function between nodes. Currently a sigmoid. '''
def nodeTransferFunc(x, offset = 0):
    return 1.0/(1.0 + math.exp(-10*(x-offset)))

''' Greater Than Zero test. '''
def isGTZ(x):
    return x > 0

''' Generate a random number according to the following PDF, which can be used to select an organism from a 
    fitness-sorted listed. Lower values/indices are more likely, since more fit organisms are more likely
    to be allowed to mate. '''    
def orgSelectPdfRand(b = 1.0):
    ''' PDF: p(x) = a/(x+b)^2
        By the constraint of all results falling in the range x = [0, 1), we get a = b^2 + b
        CDF: C(x) = (b+1)x/(b+x)

        To transform a uniform distribution (as returned by random.random()) into this desired distribution,
        we need to transform the uniform distribution by the *inverse* of the desired CDF:

        Cinv(x) = x*b/(b+1-x)
            
        The parameter b can adjusted subject to b > 0. The larger b gets, the more uniform the distribution
        becomes. '''
            
    x = random.random()
    a = b*(b+1.0)
    y = x*b/(b+1.0-x)
    return y
    
''' Test function for verifying pdf. Create a histogram of <bins> number of bins. '''
def testPdf(runs=10000, bins=10, b=0.4):
    binCnt = [0]*bins
    for k in range(runs):
        bin = int(orgSelectPdfRand(b)*bins)
        assert (bin < bins)
        binCnt[bin] += 1
        
    ''' Display output. '''        
    for k in range(bins):
        print('[' + str(k) + ']: ' + str(binCnt[k]))
        
''' Generate statistics about how often a program "succeeds." '''        
def testStats():
    Common.basicPrintEn = False
    numSuc = 0
    numRuns = 100
    print('start...')
    for k in range(numRuns):
        if neatChase.runProg() > 9.0:
            numSuc += 1
        print('run ' + str(k+1) + '/' + str(numRuns) + ', ' + str(numSuc*100.0/(k+1.0)) + '% success.')

class RGB:
    def __init__(self, rgbTuple):
        self.r = rgbTuple[0]
        self.g = rgbTuple[1]
        self.b = rgbTuple[2]
        
    def __str__(self):
        return str((self.r, self.g, self.b))
 
 
''' Convert an integer to bytearray of a given number of bytes/characters. If the littleEndian flag is True (which it should
    be for bitmap writing), we'll rearrange the order accordingly. ''' 
def intToFixedWidthByteArray(inputVal, numBytes, littleEndian = True):
    nBytes = 0
    outBytes = []
    while (nBytes < numBytes):
        outBytes = [inputVal & 255] + outBytes
        inputVal = inputVal >> 8
        nBytes += 1
    
    assert(inputVal == 0) # Assert that numBytes was large enough for this value

    if (littleEndian):
        outBytes.reverse()

    #print(str(outBytes))
    return bytearray(outBytes)
 
''' Write a 2d array (top level is a list where each entry represents a row of RGBs). Array reads top left -> bottom right pixel.
    Function converted to python from https://github.com/amcauley/rayTrace/blob/master/SourceCode/Bitmap.cpp '''  
def exportBmp24(filename, rgbArray):

    f = open(filename, 'wb')
    
    height = len(rgbArray)
    width = len(rgbArray[0])
  
    #for row in range(height-1, -1, -1):
    #    for pix in range(width):
    #        rgbVal = rgbArray[row][pix]
    #        print(str((row,pix)) + ': ' + str(rgbVal))
  
    ''' Rows padded to be multiples of 4 bytes (each pixel is 3 bytes). '''
    rowPadMod = (width*3)%4
    if (rowPadMod):
        rowPadBytes = 4 - rowPadMod
    else:
        rowPadBytes = 0
    
    #print('h: ' + str(height) + ', w: ' + str(width) + ', pad: ' + str(rowPadBytes))
    
    rowSizeBytes = width*3 + rowPadBytes    

    f.write(bytearray([66,77]))                                      # magic number, 2 bytes
    f.write(intToFixedWidthByteArray(54 + rowSizeBytes*height, 4))   # size, 4 bytes
    f.write(bytearray([0]*4))                                        # reserved1 and reserved2, 4 bytes
    f.write(intToFixedWidthByteArray(54, 4))                         # offset, 4 bytes
    f.write(intToFixedWidthByteArray(40, 4))                         # headersize, 4 bytes
    f.write(intToFixedWidthByteArray(width, 4))                      # width, 4 bytes
    f.write(intToFixedWidthByteArray(height, 4))                     # height, 4 bytes
    f.write(intToFixedWidthByteArray(1, 2))                          # colorplanes, 2 bytes
    f.write(intToFixedWidthByteArray(24, 2))                         # bitsperpixel, 2 bytes
    f.write(bytearray([0]*24))                                       # Rest of the BMP fields are all 0
    
    ''' Bitmap ordering is bottom row to top row, left to right within a row. '''
    for row in range(height-1, -1, -1):
        for pix in range(width):
            rgbVal = rgbArray[row][pix]
            #print(str((row,pix)) + ': ' + str(rgbVal))
            f.write(bytearray([rgbVal.b, rgbVal.g, rgbVal.r]))
        if (rowPadBytes):
            f.write(bytearray([0]*rowPadBytes))
            
    f.close()        
 
def bmpTest(filename):

    #c = intToFixedWidthByteArray(43981, 4)
    #print(c)
    #return
    
    rgbRow = []
    for k in range(10):
        rgbRow.append(RGB((200, 100, 100)))
        
    rgbArray = []
    for k in range(20):
        rgbArray.append(rgbRow)
        
    exportBmp24(filename, rgbArray)    
 
if __name__ == "__main__":
    bmpTest('..\\temp\\test.bmp')        