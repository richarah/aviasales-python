# aviasales-python

A Python wrapper for accessing flight ticket prices, routes, and other data via the Aviasales API

## Features

* Retrieve the cheapest tickets for specific dates.
* Fetch the latest ticket prices over a period of time.
* Explore flight price trends in a calendar format.
* Get prices for alternative (nearest) directions.
* Access popular routes for specific airlines and cities.
* Retrieve airline logos and currency exchange rates.
* Support for one-way and round-trip flights, non-stop searches, and custom sorting.

## Requirements

* Python 3.12
* `requests` library
* `python-dotenv` library for environment variable management

## Installation

1. Clone the repository:
      git clone https://github.com/your-username/aviasales-python.git

2. Navigate into the project folder:
      cd aviasales-python

3. Install the required dependencies:
      pip install -r requirements.txt

4. (Optional) If you wish to use the wrapper in different currencies or markets, you can modify the `currency` and `market` parameters in the `AviasalesAPI` class when instantiating it.

## Usage

1. **Import the API Wrapper:**
      `from aviasales import AviasalesAPI`

2. **Initialize the API Wrapper:**
      `api = AviasalesAPI(API_TOKEN)`

3. **Example Usage:**
   
   * Get the latest prices for a period:
        `data = api.get_latest_prices("OSL", "ALC", "2025-12-07", "year")`

## Methods

The following methods are available in the `AviasalesAPI` class:

* `prices_for_dates`: Get prices for specific dates.
* `get_latest_prices`: Get prices over a specific period.
* `prices_month_matrix`: Get a matrix of prices for a given month.
* `prices_nearest_places_matrix`: Get prices for nearest directions.
* `prices_week_matrix`: Get a weekly calendar of prices.
* `prices_cheap`: Get the cheapest tickets, including options with transfers.
* `grouped_prices`: Get the cheapest tickets grouped by an attribute.
* `prices_direct`: Get the cheapest non-stop tickets.
* `prices_calendar`: Get flight price trends in a calendar format.
* `airline_directions`: Get popular routes for a given airline.
* `city_directions`: Get the most popular destinations from a specified city.
* `popular_directions`: Get the cheapest tickets to popular destinations.
* `special_offers`: Get special flight offers.
* `currency_rates`: Get current exchange rates.
* `airline_logo`: Get the URL of an airline's logo.

## License

MIT
