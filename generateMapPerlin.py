from PIL import Image
import math
import random

def genRandomAngle():
    return (random.randint(1,10000)/10000)*math.pi*2

def smooth(x):
    if x > 0.5:
        return (-2*(x-1)*(x-1))+1
    else:
        return 2*x*x

def triangleWave(x,period):
    value = x%period
    peak = period/2

    if(value > period/2):
        return (-value+period)/peak
    else:
        return value/peak

def remapValues(x,origMin,origMax,newMin,newMax):
    return ((x-origMin)/(origMax-origMin))*(newMax-newMin)+newMin

def genRandomColor():
    return [random.randint(0,255),random.randint(0,255),random.randint(0,255)]

def genRandomColorFrom(color):
    deltaValue = random.randint(-100,100)
    deltaR = deltaValue+random.randint(-40,40)
    deltaG = deltaValue+random.randint(-40,40)
    deltaB = deltaValue+random.randint(-40,40)

    finalR = max(min(color[0]+deltaR,255),0)
    finalG = max(min(color[1]+deltaG,255),0)
    finalB = max(min(color[2]+deltaB,255),0)

    return[finalR,finalG,finalB]

def genNRandomColors(n):
    colors = [ [0,0,0] for i in range(n)]
    
    for i in range(n):
        colors[i] = genRandomColor()
    
    return colors

def genNRandomSimilarColors(n):
    colors = [ [0,0,0] for i in range(n)]

    colors[0] = genRandomColor()

    for i in range(n-1):
        colors[i+1] = genRandomColorFrom(colors[i])

    return colors


def interpolateColors(color1,color2,percent):
    color = [0,0,0]

    color[0] = math.floor((color2[0] - color1[0])*percent + color1[0])
    color[1] = math.floor((color2[1] - color1[1])*percent + color1[1])
    color[2] = math.floor((color2[2] - color1[2])*percent + color1[2])

    return color
    
def genRandomVectors(numVectorsX,numVectorsY,vsize):
    vectorsX = [ [ 0 for i in range(numVectorsY) ] for j in range(numVectorsX) ] 
    vectorsY = [ [ 0 for i in range(numVectorsY) ] for j in range(numVectorsX) ] 

    for i in range(numVectorsX):
        for j in range(numVectorsY):
            randomAngle = genRandomAngle()
            vectorsX[i][j] = math.cos(randomAngle)*vsize
            vectorsY[i][j] = math.sin(randomAngle)*vsize

    return [vectorsX,vectorsY]

def genRandomLatPoints(numPointsX,numPointsY):
    latPoints = [ [ 0 for i in range(numPointsY) ] for j in range(numPointsX) ]

    for i in range(numPointsX):
        for j in range(numPointsY):
            latPoints[i][j] = random.randint(1,1000)
    
    return latPoints

def calculateDotProducts(width,height,ivd,vectorsX,vectorsY):
    dotProductsNW = [ [ 0 for i in range(height) ] for j in range(width) ] 
    dotProductsSW = [ [ 0 for i in range(height) ] for j in range(width) ] 
    dotProductsNE = [ [ 0 for i in range(height) ] for j in range(width) ] 
    dotProductsSE = [ [ 0 for i in range(height) ] for j in range(width) ] 

    for i in range(width):
        for j in range(height):
            #NW
            dispVectorX = i%ivd
            dispVectorY = j%ivd
            vectorIndexX = math.floor(i/ivd)
            vectorIndexY = math.floor(j/ivd)

            dotProductsNW[i][j] = dispVectorX*vectorsX[vectorIndexX][vectorIndexY] + dispVectorY*vectorsY[vectorIndexX][vectorIndexY]

            #SW
            dispVectorX = i%ivd
            dispVectorY = j%ivd-ivd
            vectorIndexX = math.floor(i/ivd)
            vectorIndexY = math.ceil(j/ivd)

            dotProductsSW[i][j] = dispVectorX*vectorsX[vectorIndexX][vectorIndexY] + dispVectorY*vectorsY[vectorIndexX][vectorIndexY]

            #NE
            dispVectorX = i%ivd-ivd
            dispVectorY = j%ivd
            vectorIndexX = math.ceil(i/ivd)
            vectorIndexY = math.floor(j/ivd)

            dotProductsNE[i][j] = dispVectorX*vectorsX[vectorIndexX][vectorIndexY] + dispVectorY*vectorsY[vectorIndexX][vectorIndexY]

            #SE
            dispVectorX = i%ivd - ivd
            dispVectorY = j%ivd - ivd
            vectorIndexX = math.ceil(i/ivd)
            vectorIndexY = math.ceil(j/ivd)

            dotProductsSE[i][j] = dispVectorX*vectorsX[vectorIndexX][vectorIndexY] + dispVectorY*vectorsY[vectorIndexX][vectorIndexY]

    return [dotProductsNW,dotProductsSW,dotProductsNE,dotProductsSE]

