# Turo Host Assistant
This small utility helps Turo hosts to easily prepare tax returns related to Turo earnings and expenses. Not only earnings are important for end of year tax returns, but also hosts must deduct the expenses. The best deduction could be done on mileage basis. Turo does not provide hosts this information easily. This script just crawls receipt pages and parses all information needed for hosts.

## Instructions
We highly recommend to use pyenv and create a specific Python 2.7 environment with name turoenv. .python-version file in this library automatically activates that pyenv. If you don't use pyenv just run this script on python 2.7

`pip install -r requirements.txt` to install the libraries needed.

Go to config file and set your username and password.

You need selenium web driver to run this application. Download the appropriate driver for your Chrome browser version from [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads).

You will see field names in config files. These mostly will cover all fields appear on a receipt page. But Turo everyday adds new kind of reimbursements or expenses. 
If your assistant halts with an error like `ValueError: dict contains fields not in fieldnames: 'DROPOFF'` that means there is a key called `DROPOFF` found in Turo receipt but your application does not recognize it. In that case you just need to put this field name into config file fieldnames list

Turo gives all customers an export in CSV format the list of all trips under their account. Please post the list in `Reservation URL` to the trips.txt file. The assistant takes this files as an input to crawl. For sure this link can be extracted from Turo history pages but everyday Turo renews the page structure. That may break our script. We prefer to give the list manually.