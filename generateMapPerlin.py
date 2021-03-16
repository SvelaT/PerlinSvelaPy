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

def genRandomVectors(numVectorsX,numVectorsY,vsize):
    vectorsX = [ [ 0 for i in range(numVectorsY) ] for j in range(numVectorsX) ] 
    vectorsY = [ [ 0 for i in range(numVectorsY) ] for j in range(numVectorsX) ] 

    for i in range(numVectorsX):
        for j in range(numVectorsY):
            randomAngle = genRandomAngle()
            vectorsX[i][j] = math.cos(randomAngle)*vsize
            vectorsY[i][j] = math.sin(randomAngle)*vsize

    return [vectorsX,vectorsY]

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

    dotProductsNW = dotProducts[0]
    dotProductsSW = dotProducts[1]
    dotProductsNE = dotProducts[2]
    dotProductsSE = dotProducts[3]

    for i in range(width):
        for j in range(height):
            xPercent = smooth((i%ivd)/ivd) #alto no E, baixo no W
            yPercent = smooth((j%ivd)/ivd) #alto no S, baixo no N

            interNorth = (dotProductsSE[i][j]-dotProductsSW[i][j])*xPercent+dotProductsSW[i][j]
            interSouth = (dotProductsNE[i][j]-dotProductsNW[i][j])*xPercent+dotProductsNW[i][j]

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


outputImageWidth = int(input("Output image width?"))
outputImageHeight = int(input("Output image height?"))
interVectorDistance = int(input("Inter vector distance?"))
vectorSize = int(input("Vector size?"))

perlinMap1 = perlinMap(outputImageWidth,outputImageHeight,interVectorDistance,vectorSize)
perlinMap2 = perlinMap(outputImageWidth,outputImageHeight,math.floor(interVectorDistance/3),math.floor(vectorSize/3))
perlinMap2 = multiplyMap(outputImageWidth,outputImageHeight,perlinMap2,0.5)
fullMap = addMaps(outputImageWidth,outputImageHeight,perlinMap1,perlinMap2)

normalizedResults = normalizeMap(outputImageWidth,outputImageHeight,fullMap)

redColors = [ [ 0 for i in range(outputImageHeight) ] for j in range(outputImageWidth) ] 
greenColors = [ [ 0 for i in range(outputImageHeight) ] for j in range(outputImageWidth) ] 
blueColors = [ [ 0 for i in range(outputImageHeight) ] for j in range(outputImageWidth) ] 

for i in range(outputImageWidth):
    for j in range(outputImageHeight):
        value = math.ceil(255*normalizedResults[i][j])
        if(value < 126):
            blueColors[i][j] = value
        else:
            greenColors[i][j] = value

generatedMap = Image.new(mode = "RGB", size=(outputImageWidth,outputImageHeight))

pixels = generatedMap.load()

for i in range(generatedMap.size[0]):
    for j in range(generatedMap.size[1]):
        pixels[i,j] = (redColors[i][j],greenColors[i][j],blueColors[i][j])
    
generatedMap.save("generatedMap.png")

wait = input("Press any key...")
