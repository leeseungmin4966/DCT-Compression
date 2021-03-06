import math
import cv2
import numpy as np
import copy

def makeDctBasis() :
    N = 8
    M = 8
    basis = [list() for _ in range(N)]
    for u in range(N) :
        for v in range(M) :
            tmp = [[0]*N for _ in range(N)]
            Cu = 1 if u != 0 else (2 ** 0.5) / 2
            Cv = 1 if v != 0 else (2 ** 0.5) / 2
            constant = (Cu * Cv) / 4
            for i in range(N) :
                for j in range(M) :
                    cosU = math.cos(((2*i+1) * (u*math.pi))/(N*2))
                    cosV = math.cos(((2*j+1) * (v*math.pi))/(N*2))
                    tmp[i][j] = round((constant*cosU*cosV),4)
            basis[u].append(tmp)
    return basis

def makeIDctBasis():
    N = 8
    M = 8
    basis = [list() for _ in range(N)]
    for i in range(N):
        for j in range(M):
            tmp = [[0] * N for _ in range(N)]
            for u in range(N):
                for v in range(M):
                    Cu = 1 if u != 0 else (2 ** 0.5) / 2
                    Cv = 1 if v != 0 else (2 ** 0.5) / 2
                    constant = (Cu * Cv) / 4
                    cosU = math.cos(((2 * i + 1) * (u * math.pi)) / (N * 2))
                    cosV = math.cos(((2 * j + 1) * (v * math.pi)) / (N * 2))
                    tmp[u][v] = (constant * cosU * cosV)
            basis[i].append(tmp)
    return basis

def dctPerform(basis,blocks) :
    N = 8
    for u in range(len(blocks)) :
        for v in range(len(blocks[0])) :
            Fblock = list([0] * N for _ in range(N))
            for bi in range(len(basis)) :
                for bj in range(len(basis[0])) :
                    b = basis[bi][bj]
                    accum = 0
                    for i in range(N) :
                        for j in range(N) :
                            accum += (blocks[u][v][i][j] * b[i][j])
                    Fblock[bi][bj] = round((accum/1000),4)
            blocks[u][v] = Fblock
    return blocks

def inverseDctPerform(basis,blocks,Coeff) :
    N=8
    cpBlocks = copy.deepcopy(blocks)
    for u in range(len(cpBlocks)) :
        for v in range(len(cpBlocks[0])) :
            fBlock = list([0] * N for _ in range(N))
            for bi in range(len(basis)) :
                for bj in range(len(basis[0])) :
                    b = basis[bi][bj]
                    accum = 0
                    for i in range(Coeff) :
                        for j in range(Coeff) :
                            accum += (cpBlocks[u][v][i][j] * b[i][j])
                    fBlock[bi][bj] = round((accum*1000))
            cpBlocks[u][v] = fBlock
    return cpBlocks

def convertListToNumpyArary(blocks) :
    blocks = np.array(blocks)
    for i in range(len(blocks)) :
        blocks[i] = np.array(blocks[i])
        for j in range(len(blocks[0])) :
            blocks[i][j] = np.array(blocks[i][j])
    return blocks

def splitBlocks(img,h,w) :
    blocks = [[0] * (w // 8) for _ in range(h // 8)]
    splitedImg = np.vsplit(img,h//8)
    for idx1,ary in enumerate(splitedImg) :
        nary = np.hsplit(ary, w // 8)
        for idx2,block in enumerate(nary) :
            blocks[idx1][idx2] = block
    return blocks

def mergeBlocks(blocks,h,w) :
    N = 8
    arr = np.full((h, w),0)
    for u in range(len(blocks)) :
        for v in range(len(blocks[0])) :
            for i in range(N) :
                for j in range(N) :
                    arr[i+(u*N)][j+(v*N)] = int(blocks[u][v][i][j])
    return arr


if __name__ == "__main__" :

    # 1 - 2D DCT??? ????????? 8x8 DCT basis ?????????
    basis = makeDctBasis()

    # 2 - ?????? ?????? ?????? ?????? (ex. Lena)??? read ?????? graylevel??? ??????
    img = cv2.imread("test.jpeg")
    h, w, _ = img.shape
    grayImg = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

    # 3 - ????????? blocks?????? ????????? & DCT ?????? ???, Fuv Blocks ??????
    blocks = splitBlocks(grayImg,h,w)
    FuvBlocks = dctPerform(basis,blocks)

    # 4 - F(u,v)??? ?????? IDCT??? 8x8 ????????? ?????? ??????

    # 4-1) F(u,v) ????????? ??????
    basis = makeIDctBasis()
    fijBlocks = inverseDctPerform(basis,FuvBlocks,8) # coeff = 8
    fijBlocks = convertListToNumpyArary(fijBlocks)
    fij = mergeBlocks(fijBlocks,h,w)
    cv2.imwrite('test1.jpeg', fij)

    # 4-2) F(u,v) ????????? 4x4??? ????????? ?????? ???????????? 0??? ?????? ??????
    fijBlocks = inverseDctPerform(basis, FuvBlocks,4) # coeff = 4
    fijBlocks = convertListToNumpyArary(fijBlocks)
    fij = mergeBlocks(fijBlocks, h, w)
    cv2.imwrite('test2.jpeg', fij)

    # 4-3) F(u,v) ????????? 2x2??? ????????? ?????? ???????????? 0??? ?????? ??????
    fijBlocks = inverseDctPerform(basis, FuvBlocks, 2) # coeff = 2
    fijBlocks = convertListToNumpyArary(fijBlocks)
    fij = mergeBlocks(fijBlocks, h, w)
    cv2.imwrite('test3.jpeg', fij)




