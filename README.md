Installation
-----------

```
git clone git@github.com:mindflayer/pyrgeramt.git
virtualenv -p python3 .env
source .env/bin/activate
pip install -r requirements.txt
```

Usage
-----
After the area selection, if there are free slots in it, it will point your favourite browser to one of the reservation page.
You'll probably need to solve a CAPTCHA, do it and tell the script you are ready to open all the pages it found for you.

```
python berlin.py --service anmeldung  # or 'abmeldung', or what else?
```
