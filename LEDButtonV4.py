from gpiozero import LED, Button
from time import sleep, time
from random import sample
from signal import pause

# === GPIO Mapping ===
button_pins = [26, 14, 15, 18, 23, 24, 25, 8, 7]
led_pins =    [2,   3,  4,  17, 27, 22, 10, 9, 11]
status_led_pin = 19

# === Initialize hardware ===
buttons = [Button(pin, pull_up=True) for pin in button_pins]
leds = [LED(pin) for pin in led_pins]
status_led = LED(status_led_pin)

# === Game variables ===
genarr = []           # 2D list of steps and button numbers
player_count = 1
stepnum = 0
step_size = 0
current_step = 0

# === Utility functions ===

def flash_status_led(duration=0.5, times=1):
    for _ in range(times):
        status_led.on()
        sleep(duration)
        status_led.off()
        sleep(duration)

def flash_leds(indices, duration=2.0):
    for i in indices:
        leds[i].on()
    sleep(duration)
    for i in indices:
        leds[i].off()

def get_pressed_indices():
    return [i for i, btn in enumerate(buttons) if btn.is_pressed]

def code_state():
    print("\n? Entering CODE STATE: Waiting for any button press...")
    while True:
        status_led.toggle()
        sleep(0.5)
        if any(btn.is_pressed for btn in buttons):
            status_led.off()
            break

def waiting_state():
    global player_count
    print("\n? Entering WAITING STATE: Waiting 2 seconds...")
    sleep(2)
    pressed = get_pressed_indices()
    player_count = len(pressed) if pressed else 1
    print(f"? Detected players: {player_count}")

def generate_state():
    global genarr, stepnum, step_size
    genarr.clear()
    if player_count > 5:
        stepnum = 3
        step_size = 5
    else:
        stepnum = 8 - player_count
        step_size = player_count
    print(f"\n? GENERATE STATE: stepnum = {stepnum}, step_size = {step_size}")
    for i in range(stepnum):
        step = sample(range(9), step_size)
        genarr.append(step)
    print("Generated sequence:")
    for idx, step in enumerate(genarr):
        print(f"  Step {idx+1}: {[s+1 for s in step]}")  # +1 for human-readable

def water_state():
    print("\n? WATER STATE: Simulating spray sequence...")
    for idx, step in enumerate(genarr):
        print(f"  Step {idx+1}: Water spraying at buttons {[s+1 for s in step]}")
        sleep(1)
    print("?? Moving to PLAY STATE...")

def play_state():
    global current_step
    current_step = 0
    while current_step < stepnum:
        print(f"\n? PLAY STATE: Step {current_step+1}")
        status_led.on()
        sleep(2)  # signal step start
        status_led.off()

        pressed = get_pressed_indices()
        pressed.sort()
        expected = sorted(genarr[current_step])

        print(f"  Buttons pressed: {[p+1 for p in pressed]}")
        print(f"  Expected: {[e+1 for e in expected]}")

        if pressed == expected:
            print("? Correct! Spraying and flashing LEDs...")
            flash_leds(pressed, duration=2)
            print(f"? Water spraying at {[p+1 for p in pressed]}")
            current_step += 1
        else:
            print("? Incorrect! Returning to WATER STATE.")
            if pressed:
                flash_leds(pressed, duration=1)
            for led in leds:
                led.off()
            return False  # Failed round, return to water_state
    return True  # All steps passed

def win_state():
    print("\n? WIN STATE: All steps completed! Celebration begins...")
    for _ in range(10):
        for led in leds:
            led.on()
        print("? ALL water pumps spraying!")
        sleep(0.5)
        for led in leds:
            led.off()
        sleep(0.5)
    print("? Resetting game...\n")

# === Main game loop ===

def main():
    while True:
        code_state()
        waiting_state()
        generate_state()
        water_state()
        success = play_state()
        if success:
            win_state()

main()
