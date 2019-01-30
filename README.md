# Flotrackr --> Strava

Uses the [Strava v3 API](http://strava.github.io/api/) to import CSV activities from the defunct Flotrackr running logs into Strava.

Borrows from @barrald's [strava-uploader](https://github.com/barrald/strava-uploader) project and uses @hozn's [stravalib](https://github.com/hozn/stravalib) to interact with the Strava API. Thanks to all.

To start up the app, run the command `python strava_local_client.py get_write_token <client_id> <client_secret>`. Then hit the `/upload` route to begin uploading a CSV file to the authenticated user's Strava. Like this: http://127.0.0.1:8000/upload?path=myfile.csv
