from gpiozero import LED, Button
from time import sleep
from random import sample
from signal import pause
import pygame
import os
from random import randint


button_pins = [26, 14, 15, 18, 23, 24, 25, 8, 7]
led_pins =    [2, 3, 4, 17, 27, 22, 10, 9, 11]
buttons = [Button(pin, pull_up=True) for pin in button_pins]
leds = [LED(pin) for pin in led_pins]
#status_led = LED(status_led_pin)
'''
for i in range(40):
    a = randint(0,8)
    leds[a].on
    sleep(0.2)
    leds[a].off
    sleep(0.2)
'''
for i in range(40):
    for led in leds:
        sleep(0.2)
        print(led)
        led.on()
    #print("All water pumps spraying!")
    #sleep(0.5)
    for led in leds:
        sleep(0.2)
        led.off()
    #sleep(0.5)
    