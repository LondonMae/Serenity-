# Serenity
Serenity is the robot alarm clock that offers recommendations and statistics about when to go to sleep based on your Fitbit data, and wakes you up with new music catered to the user as well as a simulated sunrise.

- [Installation and Dependencies](#installation-and-dependencies)
- [Running the Webserver](#running-the-webserver)
- [APIs](#apis)

## Installation and Dependencies
- Python Version: Python 3.8
- NodeJS Version: v18.12.0. 

You must install all NodeJS dependencies using `npm install <package_name>`. The list of dependencies is in the packagaes.json file. 

All python dependencies can be installed using `python -m pip install -r requirements.txt`. 

For token access using fitbit and spotify login authentication, you will need to register and access your app credentials with the Spotify and Fitbit API. Set the callbacks to http://localhost:8888/callback and http://localhost:8888/fitbitcallback respectively. Paste your client ID and Secret into the variables in the app.js script. You will also need to entire your desired playback device id in the music.py script. Lastly, for light functionality, please find the IP address of your yeelight lightbulb and paste it in the IP varibale in the lights.py file. 

## Running the Webserver
1. run the nodeJS script app.js using `node app.js`
2. You can access the website at http://localhost:8888

## APIs
Find the links to the APIs and their documentation below:  

- [Spotify](https://developer.spotify.com/documentation/web-api/)
- [Yeelight](https://yeelight.readthedocs.io/en/latest/)
- [Fitbit](https://dev.fitbit.com/build/reference/web-api/)

