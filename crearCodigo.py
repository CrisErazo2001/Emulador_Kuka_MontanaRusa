#Funcion para generar codigo KRL movimientos con PTP con Velocidad
def create_PTP(x,y,z,A,B,C,vel_lin):
    file1 = open("ptpVel.txt","w")
    lenght = len(x)
    file1.writelines("$BASE = BASE_DATA[10]\n")
    file1.writelines("$TOOL = TOOL_DATA[10]\n")
    file1.writelines("$ADVANCE = 3\n")
    str =  "PTP {" + f"X {x[0]}, Y {y[0]}, Z {z[0]}, A {A[0]}, B {B[0]}, C {C[0]}"+ "} C_PTP\n"
    file1.writelines(str)
    for i in range(1,lenght,1):
        file1.writelines(f"$VEL.CP = {vel_lin[i-1]}\n")
        str =  "PTP {" + f"X {x[i]}, Y {y[i]}, Z {z[i]}, A {A[i]}, B {B[i]}, C {C[i]} "+  "} C_PTP\n"
        file1.writelines(str)
    file1.close()
#Funcion para generar codigo KRL movimientos con PTP sin Velocidad
def create_PTP_nV(x,y,z,A,B,C):
    file1 = open("ptp.txt","w")
    lenght = len(x)
    file1.writelines("$BASE = BASE_DATA[10]\n")
    file1.writelines("$TOOL = TOOL_DATA[10]\n")
    file1.writelines("$ADVANCE = 3\n")
    file1.writelines(str)
    for i in range(0,lenght,1):
        str =  "PTP {" + f"X {x[i]}, Y {y[i]}, Z {z[i]}, A {A[i]}, B {B[i]}, C {C[i]} "+  "} C_PTP\n"
        file1.writelines(str)
    file1.close()

#Funcion para generar codigo KRL movimientos con SPL con Velocidad
def create_SPL(x,y,z,A,B,C,vel_lin):
    file1 = open("splVel.txt","w")
    lenght = len(x)
    file1.writelines("$BASE = BASE_DATA[10]\n")
    file1.writelines("$TOOL = TOOL_DATA[10]\n")
    file1.writelines("$ADVANCE = 3\n")
    file1.writelines("SPLINE\n")
    str =  " SPL {" + f"X {x[0]}, Y {y[0]}, Z {z[0]}, A {A[0]}, B {B[0]}, C {C[0]}"+ "}\n"
    file1.writelines(str)
    
    for i in range(1,lenght,1):
        str =  " SPL {" + f"X {x[i]}, Y {y[i]}, Z {z[i]}, A {A[i]}, B {B[i]}, C {C[i]}"+ "} "+ f"WITH $VEL.CP = {vel_lin[i-1]}\n"
        file1.writelines(str)
    file1.writelines("ENDSPLINE\n") 
    file1.close()

#Funcion para generar codigo KRL movimientos con SPL SIN Velocidad
def create_SPL_nV(x,y,z,A,B,C):
    file1 = open("spl.txt","w")
    lenght = len(x)
    file1.writelines("$BASE = BASE_DATA[10]\n")
    file1.writelines("$TOOL = TOOL_DATA[10]\n")
    file1.writelines("$ADVANCE = 3\n")
    
    file1.writelines("SPLINE\n")
    for i in range(0,lenght,1):
        str =  " SPL {" + f"X {x[i]}, Y {y[i]}, Z {z[i]}, A {A[i]}, B {B[i]}, C {C[i]}"+ "} \n"
        file1.writelines(str)
    file1.writelines("ENDSPLINE\n")    
    file1.close()
#Funcion para generar codigo KRL movimientos con SPTP con Velocidad
def create_SPTP(x,y,z,A,B,C,vel_lin):
    file1 = open("sptpVel.txt","w")
    lenght = len(x)
    file1.writelines("$BASE = BASE_DATA[10]\n")
    file1.writelines("$TOOL = TOOL_DATA[10]\n")
    file1.writelines("$ADVANCE = 3\n")
    file1.writelines("PTP_SPLINE\n")
    str =  " SPTP {" + f"X {x[0]}, Y {y[0]}, Z {z[0]}, A {A[0]}, B {B[0]}, C {C[0]}"+ "}\n"
    file1.writelines(str)
    for i in range(1,lenght,1):
        str =  " SPTP {" + f"X {x[i]}, Y {y[i]}, Z {z[i]}, A {A[i]}, B {B[i]}, C {C[i]}"+ "} "+ f"WITH $VEL.CP = {vel_lin[i-1]}\n"
        file1.writelines(str)
    file1.writelines("ENDSPLINE\n")    
    file1.close()

