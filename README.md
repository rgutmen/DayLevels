# DayLevels
 
The intention of this repository is analize the previous fourteen days to get the standard deviation and added on top and below to the opening price for the current day, where those levels will be consider as target.

## Files

The program consist of mainly three files:
* app.py: API to send the data from the database in json format.
* openMarket.py: this script should run at the market opening in RTH. (using crontab)
* nightlyReport.py: this script should run once the market has close. (using crontab)

## Instalation

To install the dependecies run:


```pip install -r requirements.txt```

