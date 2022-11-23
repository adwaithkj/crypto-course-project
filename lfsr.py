if __name__=='__main__':
    pass

class lfsr:
    def __init__(self,state,taps) -> None:
        self.state=state
        self.taps=taps
        self.history=[]
        self.count=0
        print("welcome to the program")
    def next(self):
        self.out= self.state[-1]
        self.history=[self.out]+self.history
        
        for i in range(len(self.state)-1,0,-1):
            self.state[i]=self.state[i-1]
        
        temp=0

        for i in self.taps:
            temp=temp^self.state[i]

        self.state[0]=temp

        self.count+=1

        return self.history

    def showState(self):
        return self.state

# state=[0,1,0,1,0,1]
# taps=[0,1,3]
# new=lfsr(state,taps)

# print(new.state)
# print(new.next())
# print(new.state)
# print(new.next())
# print(new.state)
# print(new.next())
# print(new.state)
# print(new.next())
# print(new.state)
# print(new.next())
# print(new.state)
# print(new.next())





