from signal import pause
from gpiozero import Button

# Initialize pin 4 (BCM) as an input with an internal pull-up resistor
# Connect your trigger source (0V to 3.3V max) to GPIO 4 and Ground to GND
trigger_pin = Button(4, pull_up=False)  # GPIO 4, pin 7 (can toggle pull_up to False if you want to use an external pull-down resistor)


def voltage_triggered():
  print("Voltage trigger detected (High)! Running action...")


# Set the callback for when the pin goes HIGH (rising edge)
trigger_pin.when_pressed = voltage_triggered

print("Waiting for voltage trigger on GPIO 4...")
pause()