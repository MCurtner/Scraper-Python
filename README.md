# Scraper-Python
Webscraper built with Python's BeautifulSoup to collect all information from different grocery stores.  The data collected is saved to a PostgresDB for usage in a webapp.

## Summary

This project is designed to be run as a service with the [Groceries Web App](https://github.com/MCurtner/groceriesapp) and [Springboot Backend](https://github.com/MCurtner/grocery-backend) and a PostgresDB. In the current configuration the web scraper scrapes relevant grocery product from two different site and store the formatted objects in the PostgresDB.  The springboot backend server creates the REST API to retrieve the grocery values to be displayed in the web application. 