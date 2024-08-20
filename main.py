import subprocess
import math
import webbrowser
import os
import toml
from Foundation import NSDate, NSObject
from AppKit import NSApplication, NSStatusBar, NSStatusItem, NSMenu, NSMenuItem, NSImage, NSTimer, NSRunLoop, NSDefaultRunLoopMode, NSAppearance
from AppKit import NSApplicationActivationPolicyProhibited
from PyObjCTools import AppHelper

class CPUStatusApp(NSObject):
    statusbar = None
    statusitem = None
    timer = None
    use_fahrenheit = False
    cpu_temp_cmd = 'bin/osx-cpu-temp'  # Default path to osx-cpu-temp

    def applicationDidFinishLaunching_(self, notification):
        self.ensure_cpu_temp_built()
        self.load_settings()
        
        # Set the activation policy to hide the dock icon
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
        self.celsiusMenuItem.setState_(1 if self.use_fahrenheit == False else 0)  # Based on loaded settings
        self.menu.addItem_(self.celsiusMenuItem)
        
        # Fahrenheit Option
        self.fahrenheitMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Fahrenheit", "toggleFahrenheit:", "")
        self.fahrenheitMenuItem.setState_(1 if self.use_fahrenheit == True else 0)  # Based on loaded settings
        self.menu.addItem_(self.fahrenheitMenuItem)

        # Add break line
        self.menu.addItem_(NSMenuItem.separatorItem())

        # Menu Item for CPU
        self.cpuMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("CPU", "toggleCPU:", "")
        self.cpuMenuItem.setState_(1 if self.settings.get('cpu', True) else 0)  # Based on loaded settings
        self.menu.addItem_(self.cpuMenuItem)
        
        # Menu Item for GPU
        self.gpuMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("GPU", "toggleGPU:", "")
        self.gpuMenuItem.setState_(1 if self.settings.get('gpu', False) else 0)  # Based on loaded settings
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

    def ensure_cpu_temp_built(self):
        config_path = 'config.toml'
        if not os.path.isfile(config_path):
            # Ensure the `osx-cpu-temp` is built and available
            project_dir = 'osx-cpu-temp-master'
            bin_dir = 'bin'
            
            # Run `make` to build the executable
            subprocess.run(['make'], cwd=project_dir, check=True)
            
            # Ensure the bin directory exists
            if not os.path.exists(bin_dir):
                os.makedirs(bin_dir)
            
            # Move the executable to the bin directory
            executable_src = os.path.join(project_dir, 'osx-cpu-temp')
            executable_dst = os.path.join(bin_dir, 'osx-cpu-temp')
            if os.path.isfile(executable_src):
                os.rename(executable_src, executable_dst)
                self.cpu_temp_cmd = executable_dst
                
                # Create a default config.toml file
                self.create_default_config()
            else:
                raise FileNotFoundError(f"Expected executable not found: {executable_src}")

    def create_default_config(self):
        default_settings = {
            'cpu': True,
            'gpu': False,
            'fahrenheit': False
        }
        with open('config.toml', 'w') as config_file:
            toml.dump(default_settings, config_file)

    def load_settings(self):
        config_path = 'config.toml'
        if os.path.isfile(config_path):
            self.settings = toml.load(config_path)
            self.use_fahrenheit = self.settings.get('fahrenheit', False)
        else:
            # Default settings if config.toml is missing
            self.settings = {
                'cpu': True,
                'gpu': False,
                'fahrenheit': False
            }
            self.use_fahrenheit = False

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
            self.save_settings()

    def toggleFahrenheit_(self, sender):
        if not self.fahrenheitMenuItem.state():
            self.use_fahrenheit = True
            self.fahrenheitMenuItem.setState_(1)
            self.celsiusMenuItem.setState_(0)
            self.updateTemperature_(None)
            self.save_settings()

    def toggleCPU_(self, sender):
        current_state = self.cpuMenuItem.state()
        self.cpuMenuItem.setState_(0 if current_state else 1)
        self.updateTemperature_(None)
        self.save_settings()

    def toggleGPU_(self, sender):
        current_state = self.gpuMenuItem.state()
        self.gpuMenuItem.setState_(0 if current_state else 1)
        self.updateTemperature_(None)
        self.save_settings()

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
            # Run the osx-cpu-temp command and get output
            command = [self.cpu_temp_cmd]
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
            command = [self.cpu_temp_cmd, '-g']
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

    def save_settings(self):
        self.settings['cpu'] = self.cpuMenuItem.state() == 1
        self.settings['gpu'] = self.gpuMenuItem.state() == 1
        self.settings['fahrenheit'] = self.use_fahrenheit
        with open('config.toml', 'w') as config_file:
            toml.dump(self.settings, config_file)

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = CPUStatusApp.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()
