This repo contains the packages to be used in whatSticks06. It includes config.py and models.py that will be shared across the apps inside WhatSticks06.

packages2 is different from whatSticks06-modules because it includes flask_login and the necessary objects. Models.py creates the login_manager which get's imported to __init__.py in the web apps of whatSticks05 or whatSticks06.

The config.py maps to a json file with all the important and sensitive information. This just needs to be updated if the package is used in another computer.

Here is a brief set of instructions:

1- Set up root directory here:
root directory: C:\Users\captian2020\Documents\whatSticks06-modules2
This is done by cloning this repo to this location

2- create environment:
python -m venv venv_wsh06

3- install into pip:
This package is called wshmodules. 
And in the terminal I type:
(venv_wsh06) C:\Users\captian2020\Documents\whatSticks06-modules2>pip install -e wshmodules
For these packages I will also need pip install sqlalchemy

When I use them I am importing ‘wsh_config’ and/or ‘wsh_models’

Here is an example using wsh_config:
(venv_wsh06) C:\Users\captian2020\Documents>python
Python 3.10.2 (tags/v3.10.2:a58ebcc, Jan 17 2022, 14:12:15) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from wsh_config import ConfigDev
>>> config = ConfigDev()
>>> config.SQL_URI
'sqlite:///D:\\databases\\wsh06\\wsh06.db'


