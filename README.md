# Capture The Flag!
###### A Super-Secure™ FileServer

![Screenshot](http://i.imgur.com/W11Zchd.png)

## Features

- sql injection
- XSS
- session hijacking
- easy-to-guess passwords
- insecure file uploads

## Setup (mac)
```
# clone
git clone git@github.com:jtschoonhoven/capture-the-flag.git
cd capture-the-flag

# install dependencies
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# start server
python capture_the_flag/app.py
open http://127.0.0.1:5000/
```
