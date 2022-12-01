// initialize the express application
const express = require("express");
var cookieParser = require('cookie-parser');
var cors = require('cors');
var FitbitStrategy = require('passport-fitbit-oauth2').FitbitOAuth2Strategy;
var passport = require('passport');
var session = require('express-session');
var bodyParser = require('body-parser');
var fs = require("fs");

var app = express();

var save = "http://127.0.0.1:8080/"
app.use(express.static(__dirname + '/public'))
    app.use(cookieParser());
    app.use(bodyParser());

    app.use(session({ secret: 'keyboard cat' }));

    app.use(passport.initialize());
    app.use(passport.session({
      resave: false,
      saveUninitialized: true
    }));


    const CLIENT_ID = "238T5P";
    const CLIENT_SECRET = "1d37c3db41c1eb5b84b770fb97069f59";

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
        expires_at: (new Date().getTime() / 1000) + 31536000
      });

      // write url to txt
      fs.writeFile('fitbit_data.txt', JSON.stringify({
        accessToken: accessToken,
        refreshToken: refreshToken,
        expires_at: (new Date().getTime() / 1000) + 31536000
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

    app.get('/login', fitbitAuthenticate);
    app.get('/callbackfitbit', fitbitAuthenticate);

    app.get('/auth/fitbit/success', function(req, res, next) {
      res.send(req.user);
    });

// log the port
console.log('Listening on 8888');
app.listen(8888, "0.0.0.0");
