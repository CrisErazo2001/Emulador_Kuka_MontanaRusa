/*
  WT901CTTL       ESP32
    VCC <--->  5V/3.3V
    TX  <--->  (RX2) 16
    RX  <--->  (TX2) 17
    GND <--->  GND

  Micro SD        ESP32
    VCC <--->  5V/3.3V
    CS  <--->  GPIO 5
  MOSI  <--->  GPIO 23
   CLK  <--->  GPIO 18
   MISO <--->  GPIO 19
    GND <--->  GND

  DATOS QUE SE GUARDAN
  Tiempo [seg]
  Angulos Rollx, Pitchy, Yawz [°]
  Aceleraccion x,y,z [g] g is Gravity acceleration, 9.8m/s2
*/

#include <HardwareSerial.h>
#include <REG.h>
#include <wit_c_sdk.h>
#include "FS.h"
#include "SD.h"
#include "SPI.h"
#define ACC_UPDATE    0x01
#define GYRO_UPDATE   0x02
#define ANGLE_UPDATE  0x04
#define READ_UPDATE   0x80

HardwareSerial NuevoSerial1(2);

static volatile char s_cDataUpdate = 0, s_cCmd = 0xff;

static void AutoScanSensor(void);
static void SensorUartSend(uint8_t *p_data, uint32_t uiSize);
static void SensorDataUpdata(uint32_t uiReg, uint32_t uiRegNum);
static void Delayms(uint16_t ucMs);
const uint32_t c_uiBaud[8] = {0, 4800, 9600, 19200, 38400, 57600, 115200, 230400};

File fileA, fileO, fileT;
boolean estado = 0;
char filename[20];
int fileCount = 0;

String aceleracion = " ";
String orientacion = " ";

unsigned long tiempoInicial;
unsigned long tiempoActual;

void setup() {
  Serial.begin(115200);
  SD.begin();
  WitInit(WIT_PROTOCOL_NORMAL, 0x50);
  WitSerialWriteRegister(SensorUartSend);
  WitRegisterCallBack(SensorDataUpdata);
  WitDelayMsRegister(Delayms);
  AutoScanSensor();
   tiempoInicial = millis();
}
int i, j;
int tMuestra = 334; //Tiempo de muestra
float fAcc[3], fGyro[3], fAngle[3];
//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void loop() {
  tiempoActual = millis(); 
  unsigned long tiempoTranscurrido = (tiempoActual - tiempoInicial) / 1000; 
  while (NuevoSerial1.available())
  {
    WitSerialDataIn(NuevoSerial1.read());
  }
  while (Serial.available())
  {
    CopeCmdData(Serial.read());
  }

  if (s_cDataUpdate)
  {
    for (i = 0; i < 3; i++)
    {
      fAcc[i] = sReg[AX + i] / 32768.0f * 16.0f;
      fGyro[i] = sReg[GX + i] / 32768.0f * 2000.0f;
      fAngle[i] = sReg[Roll + i] / 32768.0f * 180.0f;
     // delay(tMuestra);
    }

    if (Mov(fGyro)) {
      estado = 1;
      Serial.print("Estado 1");
      fileA = SD.open("/Aceleracion.txt", FILE_APPEND);
      fileO = SD.open("/Orientacion.txt", FILE_APPEND);
      fileT = SD.open("/Tiempo.txt", FILE_APPEND);
      
      if (s_cDataUpdate & ACC_UPDATE)
      {
        aceleracion = String(fAcc[0]) + " " + String(fAcc[1]) + " " + String(fAcc[2]) + "\r\n";
        fileA.print(aceleracion);
        s_cDataUpdate &= ~ACC_UPDATE;
      }
      if (s_cDataUpdate & GYRO_UPDATE)
      {
        s_cDataUpdate &= ~GYRO_UPDATE;
      }
      if (s_cDataUpdate & ANGLE_UPDATE)
      {
        orientacion = String(fAngle[0]) + " " + String(fAngle[1]) + " " + String(fAngle[2]) + "\r\n";
        fileO.print(orientacion);
        s_cDataUpdate &= ~ANGLE_UPDATE;
      }
      fileT.print(tiempoTranscurrido);
      s_cDataUpdate = 0;
    }

    if (!Mov(fGyro)) {
      estado = 0;
      Serial.print("Estado 0");
      fileT.close();
      fileA.close();
      fileO.close();
    }
  }
  delay(tMuestra);
}
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void CopeCmdData(unsigned char ucData)
{
  static unsigned char s_ucData[50], s_ucRxCnt = 0;

  s_ucData[s_ucRxCnt++] = ucData;
  if (s_ucRxCnt < 3)return;                 //Less than three data returned
  if (s_ucRxCnt >= 50) s_ucRxCnt = 0;
  if (s_ucRxCnt >= 3)
  {
    if ((s_ucData[1] == '\r') && (s_ucData[2] == '\n'))
    {
      s_cCmd = s_ucData[0];
      memset(s_ucData, 0, 50);
      s_ucRxCnt = 0;
    }
    else
    {
      s_ucData[0] = s_ucData[1];
      s_ucData[1] = s_ucData[2];
      s_ucRxCnt = 2;

    }
  }
}

static void SensorUartSend(uint8_t *p_data, uint32_t uiSize)
{
  NuevoSerial1.write(p_data, uiSize);
  NuevoSerial1.flush();
}
static void Delayms(uint16_t ucMs)
{
  delay(ucMs);
}
static void SensorDataUpdata(uint32_t uiReg, uint32_t uiRegNum)
{
  int i;
  for (i = 0; i < uiRegNum; i++)
  {
    switch (uiReg)
    {
      case AZ:
        s_cDataUpdate |= ACC_UPDATE;
        break;
      case GZ:
        s_cDataUpdate |= GYRO_UPDATE;
        break;
      case Yaw:
        s_cDataUpdate |= ANGLE_UPDATE;
        break;
      default:
        s_cDataUpdate |= READ_UPDATE;
        break;
    }
    uiReg++;
  }
}

static void AutoScanSensor(void)
{
  int i, iRetry;

  for (i = 0; i < sizeof(c_uiBaud) / sizeof(c_uiBaud[0]); i++)
  {
    NuevoSerial1.begin(c_uiBaud[i]);
    NuevoSerial1.flush();
    iRetry = 2;
    s_cDataUpdate = 0;
    do
    {
      WitReadReg(AX, 3);
      delay(100);
      while (NuevoSerial1.available())
      {
        WitSerialDataIn(NuevoSerial1.read());
      }
      if (s_cDataUpdate != 0)
      {

        return ;
      }
      iRetry--;
    } while (iRetry);
  }

}


int Mov(float A[3]) {
  for (int i = 0; i < 3; i++) {
    if (A[i] != 0) {
      return 1;
    }
  }
  return 0;
}
