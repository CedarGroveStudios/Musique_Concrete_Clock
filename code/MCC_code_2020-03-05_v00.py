# MCC_code_2020-03-05_v00.py
# Cedar Grove Studios
# uses cedargrove unit_converter library
# uses cedargrove clock_builder library (display, set_time, chime)

import time
import board
import adafruit_ds3231
from analogio import AnalogIn
from unit_converter.chronos          import adjust_dst
from clock_display.repl_display      import ReplDisplay
from clock_display.displayio_display import DisplayioDisplay  # PyBadge/PyGamer display
# from clock_display.led_14x4seg       import Led14x4Display  # 14-segment LED
# from clock_display.led_7x4seg        import Led7x4Display   # 7-segment LED

i2c = board.I2C()
ds3231 = adafruit_ds3231.DS3231(i2c)

batt = AnalogIn(board.A6)
print("Battery: {:01.2f} volts".format((batt.value / 65520) * 6.6))

### SETTINGS ###
clock_display  = ["displayio", "repl"]  # List of active display(s)
clock_zone     = "Pacific"  # Name of local time zone
clock_24_hour  = False      # 24-hour clock = True; 12-hour AM/PM = False
clock_auto_dst = True       # Automatic US DST = True
clock_sound    = True       # Sound is active = True
clock_tick     = True       # One-second tick sound

### Instatiate displays

#  4-digit 14-segment LED alphanumeric display
# led_disp = Led14x4Display(clock_zone, clock_24_hour, clock_auto_dst,
#                           clock_sound, brightness=2, debug=False)

#  4-digit 7-segment LED alphanumeric display
# led_disp  = Led7x4Display(clock_zone, clock_24_hour, clock_auto_dst,
#                           clock_sound, brightness=2, debug=False)

# Displayio display
displayio_disp  = DisplayioDisplay(clock_zone, clock_24_hour, clock_auto_dst,
                                   clock_sound, brightness=0.5, debug=False)

displayio_disp.battery = (batt.value / 65520) * 6.6

#  REPL display
repl_disp = ReplDisplay(clock_zone, clock_24_hour, clock_auto_dst,
                        clock_sound, debug=False)

### Instatiate time setter
# (none)

### Instatiate chimes
# (none)

### HELPERS ###

# Manually set time upon RTC power failure
if ds3231.lost_power:
    print("--RTC POWER FAILURE--")
    # Set time with REPL
    # ds3231.datetime = repl_disp.set_datetime()

    # Set time with DisplayIO
    displayio_disp.show(ds3231.datetime)
    displayio_disp.message = "-RTC POWER FAILURE-"

min_flag = half_flag = hour_flag = False

# initiate displayio display contents
if "displayio" in clock_display:
    # Check datetime and adjust if DST
    if clock_auto_dst:             # read the RTC and adjust for DST
        current, is_dst = adjust_dst(ds3231.datetime)
    else:
        current = ds3231.datetime  # otherwise, just read the RTC
        is_dst = False

    displayio_disp.dst = is_dst
    displayio_disp.show(current)

while True:
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

    if "displayio" in clock_display:
        displayio_disp.colon  = not displayio_disp.colon  # auto-refresh

        # Check to see if time was set
        new_xst_datetime, clock_sound, update_flag = displayio_disp.set_datetime(ds3231.datetime)
        if update_flag:  # If so, update RTC Std Time with new datetime
           ds3231.datetime = new_xst_datetime
           print("RTC time was set")

    # play tick sound
    if clock_sound and clock_tick:
        displayio_disp.tick()

    # Do something every minute
    if current.tm_sec == 0 and not min_flag:
        # do something here
        print("every MIN")

        print("Battery: {:01.2f} volts".format((batt.value / 65520) * 6.6))

        # update displayio display
        if "displayio" in clock_display:
            displayio_disp.dst = is_dst
            displayio_disp.show(current)
            displayio_disp.battery = (batt.value / 65520) * 6.6

        min_flag = True
    elif current.tm_sec > 0:
        min_flag = False

    # Do something every half-hour
    if current.tm_min == 30 and not half_flag:
        # do something here
        print("every HALF")
        half_flag = True
    elif current.tm_min > 30:
        half_flag = False

    # Do something every hour
    if current.tm_min == 0 and not hour_flag:
        # do something here
        print("every HOUR")
        hour_flag = True
    elif current.tm_min > 0:
        hour_flag = False

    # wait a second before looping
    prev_sec = current.tm_sec
    while current.tm_sec == prev_sec:  # wait a second before looping
        current = ds3231.datetime
        
