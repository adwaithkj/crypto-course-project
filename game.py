
import numpy as np
import sha1
import matplotlib.pylab as plt
from dotenv import dotenv_values

class Lfsr:
    
    def __init__(self,state,taps) -> None:
        self.state=state
        self.taps=taps
        self.history=[]
        self.count=0
        self.out=self.state[-1]

    def next(self):
        self.out= self.state[-1]
        self.history=[self.out]+self.history
        
        for i in range(len(self.state)-1,0,-1):
            self.state[i]=self.state[i-1]
        
        temp=0

        for i in range(len(self.taps)):
            temp=temp^self.state[i]

        self.state[0]=temp

        self.count+=1

        return self.history

    def showState(self):
        return self.state

class Game:


    def __init__(self) -> None:
        # self.state=np.random.randint(2,size=10)
        self.temp= np.random.randint(2,size=10)
        self.privatekey=dotenv_values("./.env")["PRIVATE_KEY"]
        self.nonce=0
        self.hash=sha1.sha1(self.privatekey+str(self.nonce))

        self.updateState()
        self.play()

    def updateState(self):
        temp_str = self.hash
        res = ''.join(format(ord(i), '08b') for i in temp_str)

        seed=[]
        for i in range(10):
            seed.append(int(res[i]))
        self.state=seed

    def play(self):
        

        checkrandomness(self.state)

        self.hash=sha1.sha1(self.privatekey+str(self.nonce))
        state=self.state
        temp=[0,0,1,0,1,0,0,1,1,1]
        
        taps=[]
        for i,j in enumerate(temp):
            if j==1:
                taps.append(i)
        

        lfsr=Lfsr(state,taps)
        
        self.updateState()
        
        [lfsr.next() for i in range(10)]

        randomVal=lfsr.history
        randomVal=list(map((lambda x: str(x)),randomVal))
        randomVal="".join(randomVal)
        
        randomVal=int(randomVal,2)

        randomVal=round(randomVal/1024*1000)       

        self.result=randomVal
        self.secondhash=sha1.sha1(self.hash+str(randomVal))

        print("\n\nThis is the hash of the result",self.secondhash)
        print("\nAnd this is the serverside hash",self.hash)

    
        self.nonce+=1
        self.prompt()



    def prompt(self):
        print("\n\nWelcome to the Crypto Casino\nPlease choose a number from 0 to 1024")
        self.guess=input()

        self.evaluate()

    def evaluate(self):
        if self.result==self.guess:
            print("Congrats, you have won the lot")
        else:
            print("Better luck next time\n\nNumber",self.result ,"has won the lot")

        print("Press p to play again, d to raise dispute")

        i=input()

        if i=="p":
            self.play()
        elif i=="d":
            self.raiseDispute()
        else:
            pass
    def raiseDispute(self):
        print("The server side hash is",self.hash,"and the hash is sha1 (",self.hash,"+" , str(self.result)+")" )

        print("Press p to play again, d to raise dispute")

        i=input()

        if i=="p":
            self.play()
        elif i=="d":
            self.raiseDispute()
        else:
            pass


def checkrandomness(state):

    # state=[1,0,0,0,1,0,0,0,1,0]
    state=state
    taps=[0,0,1,0,1,0,0,1,1,1]

    print(state,taps)
    l=Lfsr(state,taps)
    arr=[]
    
    for i in range(10000):
        l.next()
        arr=arr+[list(l.state)]
    nums=[]
    
    for i in arr:
        randomVal=i
        randomVal=list(map((lambda x: str(x)),randomVal))
        randomVal="".join(randomVal)
        
        randomVal=int(randomVal,2)

        randomVal=round(randomVal)   

        nums.append(randomVal)
    
    d={}
    for i in nums:
        if i not in d:
            d[i]=1
        else:
            d[i]=d[i]+1

    for i in range(1000):
        if i not in d:
            d[i]=0
    
    lists = sorted(d.items()) # sorted by key, return a list of tuples
    
    # print(lists)

    m=max(d.values())

    print("These are the most occuring values")

    vals=[]
    for i in lists:
        if i[1]==m:
            vals.append(i[0])

    print("Select from the following values")
    print(vals)

    x, y = zip(*lists) # unpack a list of pairs into two tuples

    plt.plot(x, y)
    plt.show()

if __name__=='__main__':
    
    game=Game()



        