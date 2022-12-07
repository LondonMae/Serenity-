/**
 * This is  a basic node.js script that performs
 * the Authorization Code oAuth2 flow to authenticate against
 * the Spotify Accounts.
 *
 * For more information, read
 * https://developer.spotify.com/web-api/authorization-guide/#authorization_code_flow
 */

var open = require("open") // to open in webbrowser
var fs = require('fs');
var express = require('express'); // Express web server framework
var request = require('request'); // "Request" library
var cors = require('cors');
var querystring = require('querystring');
var cookieParser = require('cookie-parser');
const PythonShell = require('python-shell').PythonShell; // run python scripts
var FitbitStrategy = require('passport-fitbit-oauth2').FitbitOAuth2Strategy;
var passport = require('passport');
var session = require('express-session');
var bodyParser = require('body-parser');
var https = require("https")

// hardcoded from spotify app dashboard (dev settings)
var client_id = ''; // Your client id
var client_secret = ''; // Your secret
var redirect_uri = 'http://localhost:8888/callback'; // Your redirect uri

/**
 * Generates a random string containing numbers and letters
 * @param  {number} length The length of the string
 * @return {string} The generated string
 */
var generateRandomString = function(length) {
  var text = '';
  var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

  for (var i = 0; i < length; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
};

var stateKey = 'spotify_auth_state';

var app = express();
var folder;

app.use(express.static(__dirname + '/public'),express.static("public"))
   .use(cors())
   .use(cookieParser());
   app.use(bodyParser());
   app.use(session({ secret: 'keyboard cat' }));

   app.use(passport.initialize());
   app.use(passport.session({
     resave: false,
     saveUninitialized: true
   }));

   const CLIENT_ID = "";
   const CLIENT_SECRET = "";

   app.use(passport.initialize());

   var fitbitStrategy = new FitbitStrategy({
     clientID: CLIENT_ID,
     clientSecret: CLIENT_SECRET,
     scope: ['activity','heartrate','location','profile','sleep'],
     callbackURL: "http://localhost:8888/callbackfitbit",
     expires_in: "31536000"
   }, function(accessToken, refreshToken, profile, done) {

     // TODO: save accessToken here for later use
     done(null, {
       accessToken: accessToken,
       refreshToken: refreshToken,
       expires_at: (new Date().getTime() / 1000) + 24*60*60
     });

     folder = profile["displayName"]
     console.log(folder)
     try {
      fs.mkdirSync(profile["displayName"])
    }
    catch(e) {
      console.log(e)
    }
     // write url to txt
     fs.writeFile('fitbit_data.txt', JSON.stringify({
       accessToken: accessToken,
       refreshToken: refreshToken,
       expires_at: (new Date().getTime() / 1000) + 24*60*60
     }), function (err) {
       if (err) return console.log(err);
       console.log('url > test2.txt');
     });

   });

   passport.use(fitbitStrategy);

   passport.serializeUser(function(user, done) {
     done(null, user);
   });

   passport.deserializeUser(function(obj, done) {
     done(null, obj);
   });

   var fitbitAuthenticate = passport.authenticate('fitbit', {
     successRedirect: '/auth/fitbit/success',
     failureRedirect: '/auth/fitbit/failure'
   });

   // try {
   // const data = fs.readFileSync('fitbit_data.txt',
   //            {encoding:'utf8', flag:'r'});
   //              if (parseFloat(JSON.parse(data)["expires_at"]) > (new Date().getTime() / 1000)) {
   //                  console.error("hello");
   //                   fitbitAuthenticate = function(req, res, next) {
   //                    res.redirect('/auth/fitbit/success')
   //                  }
   //                }
   //  }
   //  catch(err) {
   //
   //    console.log(err)
   //  }






 app.get('/login', fitbitAuthenticate, function(res, req) {
   console.log("hello")
 });

 app.get('/callbackfitbit', fitbitAuthenticate);


 app.get('/auth/fitbit/success', function(req, res, next) {
   let pyshell = new PythonShell('test_fitbit.py', null);
   pyshell.on('message', function (message) {
     // received a message sent from the Python script (a simple "print" statement)
     console.log(message)

   });
   res.redirect("/loginspotify")
 });

 app.get('/auth/fitbit/failure', function(req, res, next) {
   let pyshell = new PythonShell('test_fitbit.py', null);
   pyshell.on('message', function (message) {
     // received a message sent from the Python script (a simple "print" statement)
     console.log(message)

   });
   res.redirect("/loginspotify")
 });

// once user goes to login
app.get('/loginspotify', function(req, res) {

  // generate random key
  var state = generateRandomString(16);
  res.cookie(stateKey, state);

  // redirect to spotify authorization
  var scope = "user-top-read,user-read-recently-played,user-read-playback-state,user-modify-playback-state,streaming";
  res.redirect('https://accounts.spotify.com/authorize?' +
    querystring.stringify({
      response_type: 'code',
      client_id: client_id,
      scope: scope,
      redirect_uri: redirect_uri,
      state: state
    }));

});


// user logged in
app.get('/callback', function(req, res) {

  // your application requests refresh and access tokens
  // after checking the state parameter

  var code = req.query.code || null;
  var state = req.query.state || null;
  var storedState = req.cookies ? req.cookies[stateKey] : null;

  if (state === null || state !== storedState) {
    res.redirect('/#' +
      querystring.stringify({
        error: 'state_mismatch'
      }));
  } else {
    res.clearCookie(stateKey);
    var authOptions = {
      url: 'https://accounts.spotify.com/api/token',
      form: {
        code: code,
        redirect_uri: redirect_uri,
        grant_type: 'authorization_code'
      },
      headers: {
        'Authorization': 'Basic ' + (new Buffer(client_id + ':' + client_secret).toString('base64'))
      },
      json: true
    };

    // get tokens
    request.post(authOptions, function(error, response, body) {
      if (!error && response.statusCode === 200) {

        var access_token = body.access_token,
            refresh_token = body.refresh_token;

        // write tokens to txt file
        console.log(folder)
        fs.writeFile('user_data/test.txt', JSON.stringify(body), function (err) {
          if (err) return console.log(err);
          console.log('token > test.txt');
        });

        // write url to txt
        fs.writeFile('user_data/test2.txt', querystring.stringify({
          access_token: access_token,
          refresh_token: refresh_token
        }), function (err) {
          if (err) return console.log(err);
          console.log('url > test2.txt');
        });

        // we can also pass the token to the browser to make requests from there
        res.redirect('/#' +
          querystring.stringify({
            access_token: access_token,
            refresh_token: refresh_token
          }));
      } else {
        // login credentials incorrect
        res.redirect('/#' +
          querystring.stringify({
            error: 'invalid_token'
          }));
      }
    });
  }
});


app.post("/alarm", function(req, res) {
  console.log(req.body)

  options = {
    mode: "text",
    pythonOptions: ['-u'], // get print results in real-time
    args:[req.body["hour"], req.body["minute"]]
  }
  let pyshell = new PythonShell('sleep_alg.py', options);
  messages = ""
  pyshell.on('message', function (message) {
    // received a message sent from the Python script (a simple "print" statement)
    messages+='<h1 style="font-size: 20px;color:#ff5100;font-family: monospace, sans-serif;text-align: center;">' + message + "</h1>"

  });
  pyshell.end(function (err, code, signal) {
  if (err) res.send("We could not make a prediction");
  console.log('The exit code was: ' + code);
  console.log('The exit signal was: ' + signal);
  console.log('finished');
  res.send(messages)
});
let pyshell2 = new PythonShell('alarm.py', options);
pyshell2.on('message', function (message) {
  // received a message sent from the Python script (a simple "print" statement)
  console.log(message)

});
});





// log the port
console.log('Listening on 8888');
app.listen(8888);

// collect fitbit token
// PythonShell.run('test_fitbit.py', null, function (err) {
//   if (err) throw err;
//   console.log('finished fitbit');
//   fitbit_auth = true;
// });
