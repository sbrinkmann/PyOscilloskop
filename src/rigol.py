#!/usr/bin/python

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

import matplotlib.pyplot as plot
import rigolScope
import sys
import usbtmc
 
""" Example program to plot the Y-T data from Channel 1"""

listOfDevices = usbtmc.getDeviceList()

systemArguments = sys.argv

# Initialize our scope
if(len(listOfDevices) == 0):
    print "You need one or more devices"
    pass 

scope = rigolScope.RigolScope(listOfDevices[0])

print scope.getName()
print ""

channel1Data = scope.getChannel1().getData();
channel1Data = channel1Data[0:600:1]

channel2Data = scope.getChannel2().getData();
channel2Data = channel2Data[0:600:1]

print "Channel 1 - Voltage scale: ", scope.getChannel1().getVoltageScale(), "V/div"
print "Channel 1 - Voltage offset: ", scope.getChannel1().getVoltageOffset(), "V"
print "Channel 1 - Data: ", channel1Data.size

print "Channel 2 - Voltage scale: ", scope.getChannel2().getVoltageScale(), "V/div"
print "Channel 2 - Voltage offset: ", scope.getChannel2().getVoltageOffset(), "V"
print "Channel 1 - Data: ", channel1Data.size

print "Timescale: ", scope.getTimeScale(), "sec/div"
print "Timescale offset: ", scope.getTimescaleOffset(), "sec"

time = scope.getTimeAxis();


# See if we should use a different time axis
if (time[599] < 1e-3):
    time = time * 1e6
    tUnit = "uS"
elif (time[599] < 1):
    time = time * 1e3
    tUnit = "mS"
else:
    tUnit = "S"
    
time = time [0:600:1]

"""You have to reactivate the keys on the scope after every access over the usb interface"""
scope.reactivateControlButtons()

# Plot the data
plot.plot(time, channel1Data)
#plot.plot(time, channel2Data)
plot.title("Oscilloskop")
plot.ylabel("Voltage (V)")
plot.xlabel("Time (" + tUnit + ")")
plot.xlim(time[0], time[599])
plot.show()
