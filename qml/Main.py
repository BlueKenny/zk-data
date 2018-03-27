#!/usr/bin/env python3

import os
import threading
import time

try: import pyotherside
except: True

import libs.send
import libs.BlueFunc

#os.system("export MIR_SOCKET=/var/run/mir_socket")


class Main:    
    def __init__(self):
        print("init")
        #for user in os.listdir("/home/"):
        #    print(user)
        User = os.popen("echo $USER").readlines()[0].rstrip()
        
        Places = []
        if os.path.exists("/home/phablet"):
            Places.append("/home/phablet/.local/share/applications")
            #Places.append("/home/phablet/.config/autostart")
        else:
            Places.append(os.popen("echo $(xdg-user-dir DESKTOP)").readlines()[0].rstrip())
            Places.append(os.popen("echo $HOME").readlines()[0].rstrip() + "/.config/autostart")
            Places.append(os.popen("echo $HOME").readlines()[0].rstrip() + "/.local/share/applications")
        
        for Desktop in Places:
            file = Desktop + "/zk-data.desktop"
            #os.system("rm " + file)
            if True:#if not os.path.exists(file):
                print("Write Desktop Entry")
                print("User: " + str(User))
                print("Desktop: " + str(Desktop))
                print("file: " + str(file))
                DesktopEntry = open(file, "a")
                DesktopEntry.write("[Desktop Entry]\n")
                DesktopEntry.write("Name=ZK-DATA\n")
                DesktopEntry.write("Path=/home/" + User + "/zk-data/qml/\n")
                if User == "pi":# für raspberry
                    DesktopEntry.write("Exec=qmlscene -qt=qt5-arm-linux-gnueabihf /home/" + User + "/zk-data/qml/Main.qml\n")
                else:
                    DesktopEntry.write("Exec=qmlscene /home/" + User + "/zk-data/qml/Main.qml\n")
                DesktopEntry.write("Terminal=false\n")
                DesktopEntry.write("X-Ubuntu-Touch=true\n")
                DesktopEntry.write("Type=Application\n")
                DesktopEntry.write("StartupNotify=true\n")
                DesktopEntry.write("Icon=/home/" + User + "/zk-data/DATA/icon.png\n")
                 
                os.system("chmod +x " + file)
            
        os.system("git pull")
        self.busy(False)

    def phone(self):
        if os.path.exists("/home/phablet"):
            print("phone True")
            return True
        else:
            print("phone False")
            return False
            #return True

    def busy(self, status):
        status = bool(status)
        print("busy = " + str(status))
        pyotherside.send("busy", status)
      
    
        
main = Main()

