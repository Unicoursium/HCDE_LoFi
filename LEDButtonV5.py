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
    print("\nWaiting for any button press...")
    while True:
        status_led.toggle()
        sleep(0.5)
        if any(btn.is_pressed for btn in buttons):
            status_led.off()
            break

def waiting_state():
    global player_count
    print("\nDetecting players,Waiting for 2 seconds...")
    sleep(2)
    pressed = get_pressed_indices()
    player_count = len(pressed) if pressed else 1
    print(f"playernum: {player_count}")

def generate_state():
    global genarr, stepnum, step_size
    genarr.clear()
    if player_count > 5:
        stepnum = 3
        step_size = 5
    else:
        stepnum = 8 - player_count
        step_size = player_count
    print(f"\nGEN STATE: stepnum = {stepnum}, step_size = {step_size}")
    for i in range(stepnum):
        step = sample(range(9), step_size)
        genarr.append(step)
    print("Sequence:")
    for idx, step in enumerate(genarr):
        print(f"  Step {idx+1}: {[s+1 for s in step]}")  # +1 for human-readable

def water_state():
    print("\nWATER STATE: Simulating spray sequence...")
    for idx, step in enumerate(genarr):
        print(f"  Step {idx+1}: Water spraying at buttons {[s+1 for s in step]}")
        sleep(1)
    print("?? Moving to PLAY STATE...")

def play_state():
    global current_step
    current_step = 0

    while current_step < stepnum:
        step_targets = genarr[current_step]
        triggered = [False] * 9  # ??????????

        print(f"\nPLAY STATE: Step {current_step+1}, targets: {[x+1 for x in step_targets]}")
        status_led.on()

        while True:
            pressed = get_pressed_indices()

            # ?????????????
            for idx in pressed:
                if idx not in step_targets:
                    print(f"Wrong button {idx+1} pressed!")
                    flash_leds([idx], duration=1)
                    for led in leds:
                        led.off()
                    status_led.off()
                    return False

            # ???????LED?????
            for i in step_targets:
                if i in pressed and not triggered[i]:
                    leds[i].on()
                    print(f"Water spraying at {i+1}")
                    triggered[i] = True

            # ???????????? ? ????????
            if all(triggered[i] for i in step_targets):
                print(f"Step {current_step+1} complete!")
                sleep(1)
                for i in step_targets:
                    leds[i].off()
                status_led.off()
                current_step += 1
                break

            sleep(0.05)

    return True

def win_state():
    print("WIN")
    for _ in range(10):
        for led in leds:
            led.on()
        print("all water pumps spraying!")
        sleep(0.5)
        for led in leds:
            led.off()
        sleep(0.5)
    print("reset\n")


def main():
    while True:
        code_state()
        waiting_state()
        generate_state()

        while True:  
            water_state()
            success = play_state()
            if success:
                win_state()
                break  
            else:
                print("back to water state")


main()

