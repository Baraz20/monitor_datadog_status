# monitor_datadog_status

> Tal Baraz | 26/07/2021
--------------------------
This program, like it's name says, monitors the DataDog's components status

It prints to STDIN at a regular frequency (The frequency is configurable) the status of *non-operational* components.

## Usage
```
usage: monitor_datadog_status.py [-h] -f FREQUENCY [--test]

optional arguments:
  -h, --help            show this help message and exit
  -f FREQUENCY, --frequency FREQUENCY
                        the frequency at which you want to check DataDog's component status.

  --test                this flag enables testing mode - statuses are forged!
```

## Notes
* This program ran using Python 3.9.5
* This program ran on Ubuntu 20.04.2