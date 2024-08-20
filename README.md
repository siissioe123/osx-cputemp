# osx-cputemp
![Python](https://img.shields.io/badge/-Python-black?style=flat-square&logo=Python)

## Description 📚
`osx-cputemp` is a simple Python script designed to monitor and display the CPU temperature on macOS systems. It helps you keep an eye on your system's thermal performance and ensures your hardware stays within safe operating temperatures.

## 📝 Instructions

### 📚 Prerequisites
- Install Python from the [official website](https://www.python.org/) (latest version) and ensure it is added to the system PATH and environment variables.
- Homebrew

  Install Homebrew by running:
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```

- [osx-cpu-temp](https://github.com/lavoiesl/osx-cpu-temp)

  Install `osx-cpu-temp` via Homebrew:
  ```bash
  brew install osx-cpu-temp
  ```

### Installation 📥
To set up `osx-cputemp`, follow these steps:
1. Download or clone the repository. If you don't have Git, refer to the [official guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
2. Open a terminal.
3. Navigate to the script folder in the terminal.
4. Install the required dependencies by running:
  ```bash
  pip install -r requirements.txt
  ```

### Usage 🚀
1. Navigate to the script folder in the terminal.
2. Run the script with Python by executing:
  ```bash
  python main.py
  ```

### Additional Details
- Upon the first launch, the necessary files, including the compiled version of `osx-cpu-temp`, will be created automatically.
- The folder `osx-cpu-temp-master` is sourced from [https://github.com/lavoiesl/osx-cpu-temp](https://github.com/lavoiesl/osx-cpu-temp). It remains as a folder for modularity.
- The `bin` folder contains the compiled version of `osx-cpu-temp`, which is generated during the initial setup.
- The `config.toml` file is used to manage and maintain configuration settings for the script.

## 🔄 Compatibility
- This script is designed for macOS systems only. 🖥️

## 📌 Notes
- This script is intended for personal use only. 🎓
- The script is currently very basic and lacks advanced features. Feel free to contribute by opening a pull request or issue.
- Performance and accuracy may vary. Contributions to improve the script are welcome.

## Bug Reporting 🐞
If you encounter any bugs or issues while using `osx-cputemp`, please report them by opening an issue on the GitHub repository. Provide detailed information to help us reproduce and resolve the problem.

## Author 🤓
`osx-cputemp` was developed by [Siissioe123](https://github.com/siissioe123).

## License 📜
This software is released under the [GPL-3.0 license](LICENSE) [(GNU General Public License)](https://www.gnu.org/licenses/gpl-3.0.html), maintained by the [Free Software Foundation](https://www.fsf.org).
