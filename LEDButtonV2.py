from gpiozero import LED, Button
from time import sleep
from random import sample

# GPIO mappings
led_pins =    [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 13, 19]
button_pins = [26,14,15,18,23,24,25,8,7,16,20,21]

# Initialize LEDs and buttons
leds = [LED(pin) for pin in led_pins]
buttons = [Button(pin, pull_up=True) for pin in button_pins]

# Game state
current_stage = 0
confirmed_buttons = []
stage_correct_options = []
button_state = [False] * 12  # track previous button state

# Determine number of correct buttons for each stage
def correct_option_count(stage):
    if stage <= 3: return 5
    elif stage <= 6: return 4
    elif stage <= 8: return 3
    elif stage <=10: return 2
    else: return 1

# Generate correct options for the current stage
def set_next_stage_options():
    global stage_correct_options
    remaining = [i for i in range(12) if i not in confirmed_buttons]
    count = correct_option_count(current_stage)
    count = min(count, len(remaining))
    stage_correct_options = sample(remaining, count)
    print(f"[Stage {current_stage+1}] Correct options: {[i+1 for i in stage_correct_options]}")

# Flash the last LED 3 times for wrong input
def flash_error_led():
    for _ in range(3):
        leds[11].on()
        sleep(0.2)
        leds[11].off()
        sleep(0.2)

# Reset game state
def reset_game():
    global current_stage, confirmed_buttons
    print("? Wrong button. Resetting game...")
    flash_error_led()
    for led in leds:
        led.off()
    current_stage = 0
    confirmed_buttons.clear()
    set_next_stage_options()

# Celebrate on full success
def celebration():
    print("? All 12 stages cleared! Celebration mode!")
    for _ in range(10):
        for led in leds:
            led.on()
        sleep(0.2)
        for led in leds:
            led.off()
        sleep(0.2)
    reset_game()

# Main loop
def main():
    global current_stage
    print("? Game started. Press buttons to guess the sequence.")
    set_next_stage_options()

    while True:
        for i in range(12):
            if buttons[i].is_pressed and not button_state[i]:  # just pressed
                button_state[i] = True

                if i in confirmed_buttons:
                    print(f"?? Button {i+1} already pressed.")
                    continue

                if i in stage_correct_options:
                    print(f"? Button {i+1} correct! Proceeding.")
                    leds[i].on()
                    confirmed_buttons.append(i)
                    current_stage += 1

                    if current_stage == 12:
                        celebration()
                        return
                    else:
                        sleep(0.3)  # allow user to release button
                        set_next_stage_options()
                else:
                    reset_game()

            elif not buttons[i].is_pressed:
                button_state[i] = False

        sleep(0.01)  # loop delay, reduces CPU usage

# Run the game
main()
