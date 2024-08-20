import subprocess
import time
import math
from Foundation import NSDate, NSObject
from AppKit import NSApplication, NSStatusBar, NSStatusItem, NSMenu, NSMenuItem, NSImage, NSTimer, NSRunLoop, NSDefaultRunLoopMode
from AppKit import NSApplicationActivationPolicyProhibited  # Importa la costante necessaria
from PyObjCTools import AppHelper

class CPUStatusApp(NSObject):
    images = {}
    statusbar = None
    statusitem = None
    timer = None

    def applicationDidFinishLaunching_(self, notification):
        # Imposta la politica di attivazione per nascondere l'icona del Dock
        NSApplication.sharedApplication().setActivationPolicy_(NSApplicationActivationPolicyProhibited)

        # Crea l'elemento della barra dei menu con una lunghezza fissa
        statusbar = NSStatusBar.systemStatusBar()
        self.statusitem = statusbar.statusItemWithLength_(100)  # Lunghezza fissa di 100 punti

        # Imposta l'immagine iniziale (puoi usarne una generica se desideri)
        self.statusitem.setImage_(NSImage.imageNamed_("NSStatusAvailable"))
        self.statusitem.setHighlightMode_(1)
        self.statusitem.setToolTip_('CPU Temperature Monitor')

        # Crea un menu semplice
        self.menu = NSMenu.alloc().init()
        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Quit", "terminate:", "")
        self.menu.addItem_(menuitem)
        self.statusitem.setMenu_(self.menu)

        # Avvia il timer per aggiornare la temperatura
        self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(NSDate.date(), 1.0, self, 'updateTemperature:', None, True)
        NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)
        self.timer.fire()

    def updateTemperature_(self, timer):
        temp = self.get_cpu_temp()
        if temp is not None:
            rounded_temp = self.round_temp(temp)
            self.statusitem.setTitle_(f"{rounded_temp}°C")
        else:
            self.statusitem.setTitle_("Error")

    def get_cpu_temp(self):
        try:
            # Esegui il comando osx-cpu-temp e ottieni l'output
            result = subprocess.run(['osx-cpu-temp'], capture_output=True, text=True)
            # Estrai la temperatura dal risultato
            temp_str = result.stdout.strip().replace('°C', '')
            # Converti la temperatura in float
            return float(temp_str)
        except Exception as e:
            print(f"Error getting CPU temperature: {e}")
            return None

    def round_temp(self, temp):
        if temp is None:
            return None
        # Arrotonda la temperatura
        return math.ceil(temp) if temp % 1 >= 0.5 else math.floor(temp)

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = CPUStatusApp.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()
