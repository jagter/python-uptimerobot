Uptime Robot integration for Python
============

Uptime Robot http://uptimerobot.com integration for your Python project. 

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash
	
	$ pip install python-uptimerobot

To get the latest commit from GitHub

.. code-block:: bash

    $ pip install -e git+git://github.com/jagter/python-uptimerobot.git#egg=uptimerobot

 


Usage
-----

Use with Python:

.. code-block:: python

    >>> from uptimerobot.uptimerobot import UptimeRobot
    >>> up = UptimeRobot(UPTIME_ROBOT_API_KEY)
    >>> up.addMonitor("arteria-webpage", "https://www.arteria.ch/")
    True


Use in Shell: (success if return value is 0, null)

.. code-block:: bash

    cd /path/to/script/
    chmod 755 uptimerobot.py # if necessary
    ./uptimerobot.py monitorFriendlyName=arteria-webpage monitorURL=https://www.arteria.ch/


History
-------

latest

0.1.5

Fixed error where requestApi didn't return when the API request failed

0.1.4

- Extended API with `.editMonitor()`.
- Updated to use HTTPs by default.

0.1.3

- Extended API with `.deleteMonitorById()`.

0.1.1 

- Extended API with `.getMonitors()`.

0.1.0

- Releveled version

0.0.7

- Python 3.x support


About the API
-------------
The full API is documented here: https://uptimerobot.com/api
