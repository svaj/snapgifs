#! /usr/bin/env python
from pysnap import Snapchat
import os
import sys
import subprocess
import glob
import ConfigParser
import optparse

FRAME_RATE = 12  # frame rate of video if we cannot detect it.
SNAPCHAT_LOGIN = ''
SNAPCHAT_PASSWORD = ''
SNAPCHAT_RECIPIENTS = ''

# Process defaults
read_config = False
try:
    config = ConfigParser.RawConfigParser()
    path = os.path.abspath('snapgifs.ini')
    config.read(path)
    read_config = True
except:
    pass

if read_config:
    try:
        SNAPCHAT_LOGIN = config.get('snapgifs', 'login').strip()
    except Exception as e:
        print "no default login"
    try:
        SNAPCHAT_PASSWORD = config.get('snapgifs', 'password').strip()
    except:
        print "no default password"
    try:
        SNAPCHAT_RECIPIENTS = config.get('snapgifs', 'recipients').strip()
    except:
        print "no default recipients"

# prepare optparser
usage = "Usage: snapgifs [options] /path/to/image.gif"
parser = optparse.OptionParser(usage=usage)
parser.add_option('-l', '--login', help='snapchat username', default=SNAPCHAT_LOGIN, dest='login')
parser.add_option('-p', '--password', help='snapchat password', default=SNAPCHAT_PASSWORD, dest='password')
parser.add_option('-r', '--recipients', help='snapchat recipients', default=SNAPCHAT_RECIPIENTS, dest='recipients')

# Parse options
(opts, args) = parser.parse_args()
if len(args) != 1:
    print usage
    sys.exit(-1)

# Load options
if opts.login:
    SNAPCHAT_LOGIN = opts.login
if opts.password:
    SNAPCHAT_PASSWORD = opts.password
if opts.recipients:
    SNAPCHAT_RECIPIENTS = opts.recipients


def gif_to_snap(gif='', login='', password='', recips=''):
    mp4 = convert_to_mp4(gif)
    if len(mp4) <= 0:
        print "Whoa, we couldn't convert that gif to a video! BEEP BOOP ERRORS."
        return

    print "Logging into snapchat as " + login
    s = Snapchat()
    s.login(login, password)
    if s.username != login:
        print "Derp, invalid credentials, doofus."
        return

    media_id = s.upload(path=mp4)
    if media_id is None:
        print "Error while uploading to snapchattery"
        return

    sent = s.send(media_id=media_id, recipients=recips,time=10)
    if sent:
        print "Wow it happened! you are so cool."
    else:
        print "Sorry, it failed sending... :("

def convert_to_mp4(filepath=''):
    """
    Converts a gif to mp4 using avconv
    :param filepath: the gif file to read in and convert to mp4.
    :return: filepath to the mp4, should be in same dir as gif
    http://stackoverflow.com/questions/3212821/animated-gif-to-avi-on-linux/3212958#3212958
    """
    print "Converting " + filepath + " to mp4..."
    base = os.path.splitext(filepath)
    basename = base[0]
    subprocess.call([
        'convert',
        '-coalesce',
        '-background',
        'white',
        filepath,
        basename + '%05d.png'
    ])

    # Guess at frame rate
    # identify -format "Frame %s: %Tcs\n" ~/test.gif   - frame life in centiseconds - how odd.
    frameratestr = subprocess.check_output([
        'identify',
        '-format',
        '%T\n',
        filepath
    ])
    if len(frameratestr) <= 0:
        framerate = str(FRAME_RATE)
    else:
        # Get first frame's lifetime...
        lifetime = frameratestr.split('\n', 1)[0]
        # print "frame lifetime is " + lifetime + "cs"
        framerate = str(float(lifetime))
        if float(framerate) <= 0.0:
            framerate = FRAME_RATE
    print "Using frame rate of " + framerate


    # avconv -r 8 -i frame%02d.png -qscale 4 test.mp4
    # convert frames to avi
    subprocess.call([
        'avconv',
        '-r',
        framerate,
        '-i',
        basename + '%05d.png',
        '-qscale',
        '4',
        '-b:a',
        '192k',
        '-y',
        '-loglevel',
        'quiet',
        '-vf',
        'scale=trunc(iw/2)*2:trunc(ih/2)*2',
        basename + '.mp4'
    ])

    # clean up
    for fl in glob.glob(basename + '*png'):
        os.remove(fl)
    return basename + '.mp4'

# Actually do the thing!
gif_to_snap(gif=args[0], login=SNAPCHAT_LOGIN, password=SNAPCHAT_PASSWORD, recips=SNAPCHAT_RECIPIENTS)
