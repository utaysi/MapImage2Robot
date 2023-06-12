# Constructor Robot with a Given Map of Buildings

This repository includes the CMP sub-system software of our graduation capstone project. 

The project is conducted by Şevval Çolak, Uğur Tayşi, Zeynep Süzen and Doğacan Şahin. It is an interdisciplinary project between the Computer Engineering and Mechatronics Engineering departments. The project is called "Constructor Robot with a Given Map of Buildings". The task of Computer Engineering students includes the use of image processing in order to evaluate the given map of buildings. This is done using the OpenCV library for processing the map images, and the PyVista library for the 3D visualization of the given maps. The results of the image processing steps are then transferred over to the robot built by the Mechatronics Engineering sub-team via Arduino serial connection. The task of Mechatronics Engineering students includes building a robot which takes the input given from the Computer Engineering students and uses that data to build the city physically using blocks.

![Screenshot2](screenshots/2.gif)
![Screenshot1](screenshots/1.png)

## System Requirements
- Python
- Tesseract (Installation Guide: https://github.com/UB-Mannheim/tesseract/wiki)
- Arduino UNO (If you enable the optional serial connection part of the code by uncommenting, you will need to have an Arduino device connected to your computer.)

Before running the code install each Python library with the pip command: 
```
pip install pyvista opencv-python numpy pytesseract webcolors pyserial
```

###### Current Todo: 

- ~~[DONE] Forward array data into new simplified array for robot output (coords + height only)~~ 
- ~~[DONE] Implement Arduino stuff~~
- ~~[DONE] Add auto 3d rotation gif~~
- ~~[DONE] Building order of text output and 3D doesn't currently match. Fix text output building order.~~
- ~~[DONE] Color reading. Currently getting blue/black instead of red.~~
- ~~[DONE] Fix 3D Visualization Scaling~~
- ~~[DONE] Make sure all variables are linked to map input variables and not constants on final working version~~
- ~~[DONE] Switch to 150x150 map with 7x7 buildings~~
- ~~[DONE] Add exlusion zone in the middle and change input maps accordingly after getting exact zone coords from Zeynep~~
- ~~[DONE] Add OCR to initial image processing~~