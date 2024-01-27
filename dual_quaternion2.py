import numpy as np
import math

'''Librería para quaternios duales
desarrollada por ´in the name of God´: Juan De Grijalva PhD'''

class Dual_quaternion():

  
    def __init__(self,a0,a1,a2,a3,b0,b1,b2,b3):
        self.a0=a0
        self.a1=a1
        self.a2=a2
        self.a3=a3
        self.b0=b0
        self.b1=b1
        self.b2=b2
        self.b3=b3
      

    def sdq(self):   #a,alfa,d,teta
        a=math.cos(self.a1/2)*math.cos(self.a3/2)
        b=math.sin(self.a1/2)*math.cos(self.a3/2)
        c=math.sin(self.a1/2)*math.sin(self.a3/2)
        d=math.cos(self.a1/2)*math.sin(self.a3/2)
        e=self.a0/2
        f=self.a2/2
        h=Dual_quaternion(a,b,c,d,-e*b-f*d,e*a-f*c,e*d+f*b,-e*c+f*a)
        return h

    #def __str__(self):
    #    return '[{0} {1}i {2}j {3}k {4}\u03B5 {5}\u03B5 {6}\u03B5 {7}\u03B5]'.format(self.a0,self.a1,self.a2,self.a3,self.a4,self.a5,self.a6,self.a7,self.a8)
    def __str__(self):
        return '[{0} {1}i {2}j {3}k \u03B5{4} \u03B5{5}i \u03B5{6}j \u03B5{7}k]'.format(self.a0,self.a1,self.a2,self.a3,self.b0,self.b1,self.b2,self.b3)
    def __add__(self,otherQ):
        q=Dual_quaternion(self.a0+otherQ.a0,self.a1+otherQ.a1,self.a2+otherQ.a2,self.a3+otherQ.a3,self.b0+otherQ.b0,self.b1+otherQ.b1,self.b2+otherQ.b2,self.b3+otherQ.b3)
        return q
    def __mul__(self,otherDQ):
        aux1=np.array([[self.a0,-self.a1,-self.a2,-self.a3],
                       [self.a1,self.a0,-self.a3,self.a2],
                       [self.a2,self.a3,self.a0,-self.a1],
                       [self.a3,-self.a2,self.a1,self.a0]])
        aux2=np.array([otherDQ.a0,otherDQ.a1,otherDQ.a2,otherDQ.a3])
        aux3=aux2.T
        aux=np.round(aux1@aux3,2)
        #h1=self.q11*otherDQ.q21
        #h2=self.q11*otherDQ.q22+self.q12*otherDQ.q21
        aux4=np.array([[self.a0,-self.a1,-self.a2,-self.a3],
                       [self.a1,self.a0,-self.a3,self.a2],
                       [self.a2,self.a3,self.a0,-self.a1],
                       [self.a3,-self.a2,self.a1,self.a0]])
        aux5=np.array([otherDQ.b0,otherDQ.b1,otherDQ.b2,otherDQ.b3]).T
        aux6=np.round(aux4@aux5,2)
        aux7=np.array([[self.b0,-self.b1,-self.b2,-self.b3],
                       [self.b1,self.b0,-self.b3,self.b2],
                       [self.b2,self.b3,self.b0,-self.b1],
                       [self.b3,-self.b2,self.b1,self.b0]])
        aux8=np.array([otherDQ.a0,otherDQ.a1,otherDQ.a2,otherDQ.a3]).T
        aux9=np.round(aux7@aux8,2)
        aux10=np.round(aux6+aux9,2)
        h=Dual_quaternion(aux[0],aux[1],aux[2],aux[3],aux10[0],aux10[1],aux10[2],aux10[3])
        return h

    def conj(self):
        h=Dual_quaternion(self.a0,-self.a1,-self.a2,-self.a3,-self.b0,self.b1,self.b2,self.b3)
        return h
    
    def roTra(self): #theta,sx,sy,sz,0,tx,ty,tz
        aux_5 = math.sqrt(self.a1 ** 2 + self.a2 ** 2 + self.a3 ** 2)
        aux_4=math.cos(self.a0/2)
        if aux_5==0:
            aux_6=0
            aux_7 =0
            aux_8=0
        else:
            aux_6=(self.a1/aux_5)*math.sin(self.a0/2)
            aux_7 = (self.a2 / aux_5) * math.sin(self.a0 / 2)
            aux_8=(self.a3 / aux_5) * math.sin(self.a0/ 2)
        #---Segunda Parte-------
        aux7=np.array([[self.b0,-self.b1,-self.b2,-self.b3],
                       [self.b1,self.b0,-self.b3,self.b2],
                       [self.b2,self.b3,self.b0,-self.b1],
                       [self.b3,-self.b2,self.b1,self.b0]])
        
        aux8=np.array([aux_4,aux_6,aux_7,aux_8]).T
        aux9=0.5*np.round(aux7@aux8,2)     
                              
        h=Dual_quaternion(aux_4,aux_6,aux_7,aux_8,aux9[0],aux9[1],aux9[2],aux9[3])
        return h
    
    def lin(self): # Expresar un DQ como linea recta DQ=[0,lx,ly,lz,0,l0x,l0y,l0z]
        aux_1=np.array([self.a1,self.a2,self.a3])
        aux_2=np.array([self.b1,self.b2,self.b3])
        m=np.round(aux_2@aux_1,2)
        h=Dual_quaternion(0,self.a1,self.a2,self.a3,0,m[0],m[1],m[2])
        return h
    
    def linl0(self): #recuperar l0 de un DQ q representa una Linea Recta
        l=np.array([self.a1,self.a2,self.a3])
        m=np.array([self.b1,self.b2,self.b3])
        l0=np.round(l@m,2)
        return l0
    
    #def plano(self):
        
        
    

# q1=Quaternion(0.75,0.25,0.25,0.25)
# q2=Quaternion(0.25,0.25,0.25,0.25)  
# h1=Dual_quaternion(q1,q2)     
# h2=Dual_quaternion(q2,q1) 
# print(h2.conj())    
# print('Multiplicacion: {0}'.format(h1*h2))    
# h3=Dual_quaternion
# a1=50
# a2=30
# a3=20
# alfa1=3.14/2
# teta1=0
# d1=0
# print(h2.sdq(a1,alfa1,d1,teta1))

#-----Ejemplo Examen--------
            
# h1=Dual_quaternion(math.pi,0,0,1,0,10,4,0)
# h1=h1.roTra()
# h2=Dual_quaternion(3*math.pi/4,0,0,1,0,-10,5,0)
# h2=h2.roTra()
# p=Dual_quaternion(1,0,0,0,0,-2,3,0)
# h1c=h1.conj()
# h2c=h2.conj()
# R=h1*h2*p*h2c*h1c
# print(R)
#-----Ejemplo Radavelli--------
# h1=Dual_quaternion(math.pi/2,0,-1,0,0,0,0,2)
# R=h1.roTra()
# print(R)
#-----Ejemplo Barrientos--------
# h1=Dual_quaternion(math.pi/2,1,0,0,0,8,-4,12)
# h1=h1.roTra()
# p=Dual_quaternion(0,0,0,0,0,1,1,0)
# h1c=h1.conj()
# R=h1*p*h1c
# print(R)

