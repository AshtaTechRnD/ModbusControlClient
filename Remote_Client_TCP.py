"""
A simple example for reading and writing to registers for controlling using Remote terminal through modbusTCP.
Any third party application can be intercaced using read/write method over TCP-modbus.
More information on registers and addresses for robot specefic registers are provided in robot manual.
"""

#!/usr/bin python

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.version import version
from pymodbus.payload import BinaryPayloadDecoder,BinaryPayloadBuilder, Endian
import time

_BYTEORDER_ = Endian.Big
_WORDORDER_ = Endian.Big
_IP_ADDRESS_ = '192.168.1.24'
_PORT_ = 1025

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

                        t = False
                        #if t =True :: command execution || else t = False :: read from registers
                        #both read write procedures can be implemented simultaneously for continuos communication. 
                        while t:
                            val = self.client.read_input_registers(0x500,count=2,unit=_UNIT_) #Read X current Position 32-bit IEEE foating point at 0x500, 0x501
                            val = val.registers
                            print(self.decode_float_and_negative(val))
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
                            self.client.write_registers(0x100,xval,unit=_UNIT_) #Write X-cmd 32-bit IEEE foating point at 0x100, 0x102
                            y_pos = float(input("Set Y-pos: "))
                            yval,lengthVal = self.encode_float_and_negative(y_pos) 
                            self.client.write_registers(0x103,yval,unit=_UNIT_) #Write Y-cmd 32-bit IEEE foating point at 0x100, 0x102
                            speed = float(input("Set Speed: "))
                            speedval,lengthVal = self.encode_float_and_negative(speed)
                            self.client.write_registers(0x112,speedval,unit=_UNIT_) #Write execution speed 32-bit IEEE foating point at 0x100, 0x102
                            executeVar = int(input("Execute? [1 or 0]: "))
                            if (executeVar == 1):
                                self.client.write_coil(0x05,1,unit=_UNIT_) #Write execute bit == 1 to execute commanded position at 0x05
                                print("Execution: "+str(x_pos)+str(y_pos))
                else:
                    print("Connection Failed, Exiting")

    
    #Simple Function to decode float and negative values from 2=>16-bit registers
    def decode_float_and_negative(self,val):
        d = BinaryPayloadDecoder.fromRegisters(val, byteorder=_BYTEORDER_, wordorder=_WORDORDER_)
        returnVal = d.decode_32bit_float()
        return returnVal
    #Simple Function to encode float and negative values to 2=>16-bit registers
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
