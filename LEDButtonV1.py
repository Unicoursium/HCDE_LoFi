from gpiozero import LED, Button
from signal import pause
from random import sample
from time import sleep

# GPIO mappings
led_pins =    [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 13, 19]
button_pins = [26,14,15,18,23,24,25,8,7,16,20,21]

# Initialize LEDs and buttons
leds = [LED(pin) for pin in led_pins]
buttons = [Button(pin, pull_up=True) for pin in button_pins]

# Global game state
current_stage = 0
confirmed_buttons = []
stage_correct_options = []
input_enabled = True

# Determine correct button count per stage
def correct_option_count(stage):
    if stage <= 3:   return 5
    elif stage <= 6: return 4
    elif stage <= 8: return 3
    elif stage <=10: return 2
    else:            return 1

# Set correct options for current stage
def set_next_stage_options():
    global stage_correct_options
    remaining_buttons = [i for i in range(12) if i not in confirmed_buttons]
    count = correct_option_count(current_stage)
    if len(remaining_buttons) < count:
        count = len(remaining_buttons)
    stage_correct_options = sample(remaining_buttons, count)
    print(f"[Stage {current_stage+1}] Possible correct buttons: {[i+1 for i in stage_correct_options]}")

# Reset game with error LED feedback
def reset_game():
    global current_stage, confirmed_buttons, input_enabled
    print("? Wrong button. Resetting game...")

    # Flash last LED (index 11) three times
    for _ in range(3):
        leds[11].on()
        sleep(0.2)
        leds[11].off()
        sleep(0.2)

    for led in leds:
        led.off()

    current_stage = 0
    confirmed_buttons = []
    input_enabled = True
    set_next_stage_options()

# Celebration after final stage
def celebration():
    global input_enabled
    print("? Congratulations! All stages cleared. Celebration mode!")
    for _ in range(10):
        for led in leds:
            led.on()
        sleep(0.2)
        for led in leds:
            led.off()
        sleep(0.2)
    reset_game()

# Button handler factory
def make_button_handler(i):
    def handle_press():
        global current_stage, input_enabled

        if not input_enabled:
            return

        if i in stage_correct_options:
            print(f"? Button {i+1} is correct. Proceeding to next stage.")
            leds[i].on()
            confirmed_buttons.append(i)
            current_stage += 1
            input_enabled = False  # Disable further input temporarily

            if current_stage == 12:
                celebration()
            else:
                sleep(0.5)  # Allow time for button release
                set_next_stage_options()
                input_enabled = True
        else:
            input_enabled = False  # Prevent double triggering on reset
            reset_game()
    return handle_press

# Assign handlers
for i, button in enumerate(buttons):
    button.when_pressed = make_button_handler(i)

# Start the game
print("? Game started! Guess the buttons in order.")
set_next_stage_options()
pause()
