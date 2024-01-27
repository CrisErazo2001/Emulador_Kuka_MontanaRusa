import math
import numpy as np
import matplotlib.pyplot as plt
from crearCodigo import get4 as data
from crearCodigo import timeblock as tb
from crearCodigo import timeblockPTP as ptp
from crearCodigo import create_SPL_nV as nspl
from crearCodigo import create_SPTP_nV as sptp
from crearCodigo import create_SPL as splV
from crearCodigo import create_SPTP as sptpV
from crearCodigo import create_PTP as kptp
from dual_quaternion2 import Dual_quaternion


# ;CON ESTA BASE Y HERRAMIENTA
# ;Z+ VA AL FRENTE
# ;Y+ VA PARA ABAJO
# ;X+ VA PARA LA IZQUIERDA
# ;A+ gira en esta Z a la derecha
# ;B+ gira en esta Y a la derecha
# ;C+ gira en esta X hacia arriba


x2 = []
y2 = []
z2 = []

x1 = []
y1 = []
z1 = []
yR1 = []
y21 = []

escala = 3
frontlim = 100

pos,vel,rot = data()

posaux = []

quat = []
quatR = []

quatV = []
quatVR = []


xR = []
yR = []
zR = [] 

t = []
tR = []

x = []
y = []
z = [] 

a = [] #represents rotation around the z-axis (yaw)
b = [] #represents rotation around the y-axis (pitch)
c = [] #represents rotation around the x-axis (roll)

aR = [] #represents rotation around the z-axis (yaw)
bR = [] #represents rotation around the y-axis (pitch)
cR = [] #represents rotation around the x-axis (roll)

posR =[]
rotR =[]

vel_lin = []
posaux = []
aAnt = 0 
bAnt = 0 
cAnt = 0

acc = []

velR = []

for p in pos:
    x.append(round(p[1],3))
    y.append(round(p[2],3))
    z.append(round(p[3],3))
    t.append(p[0])
    
# for v in vel:
#     vx = [round(p[1],3),round(-p[2],3),round(p[3],3)]
#     vel_lin.append(vx)

for r in rot:
    aAux =r[3]
    bAux =r[2]-180
    cAux =r[1]
    if aAux>180:
        aAux = aAux - 360
    if bAux>180:
        bAux = bAux - 360
    if cAux>180:
        cAux = cAux - 360
    if aAux<-180:
        aAux = aAux + 360
    if bAux<-180:
        bAux = bAux + 360
    if cAux<-180:
        cAux = cAux + 360
    a.append(aAux)
    b.append(bAux)
    c.append(cAux)
aant = 0
bant = 0
cant = 0
print(f" ti1 = {t.index(25.00437)} & ti2 = {t.index(33.66445)}")

for i in range(len(rot)):
    aaux = a[i]
    baux = b[i] * 90/360
    caux = c[i] * 120/360
    
    if ((i >= t.index(12.66006)) & (i < t.index(32.00077))): #LOOP unicamente
        print(f"i = {i} loop")
        baux = 0
        aaux = 0

    aR.append(round(aaux,3))
    bR.append(round(abs(baux),3))
    cR.append(round(caux,3))
    aant = aaux
    bant = baux
    cant = caux


print(f"max a = {max(a)} min aR = {min(a)}")
print(f"max b = {max(b)} min bR = {min(b)}")
print(f"max c = {max(c)} min cR = {min(c)}")  


print(f"max aR = {max(aR)} min aR = {min(aR)}")
print(f"max bR = {max(bR)} min bR = {min(bR)}")
print(f"max cR = {max(cR)} min cR = {min(cR)}")    

for i in range(len(pos)): 
    q = Dual_quaternion(1,0,0,0,0,x[i],y[i],z[i])
    quat.append(q)
    if i>0:
        taux = t[i] - t[i-1]
    else:
        taux = 0.333
    tR.append(taux)
    # tR.append(0.33)

# for i in range(len(pos)): 
#     qV = Dual_quaternion(1,0,0,0,0,vel_lin[i][0],vel_lin[i][1],vel_lin[i][2])
#     quatV.append(qV)

print("-------------------------Posicion----------------------------")

