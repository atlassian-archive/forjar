Forjar
=========

Forjar (spanish for forge) is a data generator for mocking datasets. You setup a schema, a period of time, and a model of how the data should perform over time and then run it!

## Dependancies

 - sqlalchemy

## Running

There is currently one example.  Run

    python examples/boatio.py

The default settings will run the simulation for 365 days and pump it to the sqlite database called forjer.db.

To run the simulation for 150 days into the database at sqlite:///boatio.sqlite use

    python examples/boatio.py -d 150 -e sqlite:///boatio.sqlite



