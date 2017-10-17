################################################################################
# set_clock.py
# Elijah Caluya 10/10/17
#
# Final Version of Date and Time Picker.
# All features are present
#
# Follows conventions and is based on code from sample_menu.py by Anthony Hornof
# Also uses code from sound.py by Anthony Hornof
#
################################################################################
__author__ = 'Caluya'

# Package imports
import readchar
import time         # for time.sleep()

# Local imports
import sound        # sound.py accompanies this file
import wave         # importing to edit wave functions

# Added functions so that the concatenated files will be able to play
# Copied from stackoverflow post
# https://stackoverflow.com/questions/46538867/attributeerror-wave-write-instance-has-no-attribute-exit
def _trivial__enter__(self):
    return self
def _self_close__exit__(self, exc_type, exc_value, traceback):
    self.close()

wave.Wave_read.__exit__ = wave.Wave_write.__exit__ = _self_close__exit__
wave.Wave_read.__enter__ = wave.Wave_write.__enter__ = _trivial__enter__


################################################################################
# main()
################################################################################
def main():
    create_sound_filenames()
    verify_sound_filenames()
    create_menu_globals()
    run_menu()

################################################################################
# Create the sound objects for the auditory menus and display.
################################################################################
def create_sound_filenames():

    # Declare global variables.
    global INTRO_WAV, YOU_SELECTED_WAV, NUMBERS_WAV, AM_WAV, PM_WAV,PRESS_AGAIN_TO_QUIT_WAV,\
        EXITING_PROGRAM_WAV, EXITING_PROGRAM_WAV_DURATION, TMP_FILE_WAV,nav_path,num_path,day_path

    print("Creating sound filenames...")
    # Create  sounds.
    nav_path = "wav_files_provided/miscellaneous_f/"
    num_path = "wav_files_provided/numbers_f/"
    day_path = "wav_files_provided/days_of_week_f/"
    INTRO_WAV = nav_path + "Intro_f.wav"
    YOU_SELECTED_WAV = nav_path + "you_selected_f.wav"
    NUMBERS_WAV = [num_path + "28_f.wav", num_path + "29_f.wav",
           num_path + "30_f.wav", num_path + "31_f.wav"]
    AM_WAV = nav_path + "AM_f.wav"
    PM_WAV = nav_path + "PM_f.wav"
    PRESS_AGAIN_TO_QUIT_WAV = nav_path + "Press_again_to_quit_f.wav"
    EXITING_PROGRAM_WAV = nav_path + "Exiting_program_f.wav"
    EXITING_PROGRAM_WAV_DURATION = 1.09 # in s. 1.09 is accurate but 0.45 saves time.

    TMP_FILE_WAV = "tmp_file_p782s8u.wav" # Random filename  for output

################################################################################
# Verify all files can be loaded and played.
# Play all sound files to make sure the paths and filenames are correct and valid.
# The very last sound tested/played should be the sound that plays at startup.
################################################################################
def verify_sound_filenames():
    print("Verifying sound filenames...")
    sound.combine_wav_files(TMP_FILE_WAV,INTRO_WAV,nav_path + "Set_day_of_week_f.wav")
    sound.Play(TMP_FILE_WAV)

################################################################################
# Create some global constants and variables for the menu.
################################################################################
def create_menu_globals():

    # Declare global variables as such.
    global CONFIRM,FORWARD_KEY,BACKWARD_KEY,QUIT_KEY,HELP,MINIMAL_HELP_STRING,\
        CURRENT_TIME,PHASE,SELECTION

    print("Creating menu globals...")
    # Constants
    # Keystrokes for the keyboard interaction.
    CONFIRM = '\x20' # space bar
    FORWARD_KEY = 'k'
    BACKWARD_KEY = 'l'
    QUIT_KEY = 'j'
    HELP = ';'
    # A bare minimum of text to display to guide the user.
    MINIMAL_HELP_STRING = "Press '" + QUIT_KEY + "' to quit."

    # Global variables
    CURRENT_TIME = 0    # The current time that is set. (Just an integer for now.)
    PHASE = 0
    SELECTION = ""

