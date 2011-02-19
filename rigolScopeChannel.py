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
