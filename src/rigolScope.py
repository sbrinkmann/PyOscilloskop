# pyOscilloskop
#
# Copyright (19.2.2011) Sascha Brinkmann
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import usbtmc
import rigolScopeChannel
import timeAxis
        
class RigolScope:
    CHANNEL1 = "CHAN1"
    CHANNEL2 = "CHAN2"
    GET_TIME_SCALE = "TIM"
    GET_SCALE = "SCAL?"
    GET_OFFSET = "OFFS?"
    GET_DISPLAY_ACTIVE = "DISPlay?"

    """Class to control a Rigol DS1000 series oscilloscope"""
    def __init__(self, device = None):
        if(device == None):
            listOfDevices = usbtmc.getDeviceList()
            if(len(listOfDevices) == 0):
                raise ValueError("There is device to access")
    
            self.device = listOfDevices[0]
        else:
            self.device = device
        self.initScope()

    def initScope(self):
        print "Connection to device: " + self.device

        self.meas = usbtmc.UsbTmcDriver(self.device)

        print "Devicename: " + self.getName()

        self.channel1 = rigolScopeChannel.RigolScopeChannel(self, self.CHANNEL1);
        self.channel2 = rigolScopeChannel.RigolScopeChannel(self, self.CHANNEL2);        
        
    def write(self, command):
        """Send an arbitrary command directly to the scope"""
        self.meas.write(command)
        
    def read(self, command):
        """Read an arbitrary amount of data directly from the scope"""
        return self.meas.read(command)
        
    def reset(self):
        """Reset the instrument"""
        self.meas.sendReset()

    def getName(self):
        return self.meas.getName()

    def getDevice(self):
        return self.device
        
    def run(self):
        self.write(":RUN")
        
    def stop(self):
        self.write(":STOP")
        
    def reactivateControlButtons(self):
        self.write(":KEY:FORC")
    
    def getScopeInformation(self, channel, command, readBytes):
        self.write(":" + channel + ":" + command)
        return self.read(readBytes)
        
    def getScopeInformationFloat(self, channel, command):
        rawScopeInformation = self.getScopeInformation(channel, command, 20)
        floatScopeInformation = float(rawScopeInformation)
        return floatScopeInformation
    
    def getScopeInformationInteger(self, channel, command):
        rawScopeInformation = self.getScopeInformation(channel, command, 20)
        floatScopeInformation = int(rawScopeInformation)
        return floatScopeInformation
    
    def getScopeInformationString(self, channel, command, readBytes):
        return self.getScopeInformation(channel, command, readBytes)
        
    def getChannel1(self):
        return self.channel1
        
    def getChannel2(self):
        return self.channel2
        
    def getTimeScale(self):
        return self.getScopeInformationFloat(self.GET_TIME_SCALE, self.GET_SCALE)
        
    def getTimescaleOffset(self):
        return self.getScopeInformationFloat(self.GET_TIME_SCALE, self.GET_OFFSET)
        
    def getTimeAxis(self):
        return timeAxis.TimeAxis(self.getTimeScale())