def interpolateDotProducts(width,height,ivd,dotProducts):
    interpolatedResults = [ [ 0 for i in range(height) ] for j in range(width) ] 

    valueNW = dotProducts[0]
    valueSW = dotProducts[1]
    valueNE = dotProducts[2]
    valueSE = dotProducts[3]

    for i in range(width):
        for j in range(height):
            xPercent = smooth((i%ivd)/ivd) #alto no E, baixo no W
            yPercent = smooth((j%ivd)/ivd) #alto no S, baixo no N

            interNorth = (valueSE[i][j]-valueSW[i][j])*xPercent+valueSW[i][j]
            interSouth = (valueNE[i][j]-valueNW[i][j])*xPercent+valueNW[i][j]

            interpolatedResults[i][j] = (interNorth-interSouth)*yPercent+interSouth

    return interpolatedResults

def interpolateCorners(width,height,ivd,corners):
    interpolatedResults = [ [ 0 for i in range(height) ] for j in range(width) ] 

    for i in range(width):
        for j in range(height):
            xPercent = smooth((i%ivd)/ivd) #alto no E, baixo no W
            yPercent = smooth((j%ivd)/ivd) #alto no S, baixo no N

            cornerNW = corners[math.floor(i/ivd)][math.floor(j/ivd)]
            cornerSW = corners[math.floor(i/ivd)][math.ceil(j/ivd)]
            cornerNE = corners[math.ceil(i/ivd)][math.floor(j/ivd)]
            cornerSE = corners[math.ceil(i/ivd)][math.ceil(j/ivd)]

            interNorth = (cornerSE-cornerSW)*xPercent+cornerSW
            interSouth = (cornerNE-cornerNW)*xPercent+cornerNW
            
            interpolatedResults[i][j] = (interNorth-interSouth)*yPercent+interSouth

    return interpolatedResults


    
def normalizeMap(width,height,interpolatedResults):
    maxValues = [0 for i in range(width)]
    minValues = [0 for i in range(width)]

    for i in range(width):
        maxValues[i] = max(interpolatedResults[i])
        minValues[i] = min(interpolatedResults[i])
    
    maxValue = max(maxValues)    
    minValue = min(minValues)

    normalizedResults = [ [ 0 for i in range(height) ] for j in range(width) ] 

    for i in range(width):
        for j in range(height):
            normalizedResults[i][j] = (interpolatedResults[i][j] - minValue)/(maxValue-minValue)

    return normalizedResults

def multiplyMap(width,height,heightmap,factor):
    resultMap = [ [ 0 for i in range(height) ] for j in range(width) ] 

    for i in range(width):
        for j in range(height):
            resultMap[i][j] = factor*heightmap[i][j]
    
    return resultMap


def addMaps(width,height,map1,map2):
    resultMap = [ [ 0 for i in range(height) ] for j in range(width) ] 

    for i in range(width):
        for j in range(height):
            resultMap[i][j] = map1[i][j] + map2[i][j]
    
    return resultMap


def perlinMap(width,height,ivd,vsize):
    numVectorsX = math.ceil(width/ivd)+1
    numVectorsY = math.ceil(height/ivd)+1

    vectors = genRandomVectors(numVectorsX,numVectorsY,vsize)

    vectorsX = vectors[0]
    vectorsY = vectors[1]

    dotProducts = calculateDotProducts(width,height,ivd,vectorsX,vectorsY)

    interpolatedResults = interpolateDotProducts(width,height,ivd,dotProducts)

    normalizedMap = normalizeMap(width,height,interpolatedResults)

    return normalizedMap

def valueNoiseMap(width,height,ivd):
    numPointsX = math.ceil(width/ivd)+1
    numPointsY = math.ceil(height/ivd)+1

    latPoints = genRandomLatPoints(numPointsX,numPointsY)

    interpolatedResults = interpolateCorners(width,height,ivd,latPoints)

    normalizedMap = normalizeMap(width,height,interpolatedResults)

    return normalizedMap

def cosinesMap(width,height,freqX,freqY):
    resultMap = [ [ 0 for i in range(height) ] for j in range(width) ] 

    for i in range(width):
        for j in range(height):
            resultMap[i][j] = math.cos(freqX*i)+math.cos(freqY*j)
        
    return resultMap 

def sawtoothMap(width,height,periodX,periodY):
    resultMap = [ [ 0 for i in range(height) ] for j in range(width) ] 

    for i in range(width):
        for j in range(height):
            resultMap[i][j] = i%periodX + j%periodY

    return resultMap

