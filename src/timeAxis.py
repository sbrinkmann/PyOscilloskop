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

class TimeAxis:
    
    def __init__(self, timescale):
        self.timescale = timescale
    
    def _getTime(self):
        time = numpy.arange(-300.0/50*self.timescale, 300.0/50*self.timescale, self.timescale/50.0)
        
        return time
    
    def getTimeAxis(self):
        time = self._getTime()
        
        if (time[599] < 1e-3):
            time = time * 1e6
        elif (time[599] < 1):
            time = time * 1e3
            
        time = time[0:600:1]

        return time
    
    def getUnit(self):
        time = self._getTime()
        
        if (time[599] < 1e-3):
            tUnit = "uS"
        elif (time[599] < 1):
            tUnit = "mS"
        else:
            tUnit = "S"
            
        return tUnit