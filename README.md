<h1> Raspberry_Pi_Learning </h1>



<h2>Hardware Requirements</h2>
<ul style="list-style-type:circle;">
  <li>A personal desktop/laptop</li>
  <li>Raspberry Pi 3 - <i>(The model B+ was used for this setup)</i></li>
  <li>Raspberry Pi Camera w/ ribbon cable</li>
  <li>5V Power supply <i>(preferably w/ 1.5A or higher)</i></li>
  <li>PC Monitor or TV for the display w/ HDMI connection</li>
  <li>HDMI Cable</li>
  <li>Standard USB Keyboard</li>
  <li>Standard USB or Bluetooth Mouse <i>(USB would be easier)</i></li>
  <li>Micro SD Card w/ 16GB or more <i>(Sandisk brand has provided the most consistent performance results)</i></li>
</ul>

<h2>Raspberry Pi</h2>
<ul style="list-style-type:circle;">
  <li>What is a Raspberry Pi?
    <ul>
      <li>The Raspberry Pi is a low cost, credit-card sized computer that plugs into a computer monitor or TV, and uses a standard keyboard and mouse. It is a capable little device that enables people of all ages to explore computing, and to learn how to program in languages like Scratch and Python. It’s capable of doing everything you’d expect a desktop computer to do, from browsing the internet and playing high-definition video, to making spreadsheets, word-processing, and playing games.</li>
    </ul>
  </li>
  <li> Where can I find the Operating Systems, or OS's, and more information? 
    <ul>
      <li>
        <a>https://www.raspberrypi.org/downloads/</a>
      </li>
    </ul>
  </li>
  <li> Steps to install the Raspbian OS:
    <ol>
      <li>Download & Install the BalenaEtcher software <a href='https://www.balena.io/etcher/'>HERE</a></li>
      <li>Download & Install the Raspbian OS <a href='https://www.raspberrypi.org/downloads/raspbian/'>HERE</a>
      <br><i>Install the Desktop version w/ the suggested software (the largest download)</i></li>
      <li>Insert the SD Card into your personal laptop/computer & format the SD Card for FAT32
        <ul>
          <li><i>For Windows users, formatting can be done by right-clicking on the drive in your File Explorer window and selecting "FORMAT"</i></li>
          <li><i>For MAC users, formatting can be done by opening the "Disk Utility", selecting the Drive, & Clicking 'ERASE'. The 'MS-DOS(FAT)' option will set it to FAT32.</i></li>
        </ul>
      </li>
      <li>Once the zip file for the RASPBIAN OS has downloaded completely, open the Balena Etcher tool>select the zip file for the Image option>Select the SD Card for the Drive option>Then click flash and confirm the selections.</li>
      </li>
      <li>When it finished, it should say succesful<i>(If it does not say successful, please go back to step ii and try again.)</i></li>
      <li>Connect the rasoberry pi camera & Insert the SD Card.</li>
      <li>Connect the display, mouse, keyboard, & then the power supply.</li>
      <li>Finally, follow the prompts to setup the wifi & user settings then reboot as instructed.</li>
    </ol>
  </li>
</ul>


<h2>Initial Setup</h2>
<h3>Enter the following commads in order using the terminal window</h3>
<ol>
  <li>sudo apt-get update && sudo apt-get upgrade</li>
  <li>sudo apt-get install build-essential cmake unzip pkg-config</li>
  <li>sudo apt-get install libjpeg-dev libpng-dev libtiff-dev</li>
  <li>sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev</li>
  <li>sudo apt-get install libxvidcore-dev libx264-dev</li>
  <li>sudo apt-get install libgtk-3-dev</li>
  <li>sudo apt-get install libcanberra-gtk*</li>
  <li>sudo apt-get install libatlas-base-dev gfortran</li>
  <li><b>ONLY IF YOU DO NOT HAVE PYTHON 3 INSTALLED ALREADY:</b>
    <br>sudo apt-get install python3-dev</li>
  <li>sudo pip3 install opencv-python</li>
  <li>sudo pip3 install numpy
  <br><i>(If this doesn't work, it's probably already installed.)</i></li>
  <li>sudo pip3 install gitpython</li>
  <li>sudo pip3 install pandas</li>
</ol>
<h4>Final Few Steps</h4>
<ul>
  <li>Go to the menu (clicking the raspberry icon in the top left hand corner)</li>
  <li>Click on 'Preferences' then 'Raspberry Pi Configuration'</li>
  <li>Go to the 'Interfaces' tab and enable the following
  <br><b><i>DO NOT CHANGE THE SETTINGS ON ANY OF THE OTHER INTERFACE ITEMS</i></b></li>
    <ul style="list-style-type:disc;">
      <li>SSH</li>
      <li>Camera</li>
      <li>VNC</li>
    </ul>
  <li>Click OK, then reboot as instructed.</li>
  <li>After rebooting you should be ready to practice with OpenCV!</li>
<ul>