print("Parte 1")
for i in range(0,t.index(12.66006),1): #Adelante 0
    
    # print(f"tiempo = {t[i]}, i = {i}")
    qR = quat[i]
    xaux = qR.b1
    yaux = qR.b2
    zaux = 4.32900*qR.b3-79.95670
    q = Dual_quaternion(1,0,0,0,0,xaux,yaux,zaux)
    quatR.append(q)
    if i == t.index(12.66006)-1:
        parte1 = [xaux,yaux,zaux]
    print(f"ang = {b[0]} tiempo = {t[i]}, i = {i} x = {xaux}, y = {yaux}, z = {zaux}")

print("Parte 2")
for i in range(t.index(12.66006),t.index(33.66445),1): #Subida y loop 0
    
    # print(f"tiempo = {t[i]}, i = {i}")
    qR = quat[i]
    Hr = Dual_quaternion(math.pi/180*-b[t.index(12.66006)],0,1,0,0,0,0,0)
    Hr = Hr.roTra()
    Hrc=Hr.conj()
    Ht = Dual_quaternion(0,0,0,0,0,-x[t.index(12.66006)],0,-z[t.index(12.66006)])
    Ht = Ht.roTra()
    Htc=Ht.conj()
    pF=Hr*Ht*qR*Htc*Hrc #asi si sirve como quiero
    
    xaux = pF.b1 + parte1[0]
    yaux = pF.b2
    # zaux = qR.b3/escala + parte2[2]
    zaux = 0.09365*(pF.b3+ parte1[2])+72.50689
    q = Dual_quaternion(1,0,0,0,0,xaux,yaux,zaux)
    quatR.append(q)
    # print(f"r = {b[t.index(33.66445)]} x = {xaux}, y = {yaux}, z = {zaux}")
    if i == t.index(33.66445)-1:
        parte2 = [xaux,yaux,pF.b3+ parte1[2]]
    print(f"ang = {b[t.index(33.66445)]} tiempo = {t[i]}, i = {i} x = {xaux}, y = {yaux}, z = {zaux}")

print("Parte 3")
for i in range(t.index(33.66445),t.index(35.66417),1): #giro a la izquierda pi/2
    
    qR = quat[i]
    Hr = Dual_quaternion(math.pi/180*-b[t.index(33.66445)],0,1,0,0,0,0,0)
    Hr = Hr.roTra()
    Hrc=Hr.conj()
    Ht = Dual_quaternion(0,0,0,0,0,-x[t.index(33.66445)],0,-z[t.index(33.66445)])
    Ht = Ht.roTra()
    Htc=Ht.conj()
    pF=Hr*Ht*qR*Htc*Hrc #asi si sirve como quiero
    
    xaux = pF.b1 + parte2[0]
    yaux = pF.b2
    # zaux = qR.b3/escala + parte2[2]
    zaux = 0.09365*(pF.b3+ parte2[2])+72.50689
    q = Dual_quaternion(1,0,0,0,0,xaux,yaux,zaux)
    quatR.append(q)
    # print(f"r = {b[t.index(33.66445)]} x = {xaux}, y = {yaux}, z = {zaux}")
    if i == t.index(35.66417)-1:
        parte3 = [xaux,yaux,pF.b3+ parte2[2]]
    print(f"ang = {b[t.index(33.66445)]} tiempo = {t[i]}, i = {i} x = {xaux}, y = {yaux}, z = {zaux}")

print("Parte 4")
for i in range(t.index(35.66417),t.index(38.33459),1): #giro a la derecha 0
    
    
    qR = quat[i]
    Hr = Dual_quaternion(math.pi/180*-b[t.index(35.66417)],0,1,0,0,0,0,0)
    Hr = Hr.roTra()
    Hrc=Hr.conj()
    Ht = Dual_quaternion(0,0,0,0,0,-x[t.index(35.66417)],0,-z[t.index(35.66417)])
    Ht = Ht.roTra()
    Htc=Ht.conj()
    pF=Hr*Ht*qR*Htc*Hrc #asi si sirve como quiero
    xaux = pF.b1 + parte3[0]
    yaux = pF.b2
    # zaux = qR.b3/escala + parte3[2]
    zaux = 0.09365*(pF.b3+ parte3[2])+72.50689
    q = Dual_quaternion(1,0,0,0,0,xaux,yaux,zaux)
    quatR.append(q)
    if i == t.index(38.33459)-1:
        parte4 = [xaux,yaux,pF.b3+ parte3[2]]
    print(f"ang = {b[t.index(35.66417)]} tiempo = {t[i]}, i = {i} x = {xaux}, y = {yaux}, z = {zaux}")

