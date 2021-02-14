#This file rapresents the implementation in dynamic programming
#of the Smith & Waterman algorithm for local allignment of two sequences.
#The file must be executed by means of the terminal where the user has to provide
#the name of the file with .py extension and the two sequences
#for which he wants the allignment.Then, the program will ask the user
#to insert the value of the gap penalty, the match and the mismatch.
#At the end, the programm will visualize the matrix containing the scores and the optimal
#local allignment of the two sequences.

import sys
matrixTrace = []   #global variables since it can be used by different
results = []       #functions of the algorithm
gap = int(input('Insert the gap penalty: '))
match = int(input('Insert the match score: '))       #global beacuse the user is free to decide
mismatch = int(input('Insert the mismatch score: '))       #their value

def check(x,y):    #match and mismatch value
    if x != y:
        return mismatch
    else:
        return match

def scoreCheck(ver,ori,diag):
    score = max(ver,ori,diag)   #score value checking to have
    if score < 0:               #a good local alignment 
        return 0
    else:
        return score

def movement(ver,ori,diag):
    move = max(ver,ori,diag)    #associate a movement to 
    if move > 0:                #positive optimal scores 
        if move == ver:
            return 'V'
        if move == ori:
            return 'O'
        if move == diag:
            return 'D'
    else:
        return '*'            #value rapresenting non optimal scores
    
def traceBack(currentMove):    #fill matrix for traceback
    global matrixTrace
    matrixTrace = matrixTrace + [currentMove,]
    return matrixTrace
 
def score(seq1,seq2):
    global results
    global matrixTrace
    
    n = len(seq2)+1         #n is the number of columns in the mXn matrix
    m = len(seq1)           #m is the number of rows in the mXn matrix
    
    firstRow = [0 for x in range(n)]
    matrix =[]
    results = []
    volatileR = results
    volatileR += [firstRow]       #matrix row initialization 
    results = volatileR
    matrix = firstRow
    volatileT = matrixTrace
    firstRowTrace = ['*'] + (['*']*len(seq2))   #traceback matrix initialization
    volatileT += [firstRowTrace,]
    matrixTrace = volatileT    
    for i in range(m):
        j = 0
        volatileRowUp = matrix
        collectScores = [(0)*gap,]        #matrix column initialization
        currentMove = ['*']             #traceback matrix initialization
        while len(collectScores) != n:

            volatileRow = volatileRowUp[0:j+2]    #consider values at index [i,j] and [i,j-1]
            ver = volatileRow[j+1] + gap
            ori = collectScores[j] + gap                   #consider values at index [i-1,j]
            diag = volatileRow[j] + check(seq1[i],seq2[j])
            j+=1
            score = scoreCheck(ver,ori,diag)     #check score is greater then 0
            collectScores += [score,]           #and colect it
            step = movement(ver,ori,diag)       #assosiate a value to the optimal allignment
            currentMove += [step,]              # and collect it

        traceback = traceBack(currentMove)
        results += [collectScores,]         #matrix filling and
        matrix = collectScores              #row re-initialization to keep of matrix filling

    return results

def plotMatrix(seq1,seq2):         #plot matrix
    m = len(seq2)+1    
    result = score(seq1,seq2)
    firstRow = [0 for x in range(m)]

    print('  |     '+'  '.join(seq2))        #plot horizontal sequence
    print('----'*(2+ m))
    print(' '.join(('  |'+'',str(firstRow))))   #plot first row
    
    for e in range(1,len(result)):
        print(' '.join((seq1[e-1],'|',''.join(str(result[e])))))   #plot rest of the matrix

def seqAllignment(seq1,seq2):
    startPoint = 0
    startRow = []
    startPosRow = 0
    startPosCol = 0
    localAll1 = ''
    localAll2 = ''
    for e in range(len(results)):         #find out starting point in the matrix
        volatileMax = max(results[e])        
        if volatileMax >= startPoint:
            startPoint = volatileMax
            startRow = results[e]
            startPosRow = e                   #starting position of the rows
            startPosCol = startRow.index(volatileMax)      #staring position of the columns

    startValue = matrixTrace[startPosRow][startPosCol]    #value of the matrix tarceback associated to the starting point
    startSeq1 = len(seq1[:startPosRow])
    startSeq2 = len(seq2[:startPosCol])           #sequences from which the alligment starts
    while True:
        value = matrixTrace[startPosRow][startPosCol]      #evaluate value of the matrix tarceback
        if value == '*':
            return localAll1,localAll2                     #end
        if value == 'V':      #mismatch
            localAll1 = seq1[startSeq1-1] + localAll1      #add a residue in seq1
            localAll2 = '-' + localAll2                    #add a gap in seq2
            startSeq1 = startSeq1 - 1
            startPosRow = startPosRow-1          #following value of the traceback
        if value == 'O':      #mismatch
            localAll2 = seq2[startSeq2 -1] + localAll2     #add a residue in seq2
            localAll1 = '-' + localAll1                    #add a gap in seq1
            startSeq2 = startSeq2 -1
            startPosCol = startPosCol -1         #following value of the traceback
        if value == 'D':      #match
            localAll1 = seq1[startSeq1-1] + localAll1      #add a residue in seq1
            localAll2 = seq2[startSeq2-1] + localAll2      #add a residue in seq2
            startSeq1 = startSeq1 - 1
            startSeq2 = startSeq2 - 1
            startPosRow = startPosRow - 1
            startPosCol = startPosCol - 1      #following value of the traceback
 
def SWalgorithm(seq1,seq2):       #all in one
    seq1 = seq1.upper()
    seq2 = seq2.upper()
    show = plotMatrix(seq1,seq2)
    allignment = seqAllignment(seq1,seq2)
    return allignment

if len(sys.argv) != 3:
    print('Usage %s string1 string2' % sys.argv[0])
    sys.exit()
str1 = sys.argv[1]
str2 = sys.argv[2]
function = SWalgorithm(str1,str2)
for seq in function:
    print(seq)
