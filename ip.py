#!/usr/bin/python
import os
import subprocess
import appindicator
import gtk

# 2016-05-07 tc@DinkumSoftware.com Bug fix.  Suppress localhost 127.0.0.1
# 2016-05-08 tc@DinkumSoftware.com Bug fix.  Display multiple IP numbers

ICON = os.path.abspath("./images/icon.png")

def get_ip():

    # The first grep produces
    #     inet addr:127.0.0.1
    #     inet addr:10.23.4.15
    #     inet addr:172.27.224.230
    # The 2nd grep removes the 127 addr (localhost)
    # The 3rd grep produces:
    #     172.27.224.230
    #     10.23.4.15

    ip = subprocess.check_output('ifconfig |\
        grep -o -P "inet addr:([^ ]*)"     |\
        grep -v    "127.0.0.1"             |\
        grep -o -P "[0-9.]+"',     shell=True)

    # turn multiple lines of IP addresses into
    # a single line with IPs space separated
    ip  = ip.strip()
    ipl = ip.split('\n')  # The list
    ip  = ' '.join(ipl)
    return ip


class IPIndicator:
    def __init__(self):
        self.ip = ""
        self.ind = appindicator.Indicator("ip-indicator", ICON,
            appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.update()
        self.ind.set_menu(self.setup_menu())
    
    def setup_menu(self):
        menu = gtk.Menu()

        refresh = gtk.MenuItem("Refresh")
        refresh.connect("activate", self.on_refresh)
        refresh.show()
        menu.append(refresh)

        return menu

    def update(self):
        """
        
        Update the IP address.
        
        """
        ip = get_ip()
        if ip != self.ip:
            self.ip = ip
            self.ind.set_label(ip)

    def on_refresh(self, widget):
        self.update()


if __name__ == "__main__":
    i = IPIndicator()
    gtk.main()

