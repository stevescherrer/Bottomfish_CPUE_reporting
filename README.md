# Bottomfish_CPUE_reporting

Python code for web scraping historical catch records of Deep 7 bottomfish hosted by Hawaii's Division of Aquatic Resources

This is handled  by the script: 'catch_reports_to_data.py'

Running this script outputs a file called "Bottomfish_CPUE_reporting.csv" containing a table of the following variables
  - species
  - pieces caught
  - pieces sold
  - value
  - price/pound
  
Prior to running locally, you will need to update the path within the 'build_csv' function located on line 126.
