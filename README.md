# Beervintory
## Info
Beervintory is an inventory system created in Flask and uses SQLAlchemy and WTForms to keep track of the various objects.
It is located at [beer.west.isilon.com](http://beer.west.isilon.com)
## Goals
To let users:
* Rate previous beers
* View current beers
* Vote on upcoming beers

To help the kegmeister:
* Keep track of cleaning dates
* View current inventory
* Track beer consumption
* Track CO2 status

## How to install
```
git clone https://github.west.isilon.com/bhanderson/beervintory
cd beervintory
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python db_create.py
python run.py
```
