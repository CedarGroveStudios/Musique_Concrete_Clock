# MCC_code_2020-06-09_v01.py
# Cedar Grove Studios
# uses Robot_Friend_FeatherWing.cedargrove_pypanel.py
# uses cedargrove unit_converter library
# uses cedargrove clock_builder library (display, set_time, chime)

import time
import board
import adafruit_ds3231
from   analogio                      import AnalogIn
from   unit_converter.chronos        import adjust_dst
from   cedargrove_clock_builder.repl_display    import ReplDisplay
from   cedargrove_clock_builder.pybadge_display import PyBadgeDisplay  # PyBadge display
# from   clock_display.led_14x4seg     import Led14x4Display  # 14-segment LED
# from   clock_display.led_7x4seg      import Led7x4Display   # 7-segment LED
# from   cedargrove_pypanel import *
# print(stemma)  # show Stemma-attached device list
from adafruit_crickit import crickit


i2c = board.I2C()
ds3231 = adafruit_ds3231.DS3231(i2c)

batt = AnalogIn(board.A6)
print("Battery: {:01.2f} volts".format((batt.value / 65520) * 6.6))

### SETTINGS ###
clock_display  = ["pybadge", "repl"]  # List of active display(s)
clock_zone     = "Pacific"  # Name of local time zone
clock_24_hour  = False      # 24-hour clock = True; 12-hour AM/PM = False
clock_auto_dst = True       # Automatic US DST = True
clock_sound    = True       # Sound is active
clock_tick     = True       # One-second tick sound

servo_1_start    = 70         # Resting servo position
servo_1_end      = 140        # Active servo position
servo_2_start    = 140         # Resting servo position
servo_2_end      = 70        # Active servo position

### Instatiate displays

#  4-digit 14-segment LED alphanumeric display
# led_disp = Led14x4Display(clock_zone, clock_24_hour, clock_auto_dst,
#                           clock_sound, brightness=2, debug=False)

#  4-digit 7-segment LED alphanumeric display
# led_disp  = Led7x4Display(clock_zone, clock_24_hour, clock_auto_dst,
#                           clock_sound, brightness=2, debug=False)

# PyBadge display
pybadge_disp  = PyBadgeDisplay(clock_zone, clock_24_hour, clock_auto_dst,
                               clock_sound, brightness=0.5, debug=False)

pybadge_disp.battery = (batt.value / 65520) * 6.

#  REPL display
repl_disp = ReplDisplay(clock_zone, clock_24_hour, clock_auto_dst,
                        clock_sound, debug=False)

### Instatiate Crickit
from adafruit_crickit import crickit
crickit.init_neopixel(1, brightness=0.01) # must call this first
crickit.onboard_pixel.brightness = 0.01
crickit.onboard_pixel[0] = (0, 255, 0)  # green for startup

# Change servo settings.
# crickit.servo_1.actuation_range = 135
# crickit.servo_1.set_pulse_width_range(min_pulse=850, max_pulse=2100)
# crickit.servo_2.actuation_range = 135
# crickit.servo_2.set_pulse_width_range(min_pulse=850, max_pulse=2100)

# Energize the power indicator
crickit.feather_drive_2.fraction = 0.5  # power indicator

### Instatiate chimes
# reset servo to start position and disable
crickit.servo_1.angle = servo_1_start
crickit.servo_2.angle = servo_2_start
time.sleep(0.25)
crickit.servo_1.angle = None  # disable servo
crickit.servo_2.angle = None
time.sleep(0.5)

"""# reset servo to end position and disable (calibrate)
crickit.servo_1.angle = servo_1_end
crickit.servo_2.angle = servo_2_end
time.sleep(0.25)
crickit.servo_1.angle = None  # disable servo
crickit.servo_2.angle = None
time.sleep(0.5)

while True:
    pass"""