def triangleMap(width,height,periodX,periodY):
    resultMap = [ [ 0 for i in range(height) ] for j in range(width) ] 

    for i in range(width):
        for j in range(height):
            resultMap[i][j] = triangleWave(i,periodX)+triangleWave(j,periodY)

    return resultMap

def randomNoiseMap(width,height):
    resultMap = [ [ 0 for i in range(height) ] for j in range(width) ] 

    for i in range(width):
        for j in range(height):
            resultMap[i][j] = random.randint(1,10000)/10000

    return resultMap

def distanceMap(width,height,pointX,pointY):
    resultMap = [ [ 0 for i in range(height) ] for j in range(width) ] 

    for i in range(width):
        for j in range(height):
            resultMap[i][j] = math.sqrt((i-pointX)*(i-pointX) + (j-pointY)*(j-pointY))

    return resultMap

def distanceCosMap(width,height,pointX,pointY,freq):
    resultMap = [ [ 0 for i in range(height) ] for j in range(width) ] 

    for i in range(width):
        for j in range(height):
            resultMap[i][j] = math.cos(freq*math.sqrt((i-pointX)*(i-pointX) + (j-pointY)*(j-pointY)))

    return resultMap

def distanceTriangleMap(width,height,pointX,pointY,period):
    resultMap = [ [ 0 for i in range(height) ] for j in range(width) ] 

    for i in range(width):
        for j in range(height):
            resultMap[i][j] = triangleWave(math.sqrt((i-pointX)*(i-pointX) + (j-pointY)*(j-pointY)),period)

    return resultMap

def gradientYMap(width,height):
    resultMap = [ [ 0 for i in range(height) ] for j in range(width) ] 

    for i in range(width):
        for j in range(height):
            resultMap[i][j] = j

    return resultMap

def genColorMapConnected(normalizedMap,numberColors,imageWidth,imageHeight,colors):
    colorsMap = [ [ [0,0,0] for i in range(imageHeight) ] for j in range(imageWidth) ] 

    for i in range(imageWidth):
        for j in range(imageHeight):
            heightValue = (numberColors-1)*normalizedResults[i][j]
            for w in range(numberColors-1):
                if(heightValue <= (w+1)):
                    heightValue = heightValue - w
                    colorsMap[i][j] = interpolateColors(colors[w],colors[w+1],heightValue)
                    break

    return colorsMap

def genColorMapSeparated(normalizedMap,numberColors,imageWidth,imageHeight,colors):
    colorsMap = [ [ [0,0,0] for i in range(imageHeight) ] for j in range(imageWidth) ] 

    for i in range(imageWidth):
        for j in range(imageHeight):
            heightValue = (math.floor(numberColors/2))*normalizedResults[i][j]
            for w in range(math.floor(numberColors/2)):
                if(heightValue <= (w+1)):
                    heightValue = heightValue - w
                    colorsMap[i][j] = interpolateColors(colors[2*w],colors[2*w+1],heightValue)
                    break

    return colorsMap



outputImageWidth = 1080
outputImageHeight = 1080

ivd = 100
vsize = 100
#normalizedResults = randomNoiseMap(outputImageWidth,outputImageHeight)
normalizedResults1 = perlinMap(outputImageWidth,outputImageHeight,ivd,vsize)
normalizedResults2 = perlinMap(outputImageWidth,outputImageHeight,math.floor(ivd/6),math.floor(vsize/6))
normalizedResults2 = multiplyMap(outputImageWidth,outputImageHeight,normalizedResults2,0.2)
normalizedResults3 = perlinMap(outputImageWidth,outputImageHeight,math.floor(ivd/18),math.floor(vsize/18))
normalizedResults3 = multiplyMap(outputImageWidth,outputImageHeight,normalizedResults3,0.1)
normalizedResults = addMaps(outputImageWidth,outputImageHeight,normalizedResults1,normalizedResults2)
normalizedResults = addMaps(outputImageWidth,outputImageHeight,normalizedResults,normalizedResults3)
#normalizedResults = gradientYMap(outputImageWidth,outputImageHeight)
normalizedResults = normalizeMap(outputImageWidth,outputImageHeight,normalizedResults)
colors = [[0,0,0],[0,0,255],[0,64,0],[255,255,255]]
numberColors = 4

colorsMap = genColorMapSeparated(normalizedResults,numberColors,outputImageWidth,outputImageHeight,colors)


generatedMap = Image.new(mode = "RGB", size=(outputImageWidth,outputImageHeight))

pixels = generatedMap.load()

for i in range(generatedMap.size[0]):
    for j in range(generatedMap.size[1]):
        pixels[i,j] = (colorsMap[i][j][0],colorsMap[i][j][1],colorsMap[i][j][2])
    
generatedMap.save("generatedMap.png")
