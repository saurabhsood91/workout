#!/usr/bin/env python

import os
import platform
import re
import time
from datetime import datetime
from random import choice

from routines import (
    ABS,
    BASIC,
    BEEFCAKE,
    CORE,
    GENERAL,
    GLUTES,
    PHYSIO_KNEES,
    PHYSIO_BACK_AND_NECK,
    PHYSIO_BALANCE,
    PHYSIO_CUSTOM,
    PHYSIO_COMBINED,
    STRETCHES,
)

from constants import (WINDOWS, MAC_OS)

SET_DURATION = 30  # duration of each set in seconds

def say_mac_os(text):
    os.system("say -v Fiona {}".format(text))

def say_linux(text):
    # Linux distros come with `spd-say`.
    # Preinstalled on ubuntu, but you may need it to install
    # it on Fedora and openSUSE
    os.system("spd-say {}".format(text))


def say(text):
    sys_platform = platform.system()
    if sys_platform == MAC_OS:
        say_mac_os(text)
    elif sys_platform == WINDOWS:
        # TODO
        pass
    else:
        # LINUX
        say_linux(text)


def begin_workout(routine_name, total_duration=None):
    """
    Either total workout duration is a function of the selected routine
    with a default set duration ("standard" workout), or set duration
    is derived from the specified total duration ("timed" workout).

    TODO: add notion of "reps."
    """
    routine = globals().get(routine_name)
    if total_duration:
        set_duration = float(total_duration) / len(routine)
    else:
        set_duration = SET_DURATION
        total_duration = len(routine) * set_duration

    say('Beginning {} minute {} workout.'
        .format(total_duration/60, routine_name))

    return (routine, set_duration, total_duration)


def end_workout():
    say('Workout complete! Congratulations!')


def do_exercise(exercise, duration, coaching=False):
    say('Next: {exercise}.'.format(exercise=exercise.name))
    if coaching and exercise.__doc__:
        description = re.sub('[^a-zA-Z0-9 \.]', ' ', exercise.__doc__)
        say(description)
    time.sleep(2)
    say('3... 2... 1... GO! {exercise}'.format(exercise=exercise.name))
    time.sleep(duration/2.0)
    call_out = choice((False, False, True))
    if call_out:
        whom = choice(('Sid', 'Ariana'))
        exercise_singular = exercise.name.rstrip('Ss')
        taunt1 = ('Come on {whom}! You call that a {exercise_singular}?'
                  .format(whom=whom, exercise_singular=exercise_singular))
        taunt2 = ('My grandma does better {exercise} than you two!'
                  .format(exercise=exercise.name))
        taunt = choice((taunt1, taunt2))
        say(taunt)
    interval = max(0, duration/2.0 - 3)
    time.sleep(interval)
    say('3... 2... 1...')
    time.sleep(1)
    return datetime.now()


def main():
    start_time = datetime.now()

    # add itinerary
    routine_name = "BEEFCAKE"
    coaching = False

    routine, set_duration, total_duration = begin_workout(routine_name)

    workout = iter(routine)
    workout_time = 0

    while True:
        try:
            exercise = next(workout)
            duration = exercise.duration * set_duration
            current_time = do_exercise(exercise, duration, coaching)
        except StopIteration:
            break

        workout_time = (current_time - start_time).total_seconds()

    print("workout time = {min}:{sec}".format(min=workout_time/60,
                                              sec=workout_time % 60))
    end_workout()


if __name__ == '__main__':
    main()
