![TASCS LOGO](./assets/logo.png)

# Bluehost Apache Weblog Parser version: 1.6.0

#### Created as a replacement of cPanel's "View Latest Activity" and Google Analytics

---

1. Securely (passphrased private cert) download compressed Apache weblogs from hosting provider
    * Windows uses: Putty Pageant 0.80
    * Linux uses: ssh-agent 
      * for cron jobs it uses [keychain](https://linux.die.net/man/1/keychain))
1. Decompress and save server log files locally
1. PARSE log files
1. LOAD unique sources from parsed logs into sources table
    * New entries into lookup table will have a NULL COUNTRY and DESCRIPTION value
1. LOAD parsed logs into database logs table
1. Convert ASN country Alpha-2 code to full country name using IPWhois
1. SET full county names, ASN Descriptions, and ALPHA2 Codes in

sources table
     *If IPWhois error during source ip lookup, exception message is entered as country name
     * If country ALPHA2 code not found, log source

###### Source IP to Country Name provided by IPWhois utility get_countries

---
OPTIONAL DEPENDENCIES:

1. analyses (dashboard via Dash/Plotly)

OPTIONAL DEV DEPENDENCIES:

1. dev (testing, linting)

---

#### src folder contains

* bluehost_log_parser: Python files needed to retrieve, process, and store web server logs to a database
* dashboard: Python files needed to analyze data stored in a database

#### assets folder contains

* 'sample_unzipped_logfile'  with anonymized data
* 'logo.png' for README logo
* A template of '.env' config file (sample.env)

#### misc folder contains

* Batch file for running a Scheduled Task in Windows
* Shell script for running a cron job in Linux

#### PRE_LAUNCH TODO's

* [ ] TASC 1 - COPY 'sample.env' from 'assets' folder to project root, rename '.env' and edit values to fit your needs
* [ ] TASC 2 - ENSURE your keychain/ssh-agent is running for access to remote log files securely

#### PARSE TODO's

* [ ] TASC 1 - run 'uv run main.py' from src/bluehost_log_parser/

#### ANALYSIS TODO's

* [ ] TASC 1 - run 'uv run app.py' from src/dashboard/
