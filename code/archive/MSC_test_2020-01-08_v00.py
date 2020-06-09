# MSC_test_2020-01-08_v00.py
# uses revised adafruit_pybadger and adafruit_crickit
# uses cedargrove_pypanel to abstract Crickit and PyBadge/PyGamer

import time
import random as rand
from cedargrove_pypanel import *
from unit_converter.chronos import adjust_dst

### SETTINGS ###
clock_type        = "repl"     # describes clock type
clock_zone        = "Pacific"  # free text
clock_24_hour     = True       # 24-hour clock; 12-hour AM/PM
clock_auto_dst    = True       # automatic US DST
clock_chime_tick  = True      # enable tick sound
clock_chime_tick_source = "tick_soft.wav"
clock_chime_half  = False      # enable half-hour chime sound
clock_chime_hour  = False      # enable hourly chime sound
clock_chime_alarm = False      # enable alarm chime sound

display_brightness = 0.5       # display brightness 0.0 to 1.0


if ds3231.lost_power:
    print("power lost since last setting")
    print("REPL setting mode")
    set_yr  = int(input("enter year (YYYY):"))
    set_mon = int(input("enter month (MM):"))
    set_dom = int(input("enter day-of-month (DD):"))
    set_hr  = int(input("enter 24-hour clock hour (hh):"))
    set_min = int(input("enter minute (mm):"))
    # Set RTC time for testing
    #                  year, mon, date, hour, min, sec, wday, yday, isdst
    ds3231.datetime = time.struct_time((set_yr, set_mon, set_dom, set_hr, set_min, 0, -1, -1, -1))

while True:
    # Check datetime and adjust if DST
    current, is_dst = adjust_dst(ds3231.datetime)

    if is_dst:
        flag_text = clock_zone + "DST"
    else:
        flag_text = clock_zone[0] + "ST"

    # Print the adjusted time
    print("{}: {}/{}/{} {:02}:{:02}:{:02}  week_day={}".format(flag_text,
          current.tm_mon, current.tm_mday, current.tm_year,
          current.tm_hour, current.tm_min, current.tm_sec,
          current.tm_wday))

    prev_sec = current.tm_sec
    while current.tm_sec == prev_sec:
        current = ds3231.datetime

    if clock_chime_tick:
        panel.play_file(clock_chime_tick_source)


