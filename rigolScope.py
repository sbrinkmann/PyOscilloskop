import usbtmc
import rigolScopeChannel
import numpy
        
class RigolScope:
    CHANNEL1 = "CHAN1"
    CHANNEL2 = "CHAN2"
    TIME_SCALE = "TIM"
    SCALE = "SCAL?"
    OFFSET = "OFFS?"

    """Class to control a Rigol DS1000 series oscilloscope"""
    def __init__(self, device):
        self.meas = usbtmc.UsbTmcDriver(device)

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
        
    def run(self):
        self.write(":RUN")
        
    def stop(self):
        self.write(":STOP")
        
    def reactivateControlButtons(self):
        self.write(":KEY:FORC")
        
    def getScopeInformation(self, channel, command):
        self.write(":" + channel + ":" + command)
        channelInformation = float(self.read(20))
        return channelInformation
        
    def getChannel1(self):
        return self.channel1
        
    def getChannel2(self):
        return self.channel2
        
    def getTimeScale(self):
        return self.getScopeInformation(self.TIME_SCALE, self.SCALE)
        
    def getTimescaleOffset(self):
        return self.getScopeInformation(self.TIME_SCALE, self.OFFSET)
        
    def getTimeAxis(self):
        timescale = self.getTimeScale()
        # Now, generate a time axis.  The scope display range is 0-600, with 300 being
        # time zero.
        time = numpy.arange(-300.0/50*timescale, 300.0/50*timescale, timescale/50.0)
        
        return time
    
    def getTimeAxisUnit(self):
        if (time[599] < 1e-3):
            time = time * 1e6
            tUnit = "uS"
        elif (time[599] < 1):
            time = time * 1e3
            tUnit = "mS"
        else:
            tUnit = "S"
