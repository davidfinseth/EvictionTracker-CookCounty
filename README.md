## Cook County Eviction Tracker
A web scraping robot that keeps track of daily eviction filings in Cook County Illinois.

## Motivation
During the COVID-19 pandemic it became clear that renters needed more protections in the face of evictions. Despite the passing of the CARES act evictions still continued to be filled across the county. 

## Data

[Eviction Dashboard](https://charts.mongodb.com/charts-project-0-bxvpg/public/dashboards/79497833-a440-4c4c-af82-e12b23d33026)
[Eviction Data](https://docs.google.com/spreadsheets/d/1wYpBQffEyS-xYp54R1hDiLBNOS2kQEeXzhjNi_C6d0U/edit?usp=sharing)

## Tech/framework used

<b>Built with</b>
- [Selenium](https://selenium-python.readthedocs.io/)
- [MongoDB](https://www.mongodb.com/)
- [gspread](https://github.com/burnash/gspread)
- [Heroku](https://heroku.com)


## Features
- Scrapes all case information from Cook County Docket lookup
- Cross checks case number with Cook County Sherif's records for eviction filing
- Searches location of filing across multiple geolocation api's to find correct address
- Uploads data to public spreadsheet
- Uploads data to private database for visualization

## Code Example
```python
import evictionscrapper

# Get all records from a sepcific date
evictionscrapper.GetAllRecordsByDate('07/29/2020')

# Get all records from between two dates
evictionscrapper.GetAllRecordsBetweenDates('07/01/2020', '07/29/2020)
```

## Contribute
Reach out or make a pull request if you would like to contribute.

## Credits
This project was built with partnership from:
 - [Autonomous Tenants Union](https://www.autonomoustenantsunion.org/)
 - [Tenants United](https://www.tenantsunitedchicago.org/)


MIT © [David Finseth](https://github.com/davidfinseth)