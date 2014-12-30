snapgif
=======

Ever want to spam people via snapchat with gifs?  Now you can!
By leveraging the "unofficial" snapchat API, avconv, and imagemagick you can send gifs via snapchat!

Installation
---

Installing on Ubuntu 14.10:

```
sudo apt-get install python-pip imagemagick libav-tools
git clone git@github.com:svaj/snapgifs.git
cd snapgifs
pip install -r requirements.txt
```


Installing on OS X (please have brew already installed):
```
sudo easy_install pip
brew install libav imagemagick
git clone git@github.com:svaj/snapgifs.git
cd snapgifs
pip install -r requirements.txt
```

Configuration
---

You can set default parameters to snapgif via editing snapgifs.ini and populating it thusly:
```
[snapgifs]
login = snapchat_login
password = snapchat_password
recipients = snapchat,users,to,send,to
```

Use
---

`./snapgif -l "snapchat_login" -p "snapchat_password" -r "snapchat,users,to,send,to" /path/to/image.gif`.


Like this tool?
Feel free to donate btc to:
18TwRYfB27pM2r9sGLdn2WkSfFZbKToEAq
