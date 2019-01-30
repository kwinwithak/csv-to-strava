import os
from stravalib import Client, exc, model
from stravalib.util import limiter
from requests.exceptions import ConnectionError, HTTPError
import requests
import csv
import time
from datetime import datetime
import utils

def upload_csv(access_token, filepath):

    # Creating a log file and a logging function
    log = open("log.txt","a+")
    now = str(datetime.now())
    def logger (message):
        log.write(now + " | " + message + "\n")
        print (message)

    logger("Connecting to Strava")
    sleeping_rlr = limiter.SleepingRateLimitRule(priority='medium')
    client = Client(access_token=access_token, rate_limiter=sleeping_rlr)
    athlete = client.get_athlete()

    logger("Beginning csv upload for " + athlete.firstname + " " + athlete.lastname)

    with open(filepath, encoding = "ISO-8859-1") as csvfile:
        activities = csv.DictReader(csvfile)
        activity_counter = 0
        for row in activities:
            try:
                activityID = "ID_" + row['Date'] + '_' + row['Name']

                if not str(row['Calulate Pace']).isdigit():
                    # TODO: help the user out
                    logger("Skipping {} due to bad csv encoding".format(activityID))
                    continue

                if activityID not in log:
                    logger("Manually uploading " + activityID)

                    seconds = utils.seconds_for_hms(0, row['Minutes'], row['Seconds'])
                    meters = utils.distance_in_meters(row['Distance'], row['Unit'])
                    starttime = datetime.strptime(str(row['Date']),"%m/%d/%y")
                    # TODO: allow start time to be configured as setting

                    description = row['Notes']
                    if row['Feel']:
                        description += "\n\n" + "Feel: " + row['Feel'] + " out of 5"

                    activity_type = 'Run'
                    if 'Cross Train Type' in row and row['Cross Train Type']:
                        activity_type = utils.parse_activity_type(row['Cross Train Type'])

                    try:
                        activity_counter += 1

                        upload = client.create_activity(
                            name = row['Name'] + " (Flotrackr entry)",
                            start_date_local = starttime,
                            elapsed_time = seconds,
                            distance = meters,
                            description = description,
                            activity_type = activity_type
                        )

                        logger("Manually created " + activityID)

                    except ValueError as err:
                        # strava doesn't return a response body if user has Activity privacy to set "Only Me"
                        # which causes the stravalib to throw an exception
                        logger("ValueError: {}".format(err))

            except ValueError as err:
                logger("Skipping {0} due to ValueError: {1}".format(activityID, err))

        logger("Complete! Uploaded " + str(activity_counter) + " activities.")
        return "Complete! Uploaded " + str(activity_counter) + " activities."


