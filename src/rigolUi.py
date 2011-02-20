#!/usr/bin/python

import gtk
import rigolScope


class MyApp(object):
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("oscilloskopControl.glade")
        self.builder.connect_signals(self)
        self.scope = rigolScope.RigolScope();
        self.win =  self.builder.get_object('window1')
        self.win.set_title("Oscilloskope remote control")
        
        self.showOscilloskopInformations()
        
    def showOscilloskopInformations(self):
        scope = self.scope
        builder = self.builder
        
        builder.get_object("labelConnectedToDevice").set_text(scope.getName() + " (" + scope.getDevice() + ")")
        builder.get_object("textChannel1Voltage").set_text(str(scope.getChannel1().getVoltageScale()) + " V/DIV")
        builder.get_object("textChannel1Offset").set_text(str(scope.getChannel1().getVoltageOffset()) + " V")
        builder.get_object("textChannel2Voltage").set_text(str(scope.getChannel2().getVoltageOffset()) + " V")
        builder.get_object("textChannel2Offset").set_text(str(scope.getChannel2().getVoltageOffset()) + " V")
        builder.get_object("textTimeAxisScale").set_text(str(scope.getTimeScale()) + "S/DIV")
        builder.get_object("textTimeAxisOffset").set_text(str(scope.getTimescaleOffset()) + " S")

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
        channel1Active = self.builder.get_object("checkChannel1Showchannel").get_active()
        channel2Active = self.builder.get_object("checkChannel2Showchannel").get_active()
        
        if(channel1Active == False and channel2Active == False):
            self.info_msg("Please select a channel first.")
            return
        
        timeAxis = self.scope.getTimeAxis()
        time = timeAxis.getTimeAxis()
        
        import matplotlib.pyplot as plot
        
        if(channel1Active):
            plot.plot(time, self.scope.getChannel1().getData())
        if(channel2Active):    
            plot.plot(time, self.scope.getChannel2().getData())
        
        plot.title("Oscilloskop")
        plot.ylabel("Voltage (V)")
        plot.xlabel("Time (" + timeAxis.getUnit() + ")")
        plot.xlim(time[0], time[599])
        plot.plot()
        plot.savefig("test.png")
        
        self.scope.reactivateControlButtons()

if __name__ == '__main__':
    app = MyApp()
    app.run()
    
