Welcome to the Super Secure Web Application!

This app serves up a simple interface to register and login.
It enforces a strict password requirement.  It must be at least 9 characters long containing at least one of each:
    - lower case alpha
    - upper case alpha
    - digit
    - a valid symbol @,#,&,(,),?,^

Requirements
============
Python 3.6
Linux - has only been tested on Linux
Git
*OWASP Zap Application (for tests only)

Installation
============

1) Highly recommended to create a virtual python environment
mkvirtualenv -p /usr/bin/python3 secapp

2) checkout the project from git & setup:

git clone https://github.com/shizzz477/secapp.git
cd secapp

3) install requirements:
pip install -r requirements.txt

Running
=======
if you are using a virtual python 3 environment:
python secapp.py

If not:
python3 secapp.py

The server should be runing at:
http://localhost:5000/
