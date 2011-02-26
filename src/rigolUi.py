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

import gtk
import rigolScope
import os
import threading

class RigolUI(object):
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("oscilloskopControl.glade")
        self.builder.connect_signals(self)
        self.scope = rigolScope.RigolScope();
        self.win =  self.builder.get_object('window1')
        self.win.set_title("Oscilloskope remote control")
        self.figureCounter = 1
        
        self.showOscilloskopInformations()
        
    def showOscilloskopInformations(self):
        scope = self.scope
        builder = self.builder
        
        builder.get_object("labelConnectedToDevice").set_text(scope.getName() + " (" + scope.getDevice() + ")")
        builder.get_object("checkChannel1Showchannel").set_active(scope.getChannel1().isChannelActive())
        builder.get_object("textChannel1Voltage").set_text(str(scope.getChannel1().getVoltageScale()) + " V/DIV")
        builder.get_object("textChannel1Offset").set_text(str(scope.getChannel1().getVoltageOffset()) + " V")
        builder.get_object("checkChannel2Showchannel").set_active(scope.getChannel2().isChannelActive())
        builder.get_object("textChannel2Voltage").set_text(str(scope.getChannel2().getVoltageScale()) + " V/DIV")
        builder.get_object("textChannel2Offset").set_text(str(scope.getChannel2().getVoltageOffset()) + " V")
        builder.get_object("textTimeAxisScale").set_text(str(scope.getTimeScale()) + "S/DIV")
        builder.get_object("textTimeAxisOffset").set_text(str(scope.getTimescaleOffset()) + " S")
        
        scope.reactivateControlButtons()

    def run(self):
        try:
            gtk.main()
        except KeyboardInterrupt:
            pass
    
    def quit(self):
        gtk.main_quit()

    def on_window1_delete_event(self, *args):
        self.quit()
        
    def info_msg(self, msg):
        dlg = gtk.MessageDialog(parent=self.win, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK, message_format=msg)
        dlg.run()
        dlg.destroy()

    def on_buttonShow_clicked(self, *args):
        self.plotFigure()
        #thread = threading.Thread(target=self.plotFigure)
        #thread.start()
        #print "Running in main thread\n"
        
    def plotFigure(self):
        print "Plot figure"
        
        parameter = " -p"
        if(self.builder.get_object("checkRestartAfterAquring").get_active()):
            parameter += " -r"
        
        if(not(self.builder.get_object("checkChannel1Showchannel").get_active())):
            parameter += " -1"
            
        if(not(self.builder.get_object("checkChannel2Showchannel").get_active())):
            parameter += " -2"
            
        os.system("./rigolCli.py " + parameter)
            
        

        
if __name__ == '__main__':
    rigolUiApp = RigolUI()
    rigolUiApp.run()
    
    
