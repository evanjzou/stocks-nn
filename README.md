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

### Tips for Installing

- pip can be downloaded through the following link:
  https://pip.pypa.io/en/stable/installing/
    
    
- virtualenv, h5py, pyaml, and bitstring can all be installed by running 
  the following command:
  ```
  pip install <name of software>
  ```
  for example:
  ```
  pip install virtualenv
  ``` 
  
- pkg-config must be intalled through a different installation software
  such as homebrew. This can be done using the following link:
  http://macappstore.org/pkg-config/  
  

## Running The Software
To run the software, first, while in the HEAD directory enter the command 
```
. .venv3/bin/activate
``` 
Next, enter the command
```  
python data_interpreter.py
```  
This will run the software for the default company, GOOG

## Changing Test Parameters
Currently the only way to change the parameters of the test is by directly
editing the code, however there are a few simple changes that can be made 
that will alter the test run.

If you wish to run the test for a different company, open data\_interpreter.py 
in a text editor, and change the value of COMPANY\_NAME on line 21 from 'GOOG'
to the stock ticker of the company you wish to run the test for.

## Troubleshooting and Known Defects

- If python 2.7 is already installed on your computer, your computer may be
  have python 2.7 set to the default python, which will result in problems
  running the software and installing software with pip.
  
  To solve this issue, run all python commands using the keyword python3
  and all pip installations using the command pip3. For example:
  ```
  pip3 install virtualenv
  ```
  ```
  python3 data_interpreter.py
  ```
  
- An error may occur when using too long of a training duration that 
  will result in the following error:
  ```
  Traceback (most recent call last):
  File "data_interpreter.py", line 135, in <module>
    TEST_DURATION_IN_DAYS), TEST_DURATION_IN_DAYS+1)
  File "data_interpreter.py", line 105, in createArrayIterator
    XList.append(timeInstanceToArray(timeInstances[i]))
  IndexError: list index out of range
  ```
  This is the result of a known defect where the system is querying for
  days in the past that we do not have data on. For example, PYPL has not
  been publicly traded for the default duration of 2000 days. This can be 
  fixed by reducing the training duration or simply searching with a 
  different company.
  
     -Note- reducing the training duration may reduce the accuracy of the
            results.
  

## Resources

Nervana Neon: <link>

AlphaVantage: <link>
