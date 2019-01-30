#!/usr/bin/env python

"""
Strava Development Sandbox.

Get your *Client ID* and *Client Secret* from https://www.strava.com/settings/api

Usage:
  strava_local_client.py get_write_token <client_id> <client_secret> [options]
  strava_local_client.py find_settings
  strava_local_client.py run

Options:
  -h --help      Show this screen.
  --port=<port>  Local port for OAuth client [default: 8000].
"""

from flask import Flask, request, redirect
import stravalib
import athlete
import uploader

app = Flask(__name__)

API_CLIENT = stravalib.Client()
CLIENT_ID = None
CLIENT_SECRET = None
ACCESS_TOKEN = None


@app.route("/")
def index():
    global ACCESS_TOKEN

    if ACCESS_TOKEN:
        athlete_info = athlete.get_name(ACCESS_TOKEN)
        return athlete_info + " is authenticated. Their current token is " + ACCESS_TOKEN
    else:
        return "Nobody is authenticated."

@app.route("/auth")
def auth():
    code = request.args.get('code')
    token_dictionary = API_CLIENT.exchange_code_for_token(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        code=code
        )
    global ACCESS_TOKEN
    ACCESS_TOKEN = token_dictionary['access_token']
    return redirect("/")

@app.route("/upload")
def uploadCSV():
    if ACCESS_TOKEN:
        try:
            path = request.args.get('path')

            if path:
                result = uploader.upload_csv(ACCESS_TOKEN, str(path))
                return result
            else:
                return "Ope! Make sure path=[relative-path-to-your-file] is in the query string! Like this --> http://127.0.0.1:8000/upload?path=myfile.csv"
        except Exception as err:
            return "Error: {}".format(err)
    else:
        return "Nobody is authenticated."


if __name__ == '__main__':
    import docopt
    import subprocess
    import sys

    args = docopt.docopt(__doc__)

    if args['get_write_token']:
        CLIENT_ID, CLIENT_SECRET = args['<client_id>'], args['<client_secret>']
        auth_url = API_CLIENT.authorization_url(
            client_id=args['<client_id>'],
            redirect_uri='http://127.0.0.1:{port}/auth'.format(port=args['--port']),
            scope=['profile:read_all', 'activity:read_all', 'activity:write'],
            state='from_cli'
            )
        if sys.platform == 'darwin':
            print('On OS X - launching {0} at default browser'.format(auth_url))
            subprocess.call(['open', auth_url])
        else:
            print('Go to {0} to authorize access: '.format(auth_url))
        app.run(port=int(args['--port']))
    elif args['find_settings']:
        subprocess.call(['open', 'https://www.strava.com/settings/api'])
    elif args['run']:
        app.run(port=int(args['--port']))
