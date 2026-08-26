from gpiozero import LED
from time import sleep

# Initialize the LED on GPIO pin 17
led = LED(5)

print("LED is blinking... Press Ctrl+C to stop.")

try:
    while True:
        led.on()       # Turn the LED on
        sleep(1)       # Wait for 1 second
        led.off()      # Turn the LED off
        sleep(1)       # Wait for 1 second

except KeyboardInterrupt:
    print("\nProgram stopped by user.")