### HELPERS ###
def chime(hour, solenoid_hold=0.05, servo_hold=0.2,
          start_1=servo_1_start, end_1=servo_1_end,
          start_2=servo_2_start, end_2=servo_2_end):  # play chime and cuckoo n cycles
    crickit.servo_1.angle = start_1  # wake up servo and move to start
    crickit.servo_2.angle = start_2
    time.sleep(servo_hold)

    if hour > 12:
        hour = hour - 12
    if hour  == 0:  # midnight hour fix
        hour = 12

    for i in range(0, hour):
        crickit.servo_1.angle = end_1  # cu
        time.sleep(servo_hold / 2)
        crickit.feather_drive_1.fraction = 1.0  # chime
        time.sleep(solenoid_hold)
        crickit.feather_drive_1.fraction = 0.0
        time.sleep(servo_hold / 2)
        crickit.servo_1.angle = start_1
        crickit.servo_2.angle = end_2    # coo
        time.sleep(servo_hold)
        crickit.servo_2.angle = start_2
        time.sleep(servo_hold)
    crickit.servo_1.angle = None  # disable servo
    crickit.servo_2.angle = None
    time.sleep(servo_hold)

crickit.onboard_pixel[0] = (255, 0, 0)  # red for chime test

# test the chimes
chime(1)

crickit.onboard_pixel[0] = (255, 24, 255)  # purple for normal operation

# Manually set time upon RTC power failure
if ds3231.lost_power:
    print("--RTC POWER FAILURE--")
    # Set time with REPL
    # ds3231.datetime = repl_disp.set_datetime()

    # Set time with PyBadge
    pybadge_disp.show(ds3231.datetime)
    pybadge_disp.message = "-RTC POWER FAILURE-"

min_flag = half_flag = hour_flag = False

# initiate pybadge display contents
if "pybadge" in clock_display:
    # Check datetime and adjust if DST
    if clock_auto_dst:             # read the RTC and adjust for DST
        current, is_dst = adjust_dst(ds3231.datetime)
    else:
        current = ds3231.datetime  # otherwise, just read the RTC
        is_dst = False

    pybadge_disp.dst = is_dst
    pybadge_disp.show(current)

while True:
    if pybadge_disp.panel.button.b:
        chime(1)

    # Check datetime and adjust if DST
    if clock_auto_dst:             # read the RTC and adjust for DST
        current, is_dst = adjust_dst(ds3231.datetime)
    else:
        current = ds3231.datetime  # otherwise, just read the RTC
        is_dst = False

    # update REPL display
    if "repl" in clock_display:
        repl_disp.dst = is_dst
        repl_disp.show(current)

    # update led display
    if "led" in clock_display:
        led_disp.dst    = is_dst
        led_disp.colon  = not led_disp.colon
        led_disp.show   = current  # refresh LED display

    if "pybadge" in clock_display:
        pybadge_disp.colon  = not pybadge_disp.colon  # auto-refresh

        # Check to see if time was set
        new_xst_datetime, clock_sound, update_flag = pybadge_disp.set_datetime(ds3231.datetime)
        if update_flag:  # If so, update RTC Std Time with new datetime
           ds3231.datetime = new_xst_datetime
           print("RTC time was set")

    # play tick sound
    if clock_sound and clock_tick:
        pybadge_disp.tick()

    if pybadge_disp.panel.light < 5000:
        pybadge_disp.panel.brightness = 0.025
        crickit.feather_drive_2.fraction = 0.05  # power indicator
    else:
        pybadge_disp.panel.brightness = 0.5
        crickit.feather_drive_2.fraction = 0.5  # power indicator

    # Do something every minute
    if current.tm_sec == 0 and not min_flag:
        # do something here
        print("every MIN")

        print("Battery: {:01.2f} volts".format((batt.value / 65520) * 6.6))

        # Check light level and adjust display/pwr brightness
        print(pybadge_disp.panel.light)

        # update PyBadge display
        if "pybadge" in clock_display:
            pybadge_disp.dst = is_dst
            pybadge_disp.show(current)
            pybadge_disp.battery = (batt.value / 65520) * 6.6

        min_flag = True
    elif current.tm_sec > 0:
        min_flag = False

    # Do something every half-hour
    if current.tm_min == 30 and not half_flag:
        # do something here
        print("every HALF")
        chime(1)
        half_flag = True
    elif current.tm_min > 30:
        half_flag = False

    # Do something every hour
    if current.tm_min == 0 and not hour_flag:
        # do something here
        print("every HOUR")
        chime(current.tm_hour)
        hour_flag = True
    elif current.tm_min > 0:
        hour_flag = False

    # wait a second before looping
    prev_sec = current.tm_sec
    while current.tm_sec == prev_sec:  # wait a second before looping
        current = ds3231.datetime
        
