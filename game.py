
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
        self.state=np.random.randint(2,size=10)
        self.temp= np.random.randint(2,size=10)
        self.privatekey=dotenv_values("./.env")["PRIVATE_KEY"]
        self.nonce=0
        self.hash=sha1.sha1(self.privatekey+str(self.nonce))

        self.play()

    def play(self):
        self.hash=sha1.sha1(self.privatekey+str(self.nonce))
        state=self.state
        temp=self.temp
        
        taps=[]
        for i,j in enumerate(temp):
            if j==1:
                taps.append(i)
        

        lfsr=Lfsr(state,taps)
        self.state=state
        
        [lfsr.next() for i in range(10)]

        randomVal=lfsr.history
        randomVal=list(map((lambda x: str(x.item())),randomVal))
        randomVal="".join(randomVal)
        
        randomVal=int(randomVal,2)

        randomVal=round(randomVal/1024*1000)       

        self.result=randomVal
        self.secondhash=sha1.sha1(self.hash+str(randomVal))

        print("\n\nThis is the hash of the result",self.secondhash)
        
        self.nonce+=1
        self.prompt()



    def prompt(self):
        print("\n\nWelcome to the Crypto Casino\nPlease choose a 3 numbers")
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


def checkrandomness():
    state=np.random.randint(2,size=10)
    taps=np.random.randint(2,size=10)
    print(state,taps)
    l=Lfsr(state,taps)
    arr=[]
    
    for i in range(10000):
        l.next()
        arr=arr+[list(l.state)]
    nums=[]
    
    for i in arr:
        randomVal=i
        randomVal=list(map((lambda x: str(x.item())),randomVal))
        randomVal="".join(randomVal)
        
        randomVal=int(randomVal,2)

        randomVal=round(randomVal/1024*1000)   

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
    print(lists)
    x, y = zip(*lists) # unpack a list of pairs into two tuples

    plt.plot(x, y)
    plt.show()



if __name__=='__main__':
    checkrandomness()
    game=Game()


        