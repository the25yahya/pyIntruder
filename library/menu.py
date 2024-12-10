import keyboard

def menu():
    options = ["fuzzing", "xss", "open redirect", "sqli", "command injection", "path traversal", "ssti"]
    current_index = 0

    while True:
        # Clear the screen
        print("\033[H\033[J", end="")
        print("\033[1;31m[*] Use ↑ and ↓ to navigate. Press Enter to select.\033[0m\n")

        # Display the menu
        for i, option in enumerate(options):
            if i == current_index:
                print(f"\033[1;31m> [*] {option}\033[0m")
            else:
                print(f"\033[1;31m  [*] {option}\033[0m")

        # Wait for a key press
        key = keyboard.read_event()

        # Process key input
        if key.event_type == "down":  # Detect a keypress event
            if key.name == "down" and current_index < len(options) - 1:
                current_index += 1
            elif key.name == "up" and current_index > 0:
                current_index -= 1
            elif key.name == "enter":
                selected_option = options[current_index]
                return selected_option