print("Parte 5")
for i in range(t.index(38.33459),t.index(40.00222),1): #giro a la derecha -pi/2
    
    # print(f"tiempo = {t[i]}, i = {i}")
    qR = quat[i]
    Hr = Dual_quaternion(math.pi/180*-b[t.index(38.33459)],0,1,0,0,0,0,0)
    Hr = Hr.roTra()
    Hrc=Hr.conj()
    Ht = Dual_quaternion(0,0,0,0,0,-x[t.index(38.33459)],0,-z[t.index(38.33459)])
    Ht = Ht.roTra()
    Htc=Ht.conj()
    pF=Hr*Ht*qR*Htc*Hrc #asi si sirve como quiero
    xaux = pF.b1 + parte4[0]
    yaux = pF.b2
    # zaux = qR.b3/escala + parte4[2]
    zaux = 0.09365*(pF.b3+ parte4[2])+72.50689
    q = Dual_quaternion(1,0,0,0,0,xaux,yaux,zaux)
    quatR.append(q)

    if i == t.index(40.00222)-1:
        parte5 = [xaux,yaux,pF.b3+ parte4[2]]
    print(f"ang = {b[t.index(38.33459)]} tiempo = {t[i]}, i = {i} x = {xaux}, y = {yaux}, z = {zaux}")

print("Parte 6")
for i in range(t.index(40.00222),t.index(46.00183),1): #giro a la derecha -pi
    # print(f"tiempo = {t[i]}, i = {i}")
    qR = quat[i]
    Hr = Dual_quaternion(math.pi/180*-b[t.index(40.00222)],0,1,0,0,0,0,0)
    Hr = Hr.roTra()
    Hrc=Hr.conj()
    Ht = Dual_quaternion(0,0,0,0,0,-x[t.index(40.00222)],0,-z[t.index(40.00222)])
    Ht = Ht.roTra()
    Htc=Ht.conj()
    pF=Hr*Ht*qR*Htc*Hrc #asi si sirve como quiero
    xaux = pF.b1 + parte5[0]
    yaux = pF.b2
    # zaux = qR.b3/escala + parte5[2]
    zaux = 0.09365*(pF.b3+ parte5[2])+72.50689
    q = Dual_quaternion(1,0,0,0,0,xaux,yaux,zaux)
    quatR.append(q)
    if i == t.index(46.00183)-1:
        parte6 = [xaux,yaux,pF.b3+ parte5[2]]
    print(f"ang = {b[t.index(40.00222)]} tiempo = {t[i]}, i = {i} x = {xaux}, y = {yaux}, z = {zaux}")

print("Parte 7")
for i in range(t.index(46.00183),t.index(49.00167),1): #giro a la derecha pi/2
    # print(f"tiempo = {t[i]}, i = {i}")
    qR = quat[i]
    # h1 = Dual_quaternion(b[t.index(46.00183)]*math.pi/180,0,1,0,0,z[t.index(46.00183)],0,-x[t.index(46.00183)])
    Hr = Dual_quaternion(math.pi/180*-b[t.index(46.00183)],0,1,0,0,0,0,0)
    Hr = Hr.roTra()
    Hrc=Hr.conj()
    Ht = Dual_quaternion(0,0,0,0,0,-x[t.index(46.00183)],0,-z[t.index(46.00183)])
    Ht = Ht.roTra()
    Htc=Ht.conj()
    pF=Hr*Ht*qR*Htc*Hrc #asi si sirve como quiero
    xaux = pF.b1 + parte6[0]
    yaux = pF.b2
    # zaux = qR.b3/escala + parte6[2]
    zaux =0.09365*( pF.b3+ parte6[2])+72.50689
    q = Dual_quaternion(1,0,0,0,0,xaux,yaux,zaux)
    quatR.append(q)
    if i == t.index(49.00167)-1:
        parte7 = [xaux,yaux,pF.b3+ parte6[2]]
    print(f"ang = {b[t.index(46.00183)]} tiempo = {t[i]}, i = {i} x = {xaux}, y = {yaux}, z = {zaux}")