################################################################################
# Run the menu in an endless loop until the user exits.
################################################################################
def run_menu():

    global CURRENT_TIME,LIMIT,days, sound_str,PHASE

    # Provide a minimal indication that the program has started.
    print("Starting program...\n")
    print(MINIMAL_HELP_STRING)

    # Get the first keystroke.
    c = readchar.readchar()

    # Special wav files for instructions
    instr_j = "my_sounds/j_to_quit.wav"
    instr_k = "my_sounds/k_for_up.wav"
    instr_l = "my_sounds/l_for_down.wav"
    semi_help = "my_sounds/semi_for_help.wav"
    space_to = "my_sounds/space_to.wav"
    restart = "my_sounds/restart.wav"
    space_conf = "my_sounds/space_to_confirm.wav"

    LIMIT = 7
    days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
    sound_str = "sound_string.wav"
    index = ""

    # Endless loop responding to the user's last keystroke.
    # The loop breaks when the user hits the QUIT_MENU_KEY.
    while True:

        ##### Respond to the user's input.
        ##### User goes forwards scrolling
        if c == FORWARD_KEY:

            # Advance the time, looping back around to the start.
            CURRENT_TIME += 1
            if CURRENT_TIME == LIMIT:
                CURRENT_TIME = 0

            # Check if in Set Day phase
            if PHASE == 0:
                sound.Play(day_path + days[CURRENT_TIME] + "_f.wav")

            # Check phase to see if Hour Phase
            if PHASE == 1:
                get_hour(CURRENT_TIME)

            #Check if user is in Minute Phase
            if PHASE == 2:
                get_minutes(CURRENT_TIME)


        ##### User Goes backwards scrolling
        if c == BACKWARD_KEY:
            # Decrease the time, looping back around to the start.
            CURRENT_TIME -= 1
            if CURRENT_TIME < 0:
                CURRENT_TIME = LIMIT-1

            # Check if in Set Day phase
            if PHASE == 0:
                sound.Play(day_path + days[CURRENT_TIME] + "_f.wav")

            # Check phase to see if Hour phase
            if PHASE == 1:
                get_hour(CURRENT_TIME)

            # Check if User is in Minute Phase
            if PHASE == 2:
                get_minutes(CURRENT_TIME)

        ##### When user confirms selection
        if c == CONFIRM:
            # Check if user is at the end of the program
            if next_state() == 1:
                time.sleep(4)
                # GIve user choice to restart or quit program
                sound.combine_wav_files(sound_str,instr_j,space_to,restart)
                sound.Play(sound_str)

                # Get user's next key input
                c = readchar.readchar()
                # If the user decides to quit, the program will end
                if (c == QUIT_KEY):
                    sound.Play(EXITING_PROGRAM_WAV)
                    time.sleep(EXITING_PROGRAM_WAV_DURATION)
                    break
                # If the user decides to restart, the program will restart all its values
                # and start the user at setting the day of the week
                elif c == CONFIRM:
                    sound.Play(nav_path + "Set_day_of_week_f.wav")
                    CURRENT_TIME = 0
                    LIMIT = 7
                    PHASE = 0


        #### If the User presses for help
        if c == HELP:
            # Notify the user to press the button again
            sound.Play(nav_path + "Press_again_for_help_f.wav")
            # Get user's next keystroke
            c = readchar.readchar()

            # Give the user instructions of the key functions and current phase
            # of the program the user is in
            if c == HELP:
                if PHASE == 0:
                    help_day = nav_path + "Set_day_of_week_f.wav"
                    sound.combine_wav_files(sound_str,space_conf,instr_j,instr_k,instr_l,semi_help,help_day)
                    sound.Play(sound_str)
                elif PHASE == 1:
                    help_hour = nav_path + "Set_hour_f.wav"
                    sound.combine_wav_files(sound_str,space_conf,instr_j,instr_k,instr_l,semi_help,help_hour)
                    sound.Play(sound_str)
                elif PHASE == 2:
                    help_day = nav_path + "Set_minutes_f.wav"
                    sound.combine_wav_files(sound_str,space_conf,instr_j,instr_k,instr_l,semi_help,help_day)
                    sound.Play(sound_str)

        #### User quits.
        if c == QUIT_KEY:

            # Notify the user that another QUIT_MENU_KEY will quit the program.
            sound.Play(PRESS_AGAIN_TO_QUIT_WAV)

            # Get the user's next keystroke.
            c = readchar.readchar()

            # If the user pressed QUIT_MENU_KEY, quit the program.
            if c == QUIT_KEY:
                sound.Play(EXITING_PROGRAM_WAV)
                # A delay is needed so the sound gets played before quitting.
                time.sleep(EXITING_PROGRAM_WAV_DURATION)
                sound.cleanup()
                # Quit the program
                break


        ##### The user presses a key that will have no effect.
        else:
            # Get the user's next keystroke.
            c = readchar.readchar()

###########
# Function that shifts the user into the next phase while adjusting limits and numbers
###########
def next_state():
    global PHASE, CURRENT_TIME, LIMIT,days, sound_str, YOU_SELECTED_WAV, picked_day,picked_hour,picked_minutes

    # Transition to Hour phase
    if PHASE == 0:
        # Get and combine selected day to announce to user
        day = day_path + days[CURRENT_TIME] + "_f.wav"
        sound.combine_wav_files(sound_str, YOU_SELECTED_WAV,day,nav_path+"Set_hour_f.wav")
        picked_day = day
        PHASE = 1
        CURRENT_TIME = 0
        LIMIT = 24
        sound.Play(sound_str)
    # Transition to Minute phase
    elif PHASE == 1:
        # Get and combine selected hour and announce to user
        selected_hour = get_hour(CURRENT_TIME)
        sound.combine_wav_files(sound_str,YOU_SELECTED_WAV,selected_hour,nav_path + "Set_minutes_f.wav")
        picked_hour = CURRENT_TIME
        PHASE = 2
        CURRENT_TIME = 0
        LIMIT = 60
        sound.Play(sound_str)
    # Transition to End phase
    elif PHASE == 2:
        selected_minutes = get_minutes(CURRENT_TIME)
        picked_minutes = selected_minutes
        get_final_time(picked_day,picked_hour,picked_minutes)
        PHASE = 3
        return 1
    return 0

