import string
import copy
import time

def read_problem():
    inputFile=file('Sudoku_input.txt','r')
    rtnList=[]
    lProblem=[]
    while True:
        line=inputFile.readline()
        line=line.strip()
        if len(line) == 0:
            break
       
        if line==';':
            rtnList.append(copy.deepcopy(lProblem))
            lProblem=[]
            continue
       
        rowList=line.split(' ')
        numberList=[]
        for number in rowList:
            number=int(number)
            numberList.append(number)
        lProblem.append(numberList)
    return rtnList
  
def sudoku_solver(lProblem,logFile):
    lSolverStack=[lProblem]
    count=0
    while len(lSolverStack)>0:
        lCurrSolution=lSolverStack.pop()
        count=count+1
        logFile.write("%d" % count + '\n')
        for row in lCurrSolution:
            outLine=''
            for number in row:
                outLine=outLine + "%d" % number +' '
            logFile.write(outLine+'\n')
        logFile.write("---------------------------\n")
        isResult=True
        lMinAvailableNumber=range(1,10)
        lMinAvailableNumberX=0
        lMinAvailableNumberY=0
       
        for idx in range(81):
            i=idx%9
            j=idx/9
            if lCurrSolution[i][j]==0:
                isResult=False
                lCurrAvailableNumber=range(1,10)
                for x in range(9):
                    if lCurrAvailableNumber.count(lCurrSolution[i][x])>0:
                        lCurrAvailableNumber.remove(lCurrSolution[i][x])
                for y in range(9):
                    if lCurrAvailableNumber.count(lCurrSolution[y][j])>0:
                        lCurrAvailableNumber.remove(lCurrSolution[y][j])
                for x in range(i/3*3,i/3*3+3):
                    for y in range(j/3*3,j/3*3+3):
                        if lCurrAvailableNumber.count(lCurrSolution[x][y])>0:
                            lCurrAvailableNumber.remove(lCurrSolution[x][y])           
                if len(lCurrAvailableNumber)<len(lMinAvailableNumber):
                    lMinAvailableNumber=copy.deepcopy(lCurrAvailableNumber)
                    lMinAvailableNumberX=i
                    lMinAvailableNumberY=j
               
                if len(lMinAvailableNumber)==0:
                    break
               
        if len(lMinAvailableNumber)>0:
            for number in lMinAvailableNumber:
                lNewSolution=copy.deepcopy(lCurrSolution)
                lNewSolution[lMinAvailableNumberX][lMinAvailableNumberY]=number
                lSolverStack.append(lNewSolution)       
               
        if isResult:
            return lCurrSolution
    return []
       
       
if __name__=='__main__':
    resultFile=open("Sudoku_output.txt",'w')
    lProblemList=read_problem()
    count=0
    print "Start solving.."
    for lProblem in lProblemList:
        count=count+1
        resultFile.write("Solving Problem:"+"%d" % count + ":" + "\n")
        logFile=open("Problem_"+"%d" % count+".log","w")
        startTime=time.time()
        lResult=sudoku_solver(lProblem,logFile)
        logFile.close()
        endTime=time.time()
        print "  Problem " + "%d" % count + ": finished! Time consuming: " + "%.4f" % (endTime-startTime) + " Seconds"
        if len(lResult)==0:
            resultFile.write("No Answer...\n")
        else:
            for row in lResult:
                outLine=''
                for number in row:
                    outLine=outLine + "%d" % number +' '
                resultFile.write(outLine+"\n")
        resultFile.write("--------------------------------\n")
    resultFile.close()
    print "Done!!"
