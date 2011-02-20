#!/usr/bin/python

import gtk


class MyApp(object):
    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("oscilloskopControl.glade")
        self.builder.connect_signals(self)

    def run(self):
        try:
            gtk.main()
        except KeyboardInterrupt:
            pass
    
    def quit(self):
        gtk.main_quit()


    def on_window1_delete_event(self, *args):
        self.quit()


if __name__ == '__main__':
    app = MyApp()
    app.run()
