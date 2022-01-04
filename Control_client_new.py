

#!/usr/bin python

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.version import version
from pymodbus.payload import BinaryPayloadDecoder,BinaryPayloadBuilder, Endian
import time

_BYTEORDER_ = Endian.Big
_WORDORDER_ = Endian.Big
_IP_ADDRESS_ = '192.168.1.43'
#_IP_ADDRESS_ = 'localhost'
_PORT_ = 1124

_UNIT_ = 0x01

class mbClientClass:
    def __init__(self):
        #connect to server
        self.client = ModbusClient(_IP_ADDRESS_, port=_PORT_)
        print("Client Connected: ",self.client.connect())
        
        while True:
            i1 = int(input("Connect? [1 or 0]: "))
            if (i1 == 1):
                if(True):
                    print("Connected")
                    i2 = int(input("Set to Operational? [1 or 0]: "))
                    if (i2 == 1):
                        self.client.write_coil(0x01,0x01,unit=_UNIT_)
                        time.sleep(0.2)
                        val,lengthVal = self.encode_float_and_negative(1000)
                        self.client.write_registers(0x112,val,unit=_UNIT_)
                        print("In Operation mode, default speed: 1000")

                        t = True
                        while t:
                            val = self.client.read_input_registers(0x41,count=1,unit=_UNIT_)
                            val = val.registers
                            #print(val)
                            print("Home: ",val[0])
                            val = self.client.read_input_registers(0x500,count=2,unit=_UNIT_)
                            #print("X",val)
                            val = val.registers
                            #print(val)
                            print("X",self.decode_float_and_negative(val))
                            val = self.client.read_input_registers(0x502,count=2,unit=_UNIT_)
                            val = val.registers
                            print("Y",self.decode_float_and_negative(val))
                            time.sleep(1)

                        while not t:
                            x_pos = float(input("Set X-pos: "))
                            #for i in x_pos:
                            #    xval,lengthVal = self.encode_float_and_negative(i)
                            #    self.client.write_registers(0x100,xval,unit=_UNIT_)
                            #    self.client.write_coil(0x05,1,unit=_UNIT_)
                            #    time.sleep(0.1)
                            
                            xval,lengthVal = self.encode_float_and_negative(x_pos)
                            print(xval)
                            self.client.write_registers(0x100,xval,unit=_UNIT_)
                            y_pos = float(input("Set Y-pos: "))
                            yval,lengthVal = self.encode_float_and_negative(y_pos)
                            self.client.write_registers(0x103,yval,unit=_UNIT_)
                            speed = float(input("Set Speed: "))
                            speedval,lengthVal = self.encode_float_and_negative(speed)
                            self.client.write_registers(0x112,speedval,unit=_UNIT_)
                            executeVar = int(input("Execute? [1 or 0]: "))
                            if (executeVar == 1):
                                self.client.write_coil(0x05,1,unit=_UNIT_)
                                print("Execution: "+str(x_pos)+str(y_pos))
                            while True:
                                eefState = int(input("Set_on estop: "))
                                if(eefState == 1):
    	                            #0x02 estop 09 eef
	                                self.client.write_coil(0x03,1,unit=_UNIT_)
                                if(eefState == 0):
	                            #0x02 estop 06 eef
    	                            self.client.write_coil(0x03,0,unit=_UNIT_)
                                exeMore = int(input("Execute More: "))
                                if (exeMore ==1):
                                    x_pos = float(input("Set X-pos: "))
                                    xval,lengthVal = self.encode_float_and_negative(x_pos)
                                    print(xval)
                                    self.client.write_registers(0x100,xval,unit=_UNIT_)
                                    y_pos = float(input("Set Y-pos: "))
                                    yval,lengthVal = self.encode_float_and_negative(y_pos)
                                    self.client.write_registers(0x103,yval,unit=_UNIT_)
                                    speed = float(input("Set Speed: "))
                                    speedval,lengthVal = self.encode_float_and_negative(speed)
                                    self.client.write_registers(0x112,speedval,unit=_UNIT_)
                                    executeVar = int(input("Execute? [1 or 0]: "))
                                    if (executeVar == 1):
                                        self.client.write_coil(0x05,1,unit=_UNIT_)
                                        print("Execution: "+str(x_pos)+str(y_pos))
	                        #print("EEF ON")
                else:
                    print("Connection Failed, Exiting") 


    def decode_float_and_negative(self,val):
        d = BinaryPayloadDecoder.fromRegisters(val, byteorder=_BYTEORDER_, wordorder=_WORDORDER_)
        returnVal = d.decode_32bit_float()
        return returnVal
    
    def encode_float_and_negative(self,val):
        builder = BinaryPayloadBuilder(byteorder=_BYTEORDER_, wordorder=_WORDORDER_)
        builder.reset()
        builder.add_32bit_float(val)
        returnVal = builder.to_registers()
        return returnVal,len(returnVal)



if __name__=='__main__':
    try:
        mbClientClass()
    except:
        print("CannotStart")
