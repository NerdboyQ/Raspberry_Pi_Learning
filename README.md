# Raspberry_Pi_Learning

## Hardware Requirements

* A personal desktop/laptop
* Raspberry Pi 3 - _(The model B+ was used for this setup)_
* Raspberry Pi Camera w/ ribbon cable
* 5V Power supply _(preferably w/ 1.5A or higher)_
* PC Monitor or TV for the display w/ HDMI connection
* HDMI Cable
* Standard USB Keyboard
* Standard USB or Bluetooth Mouse _(USB would be easier)_
* Micro SD Card w/ 16GB or more _(Sandisk brand has provided the most consistent performance results)_


## Raspberry Pi

* What is a Raspberry Pi?
    
      * The Raspberry Pi is a low cost, credit-card sized computer that plugs into a computer monitor or TV, and uses a standard keyboard and mouse. It is a capable little device that enables people of all ages to explore computing, and to learn how to program in languages like Scratch and Python. It’s capable of doing everything you’d expect a desktop computer to do, from browsing the internet and playing high-definition video, to making spreadsheets, word-processing, and playing games.
    
  
*  Where can I find the Operating Systems, or OS's, and more information? 
    
      * 
        [https://www.raspberrypi.org/downloads/](https://www.raspberrypi.org/downloads/)
      
    
  
## Steps to install the Raspbian OS:
    
1. Download & Install the BalenaEtcher software [HERE](https://www.balena.io/etcher/)
2. Download & Install the Raspbian OS [HERE](https://www.raspberrypi.org/downloads/raspbian/)
_Install the Desktop version w/ the suggested software (the largest download)_
3. Insert the SD Card into your personal laptop/computer & format the SD Card for FAT32

   * _For Windows users, formatting can be done by right-clicking on the drive in your File Explorer window and selecting "FORMAT"_
   * _For MAC users, formatting can be done by opening the "Disk Utility", selecting the Drive, & Clicking 'ERASE'. The 'MS-DOS(FAT)' option will set it to FAT32._


4. Once the zip file for the RASPBIAN OS has downloaded completely, open the Balena Etcher tool>select the zip file for the Image option>Select the SD Card for the Drive option>Then click flash and confirm the selections.

5. When it finished, it should say succesful_(If it does not say successful, please go back to step ii and try again.)_
6. Connect the rasoberry pi camera & Insert the SD Card.
7. Connect the display, mouse, keyboard, & then the power supply.
8. Finally, follow the prompts to setup the wifi & user settings then reboot as instructed.
    
  



## Initial Setup
### Enter the following commads in order using the terminal window
```
   sudo apt-get update && sudo apt-get upgrade
   sudo apt-get install build-essential cmake unzip pkg-config
   sudo apt-get install libjpeg-dev libpng-dev libtiff-dev
   sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
   sudo apt-get install libxvidcore-dev libx264-dev
   sudo apt-get install libgtk-3-dev
   sudo apt-get install libcanberra-gtk*
   sudo apt-get install libatlas-base-dev gfortran
```
>   **ONLY IF YOU DO NOT HAVE PYTHON 3 INSTALLED ALREADY:**
```
   sudo apt-get install python3-dev
   sudo pip3 install opencv-python
   sudo pip3 install numpy
```
>  _(If this doesn't work, it's probably already installed.)_
```
   sudo pip3 install gitpython
   sudo pip3 install pandas
```
#### Final Few Steps

1. Go to the menu (clicking the raspberry icon in the top left hand corner)
2. Click on 'Preferences' then 'Raspberry Pi Configuration'
3. Go to the 'Interfaces' tab and enable the following   
**_DO NOT CHANGE THE SETTINGS ON ANY OF THE OTHER INTERFACE ITEMS_**

    * SSH
    * Camera
    * VNC

4. Click OK, then reboot as instructed.
5. After rebooting you should be ready to practice with OpenCV!

