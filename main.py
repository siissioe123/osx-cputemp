import subprocess
import math
import webbrowser
import os
from Foundation import NSDate, NSObject
from AppKit import NSApplication, NSStatusBar, NSStatusItem, NSMenu, NSMenuItem, NSImage, NSTimer, NSRunLoop, NSDefaultRunLoopMode, NSAppearance
from AppKit import NSApplicationActivationPolicyProhibited
from PyObjCTools import AppHelper

class CPUStatusApp(NSObject):
    statusbar = None
    statusitem = None
    timer = None
    use_fahrenheit = False

    def applicationDidFinishLaunching_(self, notification):
        # Set the activation policy to hide dock icon
        NSApplication.sharedApplication().setActivationPolicy_(NSApplicationActivationPolicyProhibited)

        # Create the menu bar with a fixed length
        self.statusbar = NSStatusBar.systemStatusBar()
        self.statusitem = self.statusbar.statusItemWithLength_(140)  # Initially set to 140 points

        # The green dot that appears on the menu bar
        self.statusitem.setImage_(NSImage.imageNamed_("NSStatusAvailable"))
        self.statusitem.setHighlightMode_(1)
        self.statusitem.setToolTip_('Temperature Monitor')

        # Create the menu
        self.menu = NSMenu.alloc().init()

        # Add break line
        self.menu.addItem_(NSMenuItem.separatorItem())

        # Celsius Option
        self.celsiusMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Celsius", "toggleCelsius:", "")
        self.celsiusMenuItem.setState_(1)  # Initially selected
        self.menu.addItem_(self.celsiusMenuItem)
        
        # Fahrenheit Option
        self.fahrenheitMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Fahrenheit", "toggleFahrenheit:", "")
        self.fahrenheitMenuItem.setState_(0)  # Initially not selected
        self.menu.addItem_(self.fahrenheitMenuItem)

        # Add break line
        self.menu.addItem_(NSMenuItem.separatorItem())

        # Menu Item for CPU
        self.cpuMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("CPU", "toggleCPU:", "")
        self.cpuMenuItem.setState_(1)  # Initially checked
        self.menu.addItem_(self.cpuMenuItem)
        
        # Menu Item for GPU
        self.gpuMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("GPU", "toggleGPU:", "")
        self.gpuMenuItem.setState_(0)  # Initially unchecked
        self.menu.addItem_(self.gpuMenuItem)

        # Break line
        self.menu.addItem_(NSMenuItem.separatorItem())

        # Add and create github menu item (with icon)
        self.githubMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("", "openGithub:", "")
        self.updateGithubIcon()
        self.githubMenuItem.setTitle_(" Github")  # Space added before text to make room for the icon
        self.menu.addItem_(self.githubMenuItem)

        # Add a separator line before the Quit option
        self.menu.addItem_(NSMenuItem.separatorItem())
        
        # Quit Option
        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Quit", "terminate:", "")
        self.menu.addItem_(menuitem)
        
        self.statusitem.setMenu_(self.menu)

        # Start timer to update temperature
        self.timer = NSTimer.alloc().initWithFireDate_interval_target_selector_userInfo_repeats_(NSDate.date(), 1.0, self, 'updateTemperature:', None, True)
        NSRunLoop.currentRunLoop().addTimer_forMode_(self.timer, NSDefaultRunLoopMode)
        self.timer.fire()

    def updateGithubIcon(self):
        # Determine current appearance mode
        appearance = NSApplication.sharedApplication().effectiveAppearance()
        appearance_name = appearance.name()

        # Set the appropriate logo based on current appearance mode
        if appearance_name == "NSAppearanceNameDarkAqua":
            image_name = 'Github_dark00000'
        else:
            image_name = 'Github_light00000'

        # Load and set image
        image_path = os.path.join('assets', 'Github-Logos', f'{image_name}.png')
        github_icon = NSImage.alloc().initByReferencingFile_(image_path)
        self.githubMenuItem.setImage_(github_icon)

    def toggleCelsius_(self, sender):
        if not self.celsiusMenuItem.state():
            self.use_fahrenheit = False
            self.celsiusMenuItem.setState_(1)
            self.fahrenheitMenuItem.setState_(0)
            self.updateTemperature_(None)

    def toggleFahrenheit_(self, sender):
        if not self.fahrenheitMenuItem.state():
            self.use_fahrenheit = True
            self.fahrenheitMenuItem.setState_(1)
            self.celsiusMenuItem.setState_(0)
            self.updateTemperature_(None)

    def toggleCPU_(self, sender):
        current_state = self.cpuMenuItem.state()
        self.cpuMenuItem.setState_(0 if current_state else 1)
        self.updateTemperature_(None)

    def toggleGPU_(self, sender):
        current_state = self.gpuMenuItem.state()
        self.gpuMenuItem.setState_(0 if current_state else 1)
        self.updateTemperature_(None)

    def openGithub_(self, sender):
        # Open the GitHub URL in web browser
        webbrowser.open("https://github.com/siissioe123/osx-cputemp")

    def updateTemperature_(self, timer):
        temp_display = []

        if self.cpuMenuItem.state() == 1:
            temp = self.get_cpu_temp()
            if temp is not None:
                rounded_temp = self.round_temp(temp)
                unit = 'F' if self.use_fahrenheit else 'C'
                temp_display.append(f"CPU: {rounded_temp}°{unit}")
        
        if self.gpuMenuItem.state() == 1:
            temp = self.get_gpu_temp()
            if temp is not None:
                rounded_temp = self.round_temp(temp)
                unit = 'F' if self.use_fahrenheit else 'C'
                temp_display.append(f"GPU: {rounded_temp}°{unit}")

        # Join the selected items with " | "
        if temp_display:
            self.statusitem.setTitle_(" | ".join(temp_display))
        else:
            # Display "osx-cputemp" if nothing is selected
            self.statusitem.setTitle_("osx-cputemp")

        # Adjust the width of status item based on the selection
        if len(temp_display) == 1:
            self.statusitem.setLength_(100)
        elif len(temp_display) == 2:
            self.statusitem.setLength_(200)
        else:
            self.statusitem.setLength_(140)

    def get_cpu_temp(self):
        try:
            # Run the osx-cpu-temp command and get  output
            command = ['osx-cpu-temp']
            if self.use_fahrenheit:
                command.append('-F')
            result = subprocess.run(command, capture_output=True, text=True)
            temp_str = result.stdout.strip().replace('°C', '').replace('°F', '')
            return float(temp_str)
        except Exception as e:
            print(f"Error getting CPU temperature: {e}")
            return None

    def get_gpu_temp(self):
        try:
            # Run "osx-cpu-temp -g" command to get GPU temperature
            command = ['osx-cpu-temp', '-g']
            if self.use_fahrenheit:
                command.append('-F')
            result = subprocess.run(command, capture_output=True, text=True)
            temp_str = result.stdout.strip().replace('°C', '').replace('°F', '')
            return float(temp_str)
        except Exception as e:
            print(f"Error getting GPU temperature: {e}")
            return None

    def round_temp(self, temp):
        if temp is None:
            return None
        # Round the temperature
        return math.ceil(temp) if temp % 1 >= 0.5 else math.floor(temp)

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = CPUStatusApp.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()
