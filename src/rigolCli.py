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
from optparse import OptionParser
from time import strftime

parser = OptionParser()
parser.add_option("-p", "--plot", action="store_false", help="Shows the window with the plot")
parser.add_option("-1", "--hideChannel1", action="store_true", default=False, help="Hides Channel 1 in the plot")
parser.add_option("-2", "--hideChannel2", action="store_true", default=False, help="Hides Channel 1 in the plot")
parser.add_option("-i", "--informations", action="store_false", help="Prints scope informations")
parser.add_option("-s", "--savePlot", metavar="filename", help="Saves the plot into a image")
parser.add_option("-t", "--title", metavar="title", help="Set the title of the plot")
parser.add_option("-d", "--hideDate", action="store_true", default=False, help="Hides the date in the plot")

(options, args) = parser.parse_args()
 
""" Example program to plot the Y-T data from Channel 1"""

listOfDevices = usbtmc.getDeviceList()

systemArguments = sys.argv

"""Initialize our scope"""
if(len(listOfDevices) == 0):
    print "You need one or more devices"
    pass

choosenDevice = listOfDevices[0]

scope = rigolScope.RigolScope(choosenDevice)



if(options.informations != None):
    print "Device: ", choosenDevice
    print "Name: ", scope.getName()
    
    print "Channel 1 - Active: ", scope.getChannel1().isChannelActive()
    print "Channel 1 - Voltage scale: ", scope.getChannel1().getVoltageScale(), "V/div"
    print "Channel 1 - Voltage offset: ", scope.getChannel1().getVoltageOffset(), "V"
    
    print "Channel 2 - Active: ", scope.getChannel2().isChannelActive()
    print "Channel 2 - Voltage scale: ", scope.getChannel2().getVoltageScale(), "V/div"
    print "Channel 2 - Voltage offset: ", scope.getChannel2().getVoltageOffset(), "V"
    
    print "Timescale: ", scope.getTimeScale(), "sec/div"
    print "Timescale offset: ", scope.getTimescaleOffset(), "sec"

"""You have to reactivate the keys on the scope after every access over the usb interface"""
scope.reactivateControlButtons()

def fillPlot(options):
    channel1Data = scope.getChannel1().getData();
    channel1Data = channel1Data[0:600:1]
    
    channel2Data = scope.getChannel2().getData();
    channel2Data = channel2Data[0:600:1]

    time = scope.getTimeAxis();
    
    timeAxis = time.getTimeAxis()
    
    if (not(options.hideChannel1) and scope.getChannel1().isChannelActive()):
        plot.plot(timeAxis, channel1Data)
    if (not(options.hideChannel2) and scope.getChannel2().isChannelActive()):
        plot.plot(timeAxis, channel2Data)
    title = "Oscilloskop"
    if(options.title != None):
        title = options.title
    if(options.hideDate == False):
        title = title + " (" + strftime("%Y-%m-%d %H:%M:%S") + ")"
    plot.title(title)
    plot.ylabel("Voltage (V)")
    plot.xlabel("Time (" + time.getUnit() + ")")
    plot.xlim(timeAxis[0], timeAxis[599])

if(options.savePlot != None or options.plot != None):
    fillPlot(options)
    
scope.reactivateControlButtons()

if(options.savePlot != None):
    print "Save plot to: ", options.savePlot
    plot.draw()
    plot.savefig(options.savePlot)

if(options.plot != None):
        """Plot the data"""
        plot.show()

