#This file rapresents the implementation in dynamic programming
#of the Needlam & Wunch algorithm for global allignment of two sequences.
#The file must be executed by means of the terminal where the user has to provide
#the name of the file with .py extension and the two sequences
#for which he wants the allignment.Then, the program will ask the user
#to insert the value of the gap penalty, the match and the mismatch.
#At the end, the programm will visualize the matrix containing the scores and the optimal
#global allignment of the two sequences.

import sys
matrixTrace = []                               #global since it can be used by different function
gap = int(input('Insert the gap penalty: '))
match = int(input('Insert the match score: '))        #all global since the user is able
mismatch = int(input('Insert the mismatch score: '))  #to change their value

def check(x,y):
    if x != y:
        return mismatch  #check match and mismatch
    else:
        return match

def movement(ver,ori,diag):
    move = max(ver,ori,diag)
    if move == ver:
        return 'V'
    if move == ori:     #define direction of the 
        return 'O'      #optimal allignment 
    if move == diag:
        return 'D'
    
def traceBack(currentMove):             #fill matrix for traceback
    global matrixTrace          
    matrixTrace = matrixTrace + [currentMove,]
    return matrixTrace
 
def score(seq1,seq2):
    global matrixTrace

    n = len(seq2)+1     #n is the number of columns in the mXn score-matrix
    m = len(seq1)       #m is the number of rows in the mXn score-matrix
    
    firstRow = [x*gap for x in range(n)]   
    matrix =[]
    results = []
    results += [firstRow]   #matrix row initialization
    matrix = firstRow
    volatile = matrixTrace
    firstRowTrace = ['E'] + (['O']*len(seq2))   #row initialization of the
    volatile += [firstRowTrace,]                      #matrix needed for the traceback 
    matrixTrace = volatile    
    for i in range(m):
        j = 0
        volatileRowUp = matrix
        collectScores = [(i+1)*gap,]   #incrementally matrix-columns initialization
        currentMove = ['V']    #incrementally initialization of the columns of the traceback matrix 
        while len(collectScores) != n:

            volatileRow = volatileRowUp[0:j+2]        #consider values at index [i,j] and [i,j+1] of the row
            ver = volatileRow[j+1] + gap
            ori = collectScores[j] + gap                 #consider value at index [i+1,j] of the column
            diag = volatileRow[j] + check(seq1[i],seq2[j]) 
            j+=1                                             
            score = max(ver,ori,diag)      #optimal allignment calculation and collection
            collectScores += [score,]      
            step = movement(ver,ori,diag)     #associate the direction to the optimal alligment score
            currentMove += [step,]

        traceback = traceBack(currentMove)   #extend traceback matrix
        results += [collectScores,]          #add resulting row containing the socres to the final scores-matrix
        matrix = collectScores               #rinitialize the row to continuo the matrix filling

    return results

def plotMatrix(seq1,seq2):        #plot score matrix
    m = len(seq2)+1    
    result = score(seq1,seq2)
    firstRow = [x*gap for x in range(m)]

    print('  |      '+'   '.join(seq2))         #plot orizontal sequence
    print('----'*(2+ m)) 
    print(' '.join(('  |'+'',str(firstRow))))     #plot initialization
    
    for e in range(1,len(result)):                                  #plot the vertical sequence
        print(''.join((seq1[e-1],' | ',''.join(str(result[e])))))    #and the rest of the matrix

def seqAlignment(seq1,seq2):
    seq1Al = ''
    seq2Al = ''
    i = len(matrixTrace)-1
    j = len(matrixTrace[0])-1
    x = len(matrixTrace)
    while x != 0:
        value = matrixTrace[i][j]      #check value in the traceback matrix
        if value == 'E':
            return seq1Al,seq2Al      #end
        if value == 'V':   #mismatch
            seq1Al = seq1[i-1] + seq1Al   #add a residue on seq1
            seq2Al =  '-' + seq2Al        #add gap on seq2
            i = i-1
            x = x-1
        if value == 'O':   #mismatch
            seq2Al =  seq2[j-1] + seq2Al   #add a residue on seq2
            seq1Al = '-' + seq1Al          #add a gap on seq 1
            j = j-1
        if value == 'D':   #match
            seq1Al = seq1[i-1] + seq1Al   #add the matching residue
            seq2Al = seq2[j-1] + seq2Al   #on both seq1 and seq2
            i = i-1
            j = j-1
            x = x-1
            
def NWalgorithm(seq1,seq2):    #all in one
    seq1 = seq1.upper()
    seq2 = seq2.upper()
    show = plotMatrix(seq1,seq2)            #matrix
    alignment = seqAlignment(seq1,seq2)      #alignment 
    return alignment

if len(sys.argv) != 3:
    print('Usage %s string1 string2' % sys.argv[0])
    sys.exit()
str1 = sys.argv[1]
str2 = sys.argv[2]
function = NWalgorithm(str1,str2)
for seq in function:
    print(seq)







            
            
        
    

    
    