print("Parte 8")
for i in range(t.index(49.00167),t.index(56.33488),1): #giro a la derecha -pi/2
    # print(f"tiempo = {t[i]}, i = {i}")
    qR = quat[i]
    Hr = Dual_quaternion(math.pi/180*-b[t.index(49.00167)],0,1,0,0,0,0,0)
    Hr = Hr.roTra()
    Hrc=Hr.conj()
    Ht = Dual_quaternion(0,0,0,0,0,-x[t.index(49.00167)],0,-z[t.index(49.00167)])
    Ht = Ht.roTra()
    Htc=Ht.conj()
    pF=Hr*Ht*qR*Htc*Hrc #asi si sirve como quiero
    xaux = pF.b1 + parte7[0]
    yaux = pF.b2
    # zaux = qR.b3/escala + parte7[2]
    zaux = 0.09365*(pF.b3+ parte7[2])+72.50689
    q = Dual_quaternion(1,0,0,0,0,xaux,yaux,zaux)
    quatR.append(q)
    if i == t.index(56.33488)-1:
        parte8 = [xaux,yaux,pF.b3+ parte7[2]]
    print(f"ang = {b[t.index(49.00167)]} tiempo = {t[i]}, i = {i} x = {xaux}, y = {yaux}, z = {zaux}")

print("Parte 9")
for i in range(t.index(56.33488),t.index(63.33273),1): #giro a la izquierda pi/2
    # print(f"tiempo = {t[i]}, i = {i}")
    qR = quat[i]
    # h1 = Dual_quaternion(b[t.index(56.33488)]*math.pi/180,0,1,0,0,-z[t.index(56.33488)],0,x[t.index(56.33488)])
    Hr = Dual_quaternion(math.pi/180*-b[t.index(56.33488)],0,1,0,0,0,0,0)
    Hr = Hr.roTra()
    Hrc=Hr.conj()
    Ht = Dual_quaternion(0,0,0,0,0,-x[t.index(56.33488)],0,-z[t.index(56.33488)])
    Ht = Ht.roTra()
    Htc=Ht.conj()
    pF=Hr*Ht*qR*Htc*Hrc #asi si sirve como quiero
    xaux = pF.b1 + parte8[0]
    yaux = pF.b2
    # zaux = pF.b3/escala + parte8[2]
    zaux = 0.09365*(pF.b3+ parte8[2])+72.50689
    q = Dual_quaternion(1,0,0,0,0,xaux,yaux,zaux)
    quatR.append(q)
    if i == t.index(63.33273)-1:
        parte9 = [xaux,yaux,pF.b3+ parte8[2]]
    print(f"ang = {b[t.index(56.33488)]} tiempo = {t[i]}, i = {i} x = {xaux}, y = {yaux}, z = {zaux}")

print("Parte 10")
for i in range(t.index(63.33273),len(t),1): #Adelante final 0
    
    # print(f"tiempo = {t[i]}, i = {i}")
    qR = quat[i]
    # h1 = Dual_quaternion(b[t.index(63.33273)]*math.pi/180,0,1,0,0,x[t.index(63.33273)],0,-1*z[t.index(63.33273)])
    Hr = Dual_quaternion(math.pi/180*-b[t.index(63.33273)],0,1,0,0,0,0,0)
    Hr = Hr.roTra()
    Hrc=Hr.conj()
    Ht = Dual_quaternion(0,0,0,0,0,-x[t.index(63.33273)],0,-z[t.index(63.33273)])
    Ht = Ht.roTra()
    Htc=Ht.conj()
    pF=Hr*Ht*qR*Htc*Hrc #asi si sirve como quiero
    # xaux = pF.b1
    # yaux = pF.b2
    # zaux = pF.b3*0.01889*frontlim-0.00018*frontlim + 100
    xaux = pF.b1 + parte9[0]
    yaux = pF.b2
    # zaux = 1.88928*pF.b3 + 99.98110
    zaux = 1.22803*pF.b3 + 129.98771
    q = Dual_quaternion(1,0,0,0,0,xaux,yaux,zaux)
    quatR.append(q)
    print(f"ang = {b[t.index(63.33273)]} tiempo = {t[i]}, i = {i} x = {xaux}, y = {yaux}, z = {zaux}")



# ;CON ESTA BASE Y HERRAMIENTA
# ;Z+ VA AL FRENTE
# ;Y+ VA PARA ABAJO
# ;X+ VA PARA LA IZQUIERDA // derecha??
# ;A+ gira en esta Z a la derecha
# ;B+ gira en esta Y a la derecha
# ;C+ gira en esta X hacia arriba

print(len(pos))
print(len(rot))

for v in quatVR:
    vaux = math.sqrt((v.b1/2)**2 + (v.b2/4)**2+ (v.b3)**2 )
    velR.append(round(vaux/1000,3))




