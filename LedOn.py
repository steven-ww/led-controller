import RPi.GPIO as GPIO
import time
import sys
import getopt
from datetime import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
p=GPIO.PWM(17,50)
p.start(0)

# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]

# Options
options = "ht:n:f:"

# Long options
long_options = ["help", "twilight", "timeon", "timeoff"]
n = len(sys.argv)


# Parsing argument
arguments, values = getopt.getopt(argumentList, options, long_options)

try:
  # checking each argument
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h", "--Help"):
            print ("-h or --help : this message")
            print ("-t or --twilight to set the twilight time")
            print("-n or --ontime to set the time the led should start the on cycle in the format HH:MM e.g. 07:30")
            print("-f or --offtime to set the time the led should start the off cycle in the format HH:MM e.g. 17:30")
        elif currentArgument in ("-t", "--twilight"):
            print ("Twilight hours:", currentValue)
            twilight = int(currentValue)
        elif currentArgument in ("-n", "--ontime"):
            print ("On Time:", currentValue)
            on_time = time.strptime(currentValue, "%H:%M")
            on_hour = on_time[3]
            on_min = on_time[4]
        elif currentArgument in ("-f", "--offtime"):
            print ("Off Time:", currentValue)
            off_time = time.strptime(currentValue, "%H:%M")
            off_hour = off_time[3]
            off_min = off_time[4]

except getopt.error as err:
    # output error, and return with an error code
    print (str(err))
    sys.exit()


if n < 4:
    print("Not Enough Parameters")
    print("Please supply the on time, off time, twilight hours")
    print("Use -h or --help for details")
    sys.exit()


minutes_in_twilight = twilight * 60
sleep_for = minutes_in_twilight/100 * 60

print("Sleep For", sleep_for)

while True:
    now = datetime.now()
    current_hour = int(now.strftime("%H"))
    current_min = int(now.strftime("%M"))
    current_sec = now.strftime("%S")
    print("Current time", now)
    print("")

    if current_hour == on_hour:
        if current_min == on_min:
            print("Switching on..")
            for i in range(0,101,1): #Increase in Brightness
                p.ChangeDutyCycle(i)
                print("Setting Brightness to", i)
                time.sleep(sleep_for)
    if current_hour == off_hour:
        if current_min == off_min:
            print("Switching off")
            for i in range(100,0,-1): #Decrease in Brightness
                p.ChangeDutyCycle(i)
                print("Setting Brightness to", i)
                time.sleep(sleep_for)

    time.sleep(15)
