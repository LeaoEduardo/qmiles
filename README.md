Qmiles
===

Qmiles takes care of web scraping and automatically producing reports useful for travelling quotations.

## Pre-requisites:
* [Docker](https://www.docker.com/)

## Quick start
First, you need to create a `kwargs.json` file, such as:
```json
{ 
  "arrival_date": "2023-11-15",
  "departure_date": "2023-11-28",
  "origin_city": "GIG",
  "destiny_city": "MCO", 
  "guests": {
    "adults": 2,
    "minors": {
      "amount": 2,
      "ages": [5, 13]
    },
    "class": "economy"
  }
}
```

After that, you need to run:
```
sh run_web_scraper kwargs.json report.csv
```