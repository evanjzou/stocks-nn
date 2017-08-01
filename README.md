# stocks-nn
This is an experimental project applying neural networks to stock data

## Installation
This neural network requires a Mac or Linux machine in order to run.

In addition, the following software must be downloaded
- python: Version 3.4 or greater
- pip: used to install python dependencies
- virtualenv: used to create virtual environments for running the software
- h5py: Enables loading of hdf5 formats
- pyaml: Parses YAML format inputs
- pkg-config: Retrieves information about installed libraries
- bitstring: Python library for parsing numbers into binary format

After installing these dependencies, you must initialize the neon library.
To do this, connect to the HEAD directory in your command line. 
From there, enter the command 'make'.

## Running The Software
To run the software, first, while in the HEAD directory enter the command 

  . .venv3/bin/activate
  
Next, enter the command

  python data_interpreter.py
  
This will run the software for the default company, GOOG

## Changing Test Parameters
Currently the only way to change the parameters of the test is by directly editing the code, however there are a few simple changes that can be made that will alter the test run.

If you wish to run the test for a different company, open data_interpreter.py in a text editor, and change the value of COMPANY_NAME on line 21 from 'GOOG' to the stock ticker of the company you wish to run the test for.

## Resources

Nervana Neon: <link>

AlphaVantage: <link>
