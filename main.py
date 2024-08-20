import subprocess
import time
import math
from Foundation import NSDate, NSObject
from AppKit import NSApplication, NSStatusBar, NSStatusItem, NSMenu, NSMenuItem, NSImage, NSTimer, NSRunLoop, NSDefaultRunLoopMode
from AppKit import NSApplicationActivationPolicyProhibited
from PyObjCTools import AppHelper

class CPUStatusApp(NSObject):
    images = {}
    statusbar = None
    statusitem = None
    timer = None

    def applicationDidFinishLaunching_(self, notification):
        # Set activation policy to not show icon in the Dock
        NSApplication.sharedApplication().setActivationPolicy_(NSApplicationActivationPolicyProhibited)

        # Set menu bar element to have set lenght
        statusbar = NSStatusBar.systemStatusBar()
        self.statusitem = statusbar.statusItemWithLength_(100)

        # Set icon
        self.statusitem.setImage_(NSImage.imageNamed_("NSStatusAvailable"))
        self.statusitem.setHighlightMode_(1)
        self.statusitem.setToolTip_('CPU Temperature Monitor')

        # Create simple menu
        self.menu = NSMenu.alloc().init()
        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Quit", "terminate:", "")
        self.menu.addItem_(menuitem)
        self.statusitem.setMenu_(self.menu)

        # Start time to update temperature
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
            # Execute command and obtain output
            result = subprocess.run(['osx-cpu-temp'], capture_output=True, text=True)
            # Extract temperature from outut
            temp_str = result.stdout.strip().replace('°C', '')
            # Convert temperature to float
            return float(temp_str)
        except Exception as e:
            print(f"Error getting CPU temperature: {e}")
            return None

    def round_temp(self, temp):
        if temp is None:
            return None
        # Round temperature
        return math.ceil(temp) if temp % 1 >= 0.5 else math.floor(temp)

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = CPUStatusApp.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()