##########
# Function to play the hour when given the current time
##########
def get_hour(time):
    hour = "hour.wav"
    # When time is 12 AM
    if time == 0:
        index = num_path + "12_f.wav"
        sound.combine_wav_files(hour, index, AM_WAV)
        sound.Play(hour)
    # When time is 12 PM
    elif time == 12:
        index = num_path + "12_f.wav"
        sound.combine_wav_files(hour, index, PM_WAV)
        sound.Play(hour)
    # When time is after 9 AM and before 12 PM
    elif time > 9 and time < 12:
        index = num_path + str(time) + "_f.wav"
        sound.combine_wav_files(hour, index, AM_WAV)
        sound.Play(hour)
    # When time is after 12 AM and before 10 AM
    elif time < 10 and time > 0:
        index = num_path + "0" + str(time) + "_f.wav"
        sound.combine_wav_files(hour, index, AM_WAV)
        sound.Play(hour)
    # When time is after 12 PM and before 10 PM
    elif time > 12 and time < 22:
        index = num_path + "0" + str(time - 12) + "_f.wav"
        sound.combine_wav_files(hour, index, PM_WAV)
        sound.Play(hour)
    # When time is after 9 PM
    elif time > 21:
        index = num_path + str(time - 12) + "_f.wav"
        sound.combine_wav_files(hour, index, PM_WAV)
        sound.Play(hour)
    return hour

##########
# Function to announce and return the minutes
##########
def get_minutes(time):
    if (time < 10):
        sound.Play(num_path + "0" + str(time) + "_f.wav")
    else:
        sound.Play(num_path + str(time) + "_f.wav")
    return time

###########
# Function to read the final date and time the user selected
###########
def get_final_time(day,hour_num,minute_num):
    final_selection = "final.wav"
    AMPM = 0
    hour_str = ""
    minute_str = ""
    zero_str = nav_path + "o_clock_f.wav"
    oh_str = num_path + "oh_f.wav"
    # Generate the correct string based on the hour of the day
    # Also assigns AMPM = 0 if in the morning or else AMPM = 1 for the afternoon and night
    if (hour_num == 0):
        hour_str = num_path + "12_f.wav"
    elif (hour_num == 12):
        hour_str = num_path + "12_f.wav"
        AMPM = 1
    elif (hour_num  > 9 and hour_num < 12):
        hour_str = num_path + str(hour_num) + "_f.wav"
    elif (hour_num < 10 and hour_num >0):
        hour_str = num_path + "0" + str(hour_num) + "_f.wav"
    elif (hour_num >12 and hour_num < 22):
        hour_str = num_path + "0" + str(hour_num - 12) + "_f.wav"
        AMPM = 1
    elif (hour_num > 21):
        hour_str = num_path + str(hour_num-12) + "_f.wav"
        AMPM = 1

    # If the time is in the AM
    if (AMPM == 0):
        # If the minutes are 0, we need to put "o' clock" at the end
        if (minute_num == 0):
            sound.combine_wav_files(final_selection,YOU_SELECTED_WAV,day,hour_str,zero_str,AM_WAV)
        # If the number is single digit then, we must put the "oh" in front of the minutes when announcing the selection
        elif (minute_num < 10):
            minute_str = num_path + "0" + str(minute_num) + "_f.wav"
            sound.combine_wav_files(final_selection, YOU_SELECTED_WAV, day, hour_str, oh_str,minute_str, AM_WAV)
        # Any other numbers that do not change the way it is said
        else:
            minute_str = num_path + str(minute_num) + "_f.wav"
            sound.combine_wav_files(final_selection, YOU_SELECTED_WAV, day, hour_str, minute_str,AM_WAV)
    # If the time is in the PM
    elif (AMPM == 1):
        # If the minutes are 0, we need to put "o' clock" at the end
        if (minute_num == 0):
            sound.combine_wav_files(final_selection, YOU_SELECTED_WAV, day, hour_str, zero_str, PM_WAV)
        # If the number is single digit then, we must put the "oh" in front of the minutes when announcing the selection
        elif (minute_num < 10):
            minute_str = num_path + "0" + str(minute_num) + "_f.wav"
            sound.combine_wav_files(final_selection, YOU_SELECTED_WAV, day, hour_str, oh_str, minute_str, PM_WAV)
        # Any other numbers that do not change the way it is said
        else:
            minute_str = num_path + str(minute_num) + "_f.wav"
            sound.combine_wav_files(final_selection, YOU_SELECTED_WAV, day, hour_str, minute_str, PM_WAV)

    # Play the final result of day, hour, minutes, and time of day
    sound.Play(final_selection)


################################################################################
main()
################################################################################
