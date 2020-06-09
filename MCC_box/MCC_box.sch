EESchema Schematic File Version 4
LIBS:MCC_box-cache
EELAYER 26 0
EELAYER END
$Descr USLegal 14000 8500
encoding utf-8
Sheet 1 1
Title "MCC_box"
Date "2020-05-08"
Rev "v00"
Comp "Cedar Grove Studios"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L power:GND #PWR025
U 1 1 5CF11F0C
P 13650 2450
F 0 "#PWR025" H 13650 2200 50  0001 C CNN
F 1 "GND" H 13655 2277 50  0000 C CNN
F 2 "" H 13650 2450 50  0001 C CNN
F 3 "" H 13650 2450 50  0001 C CNN
	1    13650 2450
	1    0    0    -1  
$EndComp
Wire Wire Line
	13650 2450 13650 2350
Text Notes 11950 6625 0    50   ~ 0
(Unused)
$Comp
L Adafruit:Feather_M4_Express M1
U 1 1 5EB63364
P 7100 4000
F 0 "M1" H 7100 4973 50  0000 C CNN
F 1 "Feather_M4_Express" H 7100 5000 50  0001 C CNN
F 2 "Adafruit:Adafruit Feather" H 7100 4050 50  0001 C CNN
F 3 "" H 7100 4050 50  0001 C CNN
	1    7100 4000
	1    0    0    -1  
$EndComp
$EndSCHEMATC
