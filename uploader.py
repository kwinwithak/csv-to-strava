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
        activities = csv.DictReader(csvfile, skipinitialspace=True)
        activity_count = 0
        upload_count = 0

        for row in activities:
            try:
                activity_count += 1
                activityID = utils.id_from_row(row)

                if not str(row['Calulate Pace']).isdigit():
                    logger("{} - SKIPPED - bad csv encoding".format(activityID))
                    continue

                if activityID not in log:
                    seconds = utils.seconds_for_hms(0, row['Minutes'], row['Seconds'])
                    meters = utils.distance_in_meters(row['Distance'], row['Unit'])
                    starttime = datetime.strptime(str(row['Date']),"%Y-%m-%d")

                    # replace badly encoded apostrophes
                    description = row['Notes'].replace("Ã¢ÂÂ","'").replace("â","'")

                    if row['Feel']:
                        description += "\n\n" + "Feel: " + row['Feel'] + " out of 5"

                    activity_type = 'Run'
                    if 'Cross Train Type' in row and row['Cross Train Type']:
                        activity_type = utils.parse_activity_type(row['Cross Train Type'])

                    try:
                        upload = client.create_activity(
                            name = "Flotrackr - " + row['Name'],
                            start_date_local = starttime,
                            elapsed_time = seconds,
                            distance = meters,
                            description = description,
                            activity_type = activity_type
                        )

                        upload_count += 1
                        logger(activityID + " - UPLOADED")

                    except ValueError as err:
                        if str(err) == "Expecting value: line 1 column 1 (char 0)":
                            # strava doesn't return a response body if user has Activity privacy to set "Only Me"
                            # which causes the stravalib to throw an exception
                            logger(activityID + " - UPLOADED - Activities privacy likely set to Only Me - ValueError: {}".format(err))
                            upload_count += 1
                        else:
                            logger(activityID + " - MAYBE FAILED - ValueError: {}".format(err))

            except Exception as err:
                logger("{0} - SKIPPED - Exception: {1}".format(activityID, err))

        logger("COMPLETE - uploaded " + str(upload_count) + " of " + str(activity_count) + " activities")
        return "COMPLETE - uploaded " + str(upload_count) + " of " + str(activity_count) + " activities"

