import numpy

class RigolScopeChannel:
    
    def __init__(self, rigolScope, channelName):
        self.rigolScope = rigolScope
        self.channelName = channelName
        
    def getVoltageScale(self):
        return self.rigolScope.getScopeInformation(self.channelName, self.rigolScope.SCALE)
        
    def getVoltageOffset(self):
        return self.rigolScope.getScopeInformation(self.channelName, self.rigolScope.OFFSET)
        
    def getData(self):
        self.rigolScope.write(":WAV:POIN:MODE NOR")
        self.rigolScope.write(":WAV:DATA? " + self.channelName)
        
        rawdata = self.rigolScope.read(9000)
        data = numpy.frombuffer(rawdata, 'B')

        # Walk through the data, and map it to actual voltages
        # First invert the data (ya rly)
        data = data * -1 + 255
        
        voltscale = self.getVoltageScale();
        voltoffset= self.getVoltageOffset();
        
        # Now, we know from experimentation that the scope display range is actually
        # 30-229.  So shift by 130 - the voltage offset in counts, then scale to
        # get the actual voltage.
        data = (data - 130.0 - voltoffset/voltscale*25) / 25 * voltscale
        
        return data
