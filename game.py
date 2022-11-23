
import numpy as np
import sha1
import matplotlib.pylab as plt
from dotenv import dotenv_values

globaltaps=[1,0,1,0,0,0,1,0,0,1]
#The taps for a hardware lfsr can usually be found and how many bits are there in the lfsr

class Lfsr:
    
    def __init__(self,state,taps) -> None:
        self.state=state
        self.taps=taps
        self.history=[]
        self.count=0
        self.out=self.state[-1]

    def next(self):
        # print(self.state)
        self.out= self.state[-1]
        self.history=[self.out]+self.history
        
        for i in range(len(self.state)-1,0,-1):
            self.state[i]=self.state[i-1]
        
        temp=0

        for i in range(len(self.taps)):
            if self.taps[i]==1:
                temp=temp^self.state[i]
            # temp=temp^self.state[i]

        self.state[0]=temp

        self.count+=1

        return self.history

    def showState(self):
        print(self.state)
        return self.state

class Game:


    def __init__(self) -> None:
        
        self.temp= globaltaps
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
        
        self.clienthash=sha1.sha1(input("Enter the client seed to hash and store \n"))
        print(self.clienthash)

        checkrandomness(self.state)

        self.hash=sha1.sha1(self.privatekey+str(self.nonce))
        state=self.state
              
        taps=globaltaps
        lfsr=Lfsr(state,taps)
        
        self.updateState()
        
        [lfsr.next() for i in range(10)]

        randomVal=lfsr.state
        print("state",lfsr.history,lfsr.state)
        
        randomVal=list(map((lambda x: str(x)),randomVal))
        randomVal="".join(randomVal)
        
        randomVal=int(randomVal,2)

        randomVal=round(randomVal)       

        self.result=randomVal
        self.secondhash=sha1.sha1(self.hash+self.clienthash+str(randomVal))

        print("\n\nThis is the final Hash",self.secondhash)
        # print("\nThis is the serverside hash",self.hash)
        # print("\nThis is the clientside hash",self.clienthash)

    
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
        print("The server side hash is",self.hash,"\nThe client side hash is",self.clienthash,"\nand the hash is sha1 (",self.hash,"+", self.clienthash,"+", str(self.result)+")" )

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
    taps=globaltaps

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

    # plt.plot(x, y)
    # plt.show()

if __name__=='__main__':
    
    game=Game()
    # l=Lfsr([0, 0, 1, 0, 1, 0, 1, 0, 0, 0],globaltaps)

    # for i in range(10):
    #     l.next()
    #     l.showState()



        