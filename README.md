# - Fortron -

### About The Project
Pacemakers are vital devices for people with abnormal heart conditions, allowing them to experience a natural pulse through electrical stimulation. This project focuses on developing a model of a pacemaker, simulating its functionality across different pacing modes to treat different cardiac conditions. 

Please read through the documentation for further details.

Through model-based code generation and a python gui, we created the following features:
- 7 unique pacemaker modes (AOO, VOO, AAI, VVI, AOOR, VOOR, AAIR, VVIR)
- Real-time electrocardiogram display

## Technology Stack
[Python](https://www.python.org/) | [Matlab Simulink](https://www.mathworks.com/products/simulink.html) | [PyQt](https://doc.qt.io/qtforpython-5/index.html#) | [NXP FRDM K64F Board](https://www.nxp.com/design/design-center/development-boards/freedom-development-boards/mcu-boards/freedom-development-platform-for-kinetis-k64-k63-and-k24-mcus:FRDM-K64F) | [J-Link](https://www.segger.com/downloads/jlink/)

## Showcase 
#### DCM - Device Control Monitor
<p align="center">
  <img src="images\dcm.png" alt="Intro Screen Dark" />
  <br>
  <em>The Main Interface</em>
</p>

<p align="center">
  <img src="images\dcm_login.png" alt="Intro Screen Dark" />
  <br>
  <em>The Login Interface</em>
</p>

#### PaceMaker
<p align="center">
  <img src="images\pacemaker_board1.png" alt="Intro Screen Dark" />
  <br>
  <em>The FRDM-K64F Board</em>
</p>

<p align="center">
  <img src="images\pacemaker_board2.png" alt="Intro Screen Dark" />
  <br>
  <em>Pacemaker (Left) and the Heart (Right)</em>
</p>

<p align="center">
  <img src="images\simulink.png" alt="Intro Screen Dark" />
  <br>
  <em>Simulink Code</em>
</p>

## Installation
#### Prerequisites
1. Python 3.8 or later
2. MATLAB Simulink 2023b or later

#### Python Libraries
```commandline
pip install -r requirements.txt
```

#### MATLAB Simulink Libraries
- Embedded Coder, Fixed-Point Designer, MATLAB Coder, Simulink Check, Simulink Coder, Simulink Coverage, Simulink Design Verifier, Simulink Desktop Real-Time, Simulink Test, and Stateflow
- [Simulink Coder Support Package for NXP FRDM-K64F Board](https://www.mathworks.com/matlabcentral/fileexchange/55318-simulink-coder-support-package-for-nxp-frdm-k64f-board#:~:text=Simulink%C2%AE%20Coder%E2%84%A2%20Support,K64F%20peripherals%20and%20communication%20interfaces.)
- [Kinetis SDK 1.2.0 mainline release](https://www.nxp.com/design/design-center/designs/software-development-kit-for-kinetis-mcus:KINETIS-SDK)
- [V6.20a of the J-Link Software](https://www.segger.com/downloads/jlink/)

In MATLAB, write the following in to the terminal:
```matlab
open([codertarget.freedomk64f.internal.getSpPkgRootDir,
'/src/mw_sdk_interface.c']);
```
Upon opening the device change the following line:
```matlab
{ GPIO_MAKE_PIN(GPIOA_IDX, 0),  MW_NOT_USED},// PTA0, D8
```
into the following:
```matlab
{ GPIO_MAKE_PIN(GPIOC_IDX, 12),  MW_NOT_USED},// PTC12, D8
```

## Contributors
[Jack Coleman](https://www.linkedin.com/in/jack-coleman-75418330b/) |
[Alisa Norenberg](https://www.linkedin.com/in/alisa-norenberg/) |
[Fares Alterawi](https://www.linkedin.com/in/faris-alterawi/) |
[Haaniya Ahmed](https://www.linkedin.com/in/haaniya-ahmed-917927217/) |
[Hamza Alfalo](https://www.linkedin.com/in/hamza-alfalo-452a6b245/) |
[Krishna Chauhan](https://www.linkedin.com/in/krishnac88/)
