import keyboard
import time
import sys

def main():
    print("===== Space Button Auto-Clicker for MuMu Player (1600x900, 240 DPI) =====")
    print("This script will continuously press the space bar.")
    print("\nControls:")
    print("  'q' - Quit the program")
    print("  '+' - Increase click speed")
    print("  '-' - Decrease click speed")
    print("\nStep 1: Set up your MuMu Player window")
    print("Step 2: Press ENTER when ready to start clicking")
    
    # Default delay between clicks (in seconds)
    delay = 0.1
    
    input("Press ENTER to start...")
    
    # Give user time to switch to the MuMu Player window
    print("\nStarting in 5 seconds...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    print(f"\nAuto-clicking space started with {delay:.2f}s delay!")
    print("Press 'q' to stop, '+' to speed up, '-' to slow down")
    
    try:
        # Continue pressing space until 'q' is pressed
        while True:
            if keyboard.is_pressed('q'):  # Check if 'q' is pressed
                print("\nStopping auto-clicker...")
                break
            
            elif keyboard.is_pressed('+') or keyboard.is_pressed('='): # Speed up
                delay = max(0.01, delay - 0.01)  # Minimum delay of 0.01s
                print(f"\nSpeed increased! New delay: {delay:.2f}s")
                time.sleep(0.2)  # Prevent multiple adjustments
                
            elif keyboard.is_pressed('-') or keyboard.is_pressed('_'): # Slow down
                delay = min(1.0, delay + 0.01)  # Maximum delay of 1.0s
                print(f"\nSpeed decreased! New delay: {delay:.2f}s")
                time.sleep(0.2)  # Prevent multiple adjustments
            
            # Press space
            keyboard.press_and_release('space')
            
            # Delay between clicks
            time.sleep(delay)
            
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    
    print("Auto-clicker stopped.")

if __name__ == "__main__":
    main()