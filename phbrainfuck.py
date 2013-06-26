################
## BF Machine ##
################

class VM:

    def __init__(self):
        self.limit = 3000
        self.buffer = None
        self.reset()

    def reset(self):
        if self.buffer == None:
            self.buffer = [0] *self.limit
        else:
            for i in range(0,self.limit):
                self.buffer[i] = 0
        self.code = []
        self.codePtr = 0
        self.ptr = 0
        self.warningBounds = False
        self.warningUnderflow = False
        self.warningOverflow = False
	self.warningLoops = False
	self.skipCount = 0
        self.loopPos = []
        self.inputBuffer = []
        self.outputBuffer = []
        self.instCount = 0


    def _ptrRight(self):
        self.ptr = self.ptr+1
        if self.ptr>=self.limit:
            self.warningBounds = True
            self.ptr = self.ptr - 1

    def _ptrLeft(self):
        self.ptr = self.ptr-1
        if self.ptr<0:
            self.warningBounds = True
            self.ptr = self.ptr + 1

    def _ptrValUp(self):
        val = self.buffer[self.ptr]

        if val+1>255:
            self.warningOverflow = True
            return

        self.buffer[self.ptr] = val+1

    def _ptrValDown(self):
        val = self.buffer[self.ptr]

        if val-1<0:
            self.warningUnderflow = True
            return

        self.buffer[self.ptr] = val-1

    def _outputPtr(self):
        val = self.buffer[self.ptr]
        self.outputBuffer.append(val)

    def _getInputPtr(self):
        if len(self.inputBuffer)==0:
            return #no input available
        else:
            self.buffer[self.ptr] = self.inputBuffer.pop()

    def _doLoop(self):
        val = self.buffer[self.ptr]
        if val == 0:
            self.skipCount = self.skipCount+1
            self._doSkip() # loop stop condition met, so we skip code
        else:
            self.loopPos.append(self.codePtr-1)

    def _doEndLoop(self):
        self.codePtr = self.loopPos[-1]
        self.loopPos = self.loopPos[:-1]


    def _doSkip(self):
        while(self.skipCount >0):
            c = self.getChar()
            if c == -1:
                self.warningCodeUnended = True
                return

            if c == ']':
                self.skipCount = self.skipCount-1

            if c == '[':
                self.skipCount = self.skipCount+1

    #########################
    ## Outter Code         ##
    #########################

    def setCode(self,code):
        self.code = code
        self.codePtr = 0

    def getChar(self):

        if (self.codePtr == len(self.code)-1):
            return -1
        else:
            val =self.code[self.codePtr]
            self.codePtr = self.codePtr+1
            return val

    def _parseOper(self):
        val = self.getChar()

        if val == -1:
            return 0
        elif val == '>':
            self._ptrRight()
        elif val == '<':
            self._ptrLeft()
        elif val == '+':
            self._ptrValUp()
        elif val == '-':
            self._ptrValDown()
        elif val == '.':
            self._outputPtr()
        elif val == ',':
            self._getInputPtr()
        elif val == '[':
            self._doLoop()
        elif val == ']':
            self._doEndLoop()
        else:
            print "Unknown symbol in code:",val
            return 1
        self.instCount = self.instCount +1

        if self.instCount >8000: #possibly wrong code with loops
            self.warningLoops = True
            return 2

        return -1


    def parseCode(self):
        if len(self.code)==0:
            return

        ended = False
        while(ended == False):
            result = self._parseOper()
            if (result>=0):
                ended = True

        return self.outputBuffer
