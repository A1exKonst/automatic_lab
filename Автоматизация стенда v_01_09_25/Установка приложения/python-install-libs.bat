@echo off
chcp 65001
python -m ensurepip --default-pip
echo Установка 1/6 pyserial
pip install pyserial==3.5
echo Установлен pyserial
echo
echo Установка 2/6 numpy
pip install numpy==2.2.6
echo Установлен numpy
echo
echo Установка 3/6 pandas
pip install pandas==2.3.1
echo Установлен pandas
echo
echo Установка 4/6 sympy
pip install sympy==1.14.0
echo Установлен sympy
echo
echo Установка 5/6 matplotlib
pip install matplotlib==3.10.3
echo Установлен matplotlib
echo
echo Установка 6/6 pyqt5
pip install pyqt5==5.15.11
echo Установлен pyqt5
echo
echo Конец установки библиотек python. 
echo Нажмите, любую клавишу, чтобы завершить
pause