for i in range(len(quatR)):
    xraux = round(quatR[i].b1,3)
    yraux = round(quatR[i].b2,3)
    zraux = round(quatR[i].b3,3)

    x2.append(xraux)
    y2.append(yraux)
    z2.append(zraux)



for i in range(len(quatR)):
    xraux = round(quatR[i].b1*escala,3)
    yraux = round(-quatR[i].b2*escala,3)
    zraux = round(quatR[i].b3,3)

    xR.append(xraux)
    yR.append(yraux)
    zR.append(zraux)

    posaux.append([xraux,yraux,zraux])

for i in range(1,len(pos)):
    #vel_lin.append(round(v[2],2))        
    aux2 = list(map(lambda x,y: x - y, posaux[i], posaux[i-1]))
    des =  math.sqrt(aux2[0]**2 + aux2[1]**2 + aux2[2]**2)
    
    v = (des/1000)/tR[i]
    if v == 0:
        vel_lin.append(0.1)
        continue
    print(round(v,4))
    vel_lin.append(round(v*0.7,8))

print(f"max x = {max(x)} min x = {min(x)}")
print(f"max y = {max(y)} min y = {min(y)}")
print(f"max z = {max(z)} min z = {min(z)}")

print(f"max x2 = {max(x2)} min x2 = {min(x2)}")
print(f"max y2 = {max(y2)} min y2 = {min(y2)}")
print(f"max z2 = {max(z2)} min z2 = {min(z2)}")

print(f"max xR = {max(xR)} min xR = {min(xR)}")
print(f"max yR = {max(yR)} min yR = {min(yR)}")
print(f"max zR = {max(zR)} min zR = {min(zR)}")







# for i in range(len(quatR)):
#     pAux = np.array([xR[i],yR[i],zR[i]])
#     rAux = np.array([aR[i],bR[i],cR[i]])
#     vAux = np.array([vel_lin[i][1],vel_lin[i][2],vel_lin[i][3]])
#     accaux = np.array(acc[i])


sptp(xR,yR,zR,aR,bR,cR)
nspl(xR,yR,zR,aR,bR,cR)
tb(xR,yR,zR,aR,bR,cR,tR,max(t))
ptp(xR,yR,zR,aR,bR,cR,tR,71)
splV(xR,yR,zR,aR,bR,cR,vel_lin)
sptpV(xR,yR,zR,aR,bR,cR,vel_lin)
kptp(xR,yR,zR,aR,bR,cR,vel_lin)
# Grafica

for p in pos:
    x1.append(round(p[1],3))
    y1.append(round(p[2],3))
    z1.append(round(p[3],3))
for k in yR:
    yR1.append(-k)
for k in y2:
    y21.append(-k)

fig = plt.figure(figsize=(10,7))
fig2 = plt.figure(figsize=(10,7))
fig4 = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111, projection='3d')
ax2 = fig2.add_subplot(111, projection='3d')
ax4 = fig4.add_subplot(111, projection='3d')