"""
panel.pixels.fill = ((0, 0, 0))  # clear neopixels
panel.brightness = DISPLAY_BRIGHTNESS  # set initial display brightness

for i in range(0,3): print(" ")
if panel.has_joystick: print("Joystick found")  # if PyGamer
else: print("No joystick")

test_delay = 0.25  # seconds between tests

print(" ")
print("Stemma devices found:")
for i in range(0, len(stemma)):
    print("%s : %s" % (stemma[i][0], stemma[i][2]))
if len(stemma) == 0: print("--none--")
print(" ")
time.sleep(test_delay)

# Test of adjust_dst helper

if ds3231.lost_power:
    print("power lost since last setting")
    time.sleep(test_delay)

# Set RTC time for testing
#                  year, mon, date, hour, min, sec, wday, yday, isdst
ds3231.datetime = time.struct_time((2020, 3, 16, 22, 59, 55, 6, -1, -1))
current = ds3231.datetime
hour = current.tm_hour

print(current)
print(time.mktime(current))

time.sleep(3)

current1 = ds3231.datetime
print(current1)
print(time.mktime(current1))

print("equal", current1 == current)
print("less than", current < current1)
print("less than", time.mktime(current) < time.mktime(current1))
print(time.mktime(current1) - time.mktime(current))

time.sleep(3)

while True:
    if PIXEL:
        panel.pixels[0] = ((128, 12, 128))  # dim purple neopixel

    if TICK:
        panel.play_file(TICK_SOURCE)
    else:
        time.sleep(0.05)

    print("---")
    dst_flag, month, date, weekday, hour = adjust_dst(current)
    if dst_flag: dst_text = "DST"
    else: dst_text = "xST"

    print(current)
    print('{}: {}/{}/{} {:02}:{:02}:{:02}'.format(dst_text, current.tm_mon,
          date, current.tm_year, hour,
          current.tm_min, current.tm_sec))
    print(weekday)

    if PIXEL:
        panel.pixels[0] = ((0, 0, 0))  # dark neopixel

    prev_sec = current.tm_sec
    while current.tm_sec == prev_sec:
        current = ds3231.datetime


# set Crickit on-board NeoPixel to purple
crickit.onboard_pixel[0] = (255, 24, 255)

# PyBadge test
panel.pixels.fill((255, 24, 255))  # dim purple neopixels
panel.brightness = 0.9  # set initial display brightness
panel.show_badge(name_string="RobotFriend", hello_scale=2, my_name_is_scale=1, name_scale=2)
time.sleep(test_delay)
panel.show_terminal()

# Text area test
# Set text, font, and color
text = "HELLO WORLD"
font = terminalio.FONT
# font = pp.bitmap_font.load_font("/Helvetica-Bold-16.bdf")
color = 0x0000FF
# Create the text label
text_area = label.Label(font, text="HELLO WORLD", color=0x00FF00)
# Set the location
text_area.x = 50
text_area.y = 60
# Show it
display.show(text_area)
time.sleep(test_delay)

# Bitmap graphics test
with open("/RobotFriend_tiny.bmp", "rb") as bitmap_file:
    # Setup the file as the bitmap data source
    bitmap = displayio.OnDiskBitmap(bitmap_file)
    # Create a TileGrid to hold the bitmap
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())
    # Create a Group to hold the TileGrid
    group = displayio.Group()
    # Add the TileGrid to the Group
    group.append(tile_grid)
    # Add the Group to the Display
    display.show(group)
    display.wait_for_frame()
    time.sleep(test_delay)

# Turtle graphics test
def hilbert2(step, rule, angle, depth, t):
    if depth > 0:
        a = lambda: hilbert2(step, "a", angle, depth - 1, t)
        b = lambda: hilbert2(step, "b", angle, depth - 1, t)
        left = lambda: t.left(angle)
        right = lambda: t.right(angle)
        forward = lambda: t.forward(step)
        if rule == "a":
            left(); b(); forward(); right(); a(); forward(); a(); right(); forward(); b(); left()
        if rule == "b":
            right(); a(); forward(); left(); b(); forward(); b(); left(); forward(); a(); right()

turtle = turtle(board.DISPLAY)
turtle.penup()

turtle.goto(-45, -45)
turtle.pendown()
hilbert2(6, "a", 90, 4, turtle)

time.sleep(test_delay)

# test of solenoid on drive_1
def soleniod():  # helper for soleniod on feather_drive_1
    crickit.feather_drive_1.fraction = 1.0
    time.sleep(0.05)
    crickit.feather_drive_1.fraction = 0.0

soleniod()

# test of Servo 1
crickit.servo_1.angle = 90
time.sleep(test_delay)
crickit.servo_1.angle = 0
time.sleep(test_delay)
crickit.servo_1.angle = 180
time.sleep(test_delay)

print("MSC_test_2020-01-08_v00.py")
print("--------------------------")

# Wave file to speaker test
panel.play_tone(440, 0.25)
time.sleep(0.25)
panel.play_file("rimshot.wav")
time.sleep(test_delay)

t1 = time.time()
select_state = True
light_sensor = panel.light / 65536
panel.show_terminal()

while True:
    t2 = time.monotonic()

    if panel.button.select:
        if select_state:
            panel.show_badge(name_string="RobotFriend", hello_scale=2, my_name_is_scale=1, name_scale=2)
        else:
            panel.show_terminal()
        while panel.button.select:
            time.sleep(0.1)  # allow button to release
        select_state = not(select_state)

    print("----------")
    panel.pixels.fill([0, 0, 0])
    if panel.has_joystick:
        print("Joystick:", panel.joystick)  # if PyGamer

    # print(panel.button)  # to show state of buttons

    light_sensor = ((panel.light / 65536) + light_sensor) /2
    x, y, z = panel.acceleration
    print("Time:%6.0f, Light:%1.2f" % (t2, light_sensor))
    print("X:%2.1f, Y:%2.1f, Z:%2.1f" % (x, y, z))
    # scale and format for plotter
    print((int(light_sensor * 100) / 100, int(x * 10) / 100,
           int(y * 10) / 100, int(z * 10) / 100))

    rgb = [rand.randint(64, 255), rand.randint(64, 255), rand.randint(64, 255)]
    panel.pixels[int(t2) % 5] = rgb
    crickit.onboard_pixel[0]  = rgb

    panel.auto_dim_display(delay=20, movement_threshold=1)

    time.sleep(test_delay)"""
