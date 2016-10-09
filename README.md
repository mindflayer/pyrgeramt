Installation
-----------

```
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Usage
-----
After the area selection, if there are free slots in it, it will point your favourite browser to the reservation pages.
If you got some captchas, just solve one of them and execute the script again.

```
python berlin.py --service anmeldung  # or 'abmeldung', or what else?
```