surf = ax.scatter(x1, z1, y1)
surf = ax.scatter(x1[0], z1[0], y1[0], color = 'r',s = 100)
surf = ax.scatter(x1[t.index(12.66006)], z1[t.index(12.66006)], y1[t.index(12.66006)], color = 'green',s = 100)
surf = ax.scatter(x1[t.index(33.66445)], z1[t.index(33.66445)], y1[t.index(33.66445)], color = 'green',s = 50)
surf = ax.scatter(x1[t.index(35.66417)], z1[t.index(35.66417)], y1[t.index(35.66417)], color = 'green',s = 50)
surf = ax.scatter(x1[t.index(38.33459)], z1[t.index(38.33459)], y1[t.index(38.33459)], color = 'green',s = 50)
surf = ax.scatter(x1[t.index(40.00222)], z1[t.index(40.00222)], y1[t.index(40.00222)], color = 'green',s = 50)
surf = ax.scatter(x1[t.index(46.00183)], z1[t.index(46.00183)], y1[t.index(46.00183)], color = 'green',s = 50)
surf = ax.scatter(x1[t.index(49.00167)], z1[t.index(49.00167)], y1[t.index(49.00167)], color = 'green',s = 50)
surf = ax.scatter(x1[t.index(56.33488)], z1[t.index(56.33488)], y1[t.index(56.33488)], color = 'green',s = 50)
surf = ax.scatter(x1[t.index(63.33273)], z1[t.index(63.33273)], y1[t.index(63.33273)], color = 'green',s = 50)
surf = ax.plot(x1, z1, y1, color = 'c')
surf = ax2.scatter(x2, z2, y2)
surf = ax2.plot(x2, z2, y2, color = 'c')
surf = ax2.scatter(x2[t.index(12.66006)], z2[t.index(12.66006)], y2[t.index(12.66006)], color = 'green',s = 50)
surf = ax2.scatter(x2[t.index(33.66445)], z2[t.index(33.66445)], y2[t.index(33.66445)], color = 'green',s = 50)
surf = ax2.scatter(x2[t.index(35.66417)], z2[t.index(35.66417)], y2[t.index(35.66417)], color = 'green',s = 50)
surf = ax2.scatter(x2[t.index(38.33459)], z2[t.index(38.33459)], y2[t.index(38.33459)], color = 'green',s = 50)
surf = ax2.scatter(x2[t.index(40.00222)], z2[t.index(40.00222)], y2[t.index(40.00222)], color = 'green',s = 50)
surf = ax2.scatter(x2[t.index(46.00183)], z2[t.index(46.00183)], y2[t.index(46.00183)], color = 'green',s = 50)
surf = ax2.scatter(x2[t.index(49.00167)], z2[t.index(49.00167)], y2[t.index(49.00167)], color = 'green',s = 50)
surf = ax2.scatter(x2[t.index(56.33488)], z2[t.index(56.33488)], y2[t.index(56.33488)], color = 'green',s = 50)
surf = ax2.scatter(x2[t.index(63.33273)], z2[t.index(63.33273)], y2[t.index(63.33273)], color = 'green',s = 50)
surf = ax4.scatter(xR, zR, yR)
surf = ax4.plot(xR, zR, yR, color = 'c')
surf = ax4.scatter(xR[t.index(12.66006)], zR[t.index(12.66006)], yR[t.index(12.66006)], color = 'green',s = 50)
surf = ax4.scatter(xR[t.index(33.66445)], zR[t.index(33.66445)], yR[t.index(33.66445)], color = 'green',s = 50)
surf = ax4.scatter(xR[t.index(35.66417)], zR[t.index(35.66417)], yR[t.index(35.66417)], color = 'green',s = 50)
surf = ax4.scatter(xR[t.index(38.33459)], zR[t.index(38.33459)], yR[t.index(38.33459)], color = 'green',s = 50)
surf = ax4.scatter(xR[t.index(40.00222)], zR[t.index(40.00222)], yR[t.index(40.00222)], color = 'green',s = 50)
surf = ax4.scatter(xR[t.index(46.00183)], zR[t.index(46.00183)], yR[t.index(46.00183)], color = 'green',s = 50)
surf = ax4.scatter(xR[t.index(49.00167)], zR[t.index(49.00167)], yR[t.index(49.00167)], color = 'green',s = 50)
surf = ax4.scatter(xR[t.index(56.33488)], zR[t.index(56.33488)], yR[t.index(56.33488)], color = 'green',s = 50)
surf = ax4.scatter(xR[t.index(63.33273)], zR[t.index(63.33273)], yR[t.index(63.33273)], color = 'green',s = 50)
# Personaliza el gráfico
ax.set_xlabel('Eje X')
ax.set_ylabel('Eje Z')
ax.set_zlabel('Eje Y')

ax2.set_xlabel('Eje X')
ax2.set_ylabel('Eje Z')
ax2.set_zlabel('Eje Y')

ax4.set_xlabel('Eje X')
ax4.set_ylabel('Eje Z')
ax4.set_zlabel('Eje Y')

# ax.set_title('Recorrido obtenido de Unity')
ax2.set_title('Recorrido generado tras reorientacion')
ax4.set_title('Recorrido generado para el robot')

fig3, ax3 = plt.subplots()
ax3.scatter(xR[1:],zR[1:])
ax3.scatter(xR[0],zR[0],color = 'r')
ax3.set_xlabel('Eje X')
ax3.set_ylabel('Eje Z')

fig5, ax5= plt.subplots()
ax5.scatter(x,z)
ax5.scatter(x[1:],z[1:],color = 'royalblue')
ax5.scatter(x[0],z[0],color = 'r')
ax5.set_xlabel('Eje X')
ax5.set_ylabel('Eje Z')

# Muestra el gráfico
plt.show()