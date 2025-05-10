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
confirmed_buttons = []           # e.g. [7, 8, 2]
button_state = [False] * 12      # track previous button state
fixed_answers = [None] * 12      # record correct button for each stage
stage_correct_options = []       # only used during "new" stage

# Determine number of correct buttons per stage
def correct_option_count(stage):
    if stage <= 3: return 5
    elif stage <= 6: return 4
    elif stage <= 8: return 3
    elif stage <=10: return 2
    else: return 1

# Generate new random correct options for current stage
def generate_stage_options():
    remaining = [i for i in range(12) if i not in confirmed_buttons]
    count = correct_option_count(current_stage)
    return sample(remaining, min(count, len(remaining)))

# Set correct options (either fixed or random)
def set_stage_correct_options():
    global stage_correct_options
    if fixed_answers[current_stage] is not None:
        stage_correct_options = [fixed_answers[current_stage]]
    else:
        stage_correct_options = generate_stage_options()
    print(f"[lv {current_stage+1}] Correct: {[i+1 for i in stage_correct_options]}")

# Flash the last LED (index 11) 3 times for error feedback
def flash_error_led():
    for _ in range(3):
        leds[11].on()
        sleep(0.2)
        leds[11].off()
        sleep(0.2)

# Reset game, keep fixed_answers
def reset_game():
    global current_stage, confirmed_buttons
    print("wrong button")
    flash_error_led()
    for led in leds:
        led.off()
    current_stage = 0
    confirmed_buttons.clear()
    set_stage_correct_options()
    
def reset_cel():
    global current_stage, confirmed_buttons
    print("greatreset")
    flash_error_led()
    for led in leds:
        led.off()
    current_stage = 0
    confirmed_buttons.clear()
    #set_stage_correct_options()

# Celebrate on full success
def celebration():
    print("niubi")
    for _ in range(10):
        for led in leds:
            led.on()
        sleep(0.2)
        for led in leds:
            led.off()
        sleep(0.2)
    reset_cel()

# Main loop
def main():
    global current_stage

    print("start")
    set_stage_correct_options()

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

                    # Lock in fixed answer if not already
                    if fixed_answers[current_stage] is None:
                        fixed_answers[current_stage] = i

                    current_stage += 1
                    if current_stage == 12:
                        celebration()
                        return
                    else:
                        sleep(0.3)
                        set_stage_correct_options()
                else:
                    reset_game()

            elif not buttons[i].is_pressed:
                button_state[i] = False

        sleep(0.01)

main()
