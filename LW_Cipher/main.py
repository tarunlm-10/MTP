from JLCrypto import JoyeLibert
from PRF import PRF
import random
import gmpy2
import time

class LabHE:
    def __init__(self,lamda):
        self.lamda = lamda
        self.sk = None
        self.pk = None
        self.obj = JoyeLibert(self.lamda)
        self.k = 128

    def KeyGen(self):
        
        sk_, pk = self.obj.generate_keypair()
        seed = random.randint(2**(self.k-1) + 1,2**self.k)
        self.sk = (sk_,seed)
        self.pk = pk
        return None
    
    def Encrypt_OFF(self,label):
        b = PRF(self.sk[1],label,2**self.k)
        ctx = self.obj.encrypt(b)
        return (b,ctx)
    
    def Encrypt_ON(self,m,C_off):
        b, beta = C_off
        a = m-b
        return (a,beta)
    

    def Decrypt_OFF(self,P):
        op, data = P
        b_i = []
        for i in data:
            temp = PRF(self.sk[1],i,2**self.k)
            b_i.append(temp)
        b = self.lab_prog(op,b_i)
        return b
    

    def Decrypt_ON(self,cipher,b):

        if len(cipher) == 2:
            return cipher[0]+b     

        else:
            m_ = self.obj.decrypt(cipher[0])
            return m_+b   

    def Decrypt2(self,cipher):
        b = self.obj.decrypt(cipher[1])
        return b

    def homomorphic_add(self,data):
        a = data[0][0]
        beta = data[0][1]
        for a_i,beta_i in data[1:]:
            a+=a_i
            beta = self.obj.add(beta,beta_i)
        return (a,beta)
        

    def homomorphic_mul(self,data):
        a = data[0][0]
        beta = data[0][1]
        temp= None
        for a_i,beta_i in data[1:]:
            temp = self.obj.encrypt((a*a_i)% 2**self.k)
            temp = temp + gmpy2.powmod(beta_i,a,self.pk.n)
            temp = temp + gmpy2.powmod(a_i,beta,self.pk.n)
        print(temp)
        return [temp]
            

    def cons_mul(self,c,cipher):
        if len(cipher)==1:
            return ((cipher[0]**c)%self.pk.n)
        else:
            return (c*cipher[0],(cipher[1]**c)%self.pk.n)


    def lab_prog(self,op,inp):
        if op == "add":
            return sum(inp) % self.pk.n
        elif op=="mul":
            temp=1
            for i in inp:
                temp=(temp*i)%self.pk.n
            return (temp)


if __name__ == "__main__":
    start = time.time()
    obj = LabHE(128)
    obj.KeyGen()
    end = time.time()
    m1,label1 = list(map(int,input("Enter an integer and its label: ").split()))
    m2,label2 = list(map(int,input("Enter an integer and its label: ").split()))

    C_off1 = obj.Encrypt_OFF(label1)
    C_off2 = obj.Encrypt_OFF(label2)
    ctx1 = obj.Encrypt_ON(m1,C_off1)
    ctx2 = obj.Encrypt_ON(m2,C_off2)

    Query = ("add",[1,2])
    data = [ctx1,ctx2]
    ctx = obj.homomorphic_add(data)
    skp = obj.Decrypt_OFF(Query)
    ans = obj.Decrypt_ON(ctx,skp)
    Query2 = ("mul",[1,2])
    ct2 = obj.homomorphic_mul(data)
    skp1 = obj.Decrypt_OFF(Query2)
    ans2 = obj.Decrypt_ON(ct2,skp1)
    print(ans)
    print(ans2)
    # ct2 = obj.cons_mul(2,ctx1)
    # ans2 = obj.Decrypt2(ct2)
    # print(ct2[0] + ans2)