#Funcion para generar codigo KRL movimientos con SPTP SIN Velocidad
def create_SPTP_nV(x,y,z,A,B,C):
    file1 = open("sptp.txt","w")
    lenght = len(x)
    file1.writelines("$BASE = BASE_DATA[10]\n")
    file1.writelines("$TOOL = TOOL_DATA[10]\n")
    file1.writelines("$ADVANCE = 3\n")
    file1.writelines("PTP_SPLINE\n")
    for i in range(0,lenght,1):
        str =  " SPTP {" + f"X {x[i]}, Y {y[i]}, Z {z[i]}, A {A[i]}, B {B[i]}, C {C[i]}"+ "} \n"
        file1.writelines(str)
    file1.writelines("ENDSPLINE\n")    
    file1.close()
#Funcion para generar codigo KRL TIME BLOCK con SPLINE block
def timeblock(x,y,z,A,B,C,t, t_total):
    file1 = open("time_block.txt","w")
    lenght = len(x)
    file1.writelines("$BASE = BASE_DATA[10]\n")
    file1.writelines("$TOOL = TOOL_DATA[10]\n")
    file1.writelines("SPLINE\n")
    str =  " SPL {" + f"X {x[0]}, Y {y[0]}, Z {z[0]}, A {A[0]}, B {B[0]}, C {C[0]}"+ "}\n"
    file1.writelines(str)
    file1.writelines(" TIME_BLOCK START\n")
    for i in range(1,lenght,1):
        str =  " SPL {" + f"X {x[i]}, Y {y[i]}, Z {z[i]}, A {A[i]}, B {B[i]}, C {C[i]}"+ "}\n"
        file1.writelines(str)
        file1.writelines(f" TIME_BLOCK PART = {round(100/(lenght-1),5)}\n")
    file1.writelines(f" TIME_BLOCK END = {t_total}\n")
    file1.writelines("ENDSPLINE\n")
    file1.close()
#Funcion para generar codigo KRL TIME BLOCK con PTP_SPLINE block
def timeblockPTP(x,y,z,A,B,C,t, t_total):
    count = 0
    file1 = open("time_blockptp.txt","w")
    lenght = len(x)
    file1.writelines("$BASE = BASE_DATA[10]\n")
    file1.writelines("$TOOL = TOOL_DATA[10]\n")
    file1.writelines("PTP_SPLINE\n")
    str =  " SPTP {" + f"X {x[0]}, Y {y[0]}, Z {z[0]}, A {A[0]}, B {B[0]}, C {C[0]}"+ "}\n"
    file1.writelines(str)
    file1.writelines(" TIME_BLOCK START\n")
    for i in range(1,lenght,1):
        str =  " SPTP {" + f"X {x[i]}, Y {y[i]}, Z {z[i]}, A {A[i]}, B {B[i]}, C {C[i]}"+ "}\n"
        file1.writelines(str)
        file1.writelines(f" TIME_BLOCK PART = {round(100/(lenght-1),5)}\n")
        count+=1
    file1.writelines(f" TIME_BLOCK END = {t_total}\n")
    file1.writelines("ENDSPLINE\n")
    file1.close()

#Funcion para extrar la data de Unity obtenida de los archivos de texto
def get4():
    f1 = open('posicion3.txt','r')
    f2 = open('velocidad3.txt','r')
    f3 = open('rotacion3.txt','r')
    pos3 = []
    vel3 = []
    rot3 = []
    for l in f1:
        temp = []
        aux = l.split(',')
        a=aux[3].split('\n')
        z = float(a[0])
        temp.append(float(aux[0]))
        temp.append(float(aux[1]))
        temp.append(float(aux[2]))
        temp.append(z)
        pos3.append(temp)

    for l in f2:
        temp = []
        aux = l.split(',')
        
        a=aux[3].split('\n')
        z = float(a[0])
        temp.append(float(aux[0]))
        temp.append(float(aux[1]))
        temp.append(float(aux[2]))
        temp.append(z)
        vel3.append(temp)

    for l in f3:
        temp = []
        aux = l.split(',')
        a=aux[3].split('\n')
        z = float(a[0])
        temp.append(float(aux[0]))
        temp.append(float(aux[1]))
        temp.append(float(aux[2]))
        temp.append(z)
        rot3.append(temp)

    return pos3,vel3,rot3