def distance_in_meters(value, unit):
    if not value or not unit:
        return 0
    else:
        uom = unit.lower()
        if uom == "meters":
            return float(value)
        elif uom == "kilometers" or uom == "km":
            return float(value) * 1000
        elif uom == "miles" or uom == "mi":
            return float(value) * 1609.344
        else:
            return 0

def seconds_for_hms(hours, minutes, seconds):
    total_seconds = 0
    total_seconds += int(hours) * 3600 if hours else 0
    total_seconds += int(minutes) * 60 if minutes else 0
    total_seconds += int(seconds) if seconds else 0
    return total_seconds

def parse_activity_type(value):
    if value:
        activity = value.lower().strip()
        if activity == "run":
            return "Run"
        elif activity == "swim":
            return "Swim"
        elif activity == "bike":
            return "Ride"
        else:
            return "Workout"
    else:
        return "Workout"

def duration_calc(duration):
    # Function to convert the HH:MM:SS in the Runkeeper CSV to seconds

    # Splits the duration on the :, so we wind up with a 3-part array
    split_duration = str(duration).split(":")
    # If the array only has 2 elements, we know the activity was less than an hour
    if len(split_duration) == 2:
        hours = 0
        minutes = int(split_duration[0])
        seconds = int(split_duration[1])
    else:
        hours = int(split_duration[0])
        minutes = int(split_duration[1])
        seconds = int(split_duration[2])

    total_seconds = seconds + (minutes*60) + (hours*60*60)
    return total_seconds
