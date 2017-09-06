# Capture The Flag!
###### A Super-Secure™ FileServer

Insecure web server for hacking practice.

![Screenshot](http://i.imgur.com/W11Zchd.png)

## Features

- sql injection
- XSS
- session hijacking
- easy-to-guess passwords
- insecure file uploads

## Basic Setup (mac)

Quick-and-dirty setup to get this running locally. Suitable for personal use on a device you own or don't care about. Just keep in mind that, while this server is running, the device is hackable by anyone with access to it. If you run this server on a port that's open to the internet, then "anyone with access" means "everyone in the world". Be smart.

```
# clone
git clone https://github.com/jtschoonhoven/capture-the-flag.git
cd capture-the-flag

# install dependencies
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# start server
python capture_the_flag/app.py
open http://127.0.0.1:5000/
```

## Advanced Setup (ubuntu)

I am not a security expert and none of these steps will keep your system safe from a competent hacker. If you're going to expose this server to the internet, please make sure it's being hosted from a device that can be erased or ransacked without anyone feeling bad about that.

These steps are meant as a rough template. You need not use AWS or Ubuntu.

1. spin up a new micro AWS EC2 instance (use the free tier)
2. ssh to the instance using its public IP address and your private key, e.g `ssh -i /private/key.pim ec2-user@54.193.12.345`
3. install dependencies `sudo yum install git-all nginx`
4. pick a source directory and `chown` it, e.g. `cd /srv & sudo chown ec2-user /srv`
5. clone the repo to the source directory, e.g. `git clone https://github.com/jtschoonhoven/capture-the-flag.git`
6. configure nginx to proxy the flask server on port 5000
7. copy dependencies to a `chroot` jail for nginx and the flask server (TODO: fill in details)
8. run the flask server and nginx with `chroot` (TODO: fill in details)
9. point a web browser to your host's IP address and hack away
