import os
import requests
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta

class AviasalesAPI:
    BASE_URL = "https://api.travelpayouts.com"

    def __init__(self, token, currency="EUR", market="eu"):
        """
        Initialize the API wrapper.

        :param token: Your Aviasales API token.
        :param currency: Default currency (default "EUR").
        :param market: Data market (default "EUR").
        """
        self.token = token
        self.currency = currency
        self.market = market
        self.session = requests.Session()

    def _get(self, path, params=None):
        """
        Internal helper to perform a GET request.
        Automatically adds the token, currency, and market to the query.
        """
        if params is None:
            params = {}
        params.setdefault("token", self.token)
        params.setdefault("currency", self.currency)
        params.setdefault("market", self.market)
        url = f"{self.BASE_URL}{path}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def prices_for_dates(self, origin, destination, departure_at, return_at=None,
                         one_way=True, direct=False, sorting="price",
                         unique=False, limit=30, page=1):
        """
        Returns the cheapest tickets for specific dates.
        (Replaces older endpoints like /v1/city-directions, /v1/prices/cheap, etc.)

        :param origin: IATA code of the departure city/airport.
        :param destination: IATA code of the destination city/airport.
        :param departure_at: Departure date in YYYY-MM or YYYY-MM-DD format.
        :param return_at: Return date (if round-trip).
        :param one_way: If True, one-way search; otherwise round-trip.
        :param direct: If True, non-stop flights only.
        :param sorting: Sorting parameter ("price" or "route").
        :param unique: Return only unique routes.
        :param limit: Number of records per page.
        :param page: Page number.
        """
        path = "/aviasales/v3/prices_for_dates"
        params = {
            "origin": origin,
            "destination": destination,
            "departure_at": departure_at,
            "one_way": str(one_way).lower(),
            "direct": str(direct).lower(),
            "sorting": sorting,
            "unique": str(unique).lower(),
            "limit": limit,
            "page": page
        }
        if return_at:
            params["return_at"] = return_at
        return self._get(path, params)

    def get_latest_prices(self, origin, destination, beginning_of_period, period_type,
                          one_way=True, sorting="price", page=1, limit=1000,
                          show_to_affiliates=True, trip_class=0, trip_duration=None):
        """
        Returns the prices for airline tickets over a specific period.
        (Wraps /aviasales/v3/get_latest_prices)

        :param origin: IATA code of the departure.
        :param destination: IATA code of the destination.
        :param beginning_of_period: Start of the period (e.g., "2025-12-07").
        :param period_type: Type of period ("year", "month", or "day").
        :param one_way: True for one-way tickets.
        :param sorting: Sorting rule ("price" is default).
        :param page: Page number for pagination.
        :param limit: Number of records per page.
        :param show_to_affiliates: If True, returns partner offers.
        :param trip_class: Flight class (0 for economy, 1 for business, etc.).
        :param trip_duration: Length of stay in days.
        """
        path = "/aviasales/v3/get_latest_prices"
        params = {
            "origin": origin,
            "destination": destination,
            "beginning_of_period": beginning_of_period,
            "period_type": period_type,
            "one_way": str(one_way).lower(),
            "sorting": sorting,
            "page": page,
            "limit": limit,
            "show_to_affiliates": str(show_to_affiliates).lower(),
            "trip_class": trip_class
        }
        if trip_duration is not None:
            params["trip_duration"] = trip_duration
        return self._get(path, params)

    def prices_month_matrix(self, origin, destination, month, show_to_affiliates=True,
                            one_way=True, trip_duration=None, limit=30):
        """
        Returns the calendar of prices for a given month.
        (Wraps /v2/prices/month-matrix)

        :param origin: IATA code of departure.
        :param destination: IATA code of destination.
        :param month: Beginning of the month in YYYY-MM-DD format.
        :param show_to_affiliates: If True, returns partner offers.
        :param one_way: True for one-way tickets.
        :param trip_duration: Optional duration of stay.
        :param limit: Number of days (e.g. 30 or 31).
        """
        path = "/v2/prices/month-matrix"
        params = {
            "origin": origin,
            "destination": destination,
            "month": month,
            "show_to_affiliates": str(show_to_affiliates).lower(),
            "one_way": str(one_way).lower(),
            "limit": limit
        }
        if trip_duration is not None:
            params["trip_duration"] = trip_duration
        return self._get(path, params)

    def prices_nearest_places_matrix(self, origin, destination, distance, limit=5,
                                     show_to_affiliates=True, depart_date=None,
                                     return_date=None, flexibility=0):
        """
        Returns prices for alternative (nearest) directions.
        (Wraps /v2/prices/nearest-places-matrix)

        :param origin: IATA code of departure.
        :param destination: IATA code of destination.
        :param distance: Search radius (in km).
        :param limit: Number of variants to return.
        :param show_to_affiliates: Whether to return only partner offers.
        :param depart_date: Optional departure date.
        :param return_date: Optional return date.
        :param flexibility: Date flexibility (0-7).
        """
        path = "/v2/prices/nearest-places-matrix"
        params = {
            "origin": origin,
            "destination": destination,
            "distance": distance,
            "limit": limit,
            "show_to_affiliates": str(show_to_affiliates).lower(),
            "flexibility": flexibility
        }
        if depart_date:
            params["depart_date"] = depart_date
        if return_date:
            params["return_date"] = return_date
        return self._get(path, params)

    def prices_week_matrix(self, origin, destination, depart_date, return_date,
                           show_to_affiliates=True):
        """
        Returns a weekly calendar of prices near the target dates.
        (Wraps /v2/prices/week-matrix)

        :param origin: IATA code of departure.
        :param destination: IATA code of destination.
        :param depart_date: Departure date (YYYY-MM-DD).
        :param return_date: Return date (YYYY-MM-DD).
        :param show_to_affiliates: If True, returns partner offers.
        """
        path = "/v2/prices/week-matrix"
        params = {
            "origin": origin,
            "destination": destination,
            "depart_date": depart_date,
            "return_date": return_date,
            "show_to_affiliates": str(show_to_affiliates).lower()
        }
        return self._get(path, params)

    def prices_cheap(self, origin, destination, depart_date=None, return_date=None, page=1):
        """
        Returns the cheapest tickets (including options with transfers).
        (Wraps /v1/prices/cheap)

        :param origin: IATA code of departure.
        :param destination: IATA code of destination.
        :param depart_date: Optional departure date (YYYY-MM).
        :param return_date: Optional return date (YYYY-MM).
        :param page: Page number for pagination.
        """
        path = "/v1/prices/cheap"
        params = {
            "origin": origin,
            "destination": destination,
            "page": page
        }
        if depart_date:
            params["depart_date"] = depart_date
        if return_date:
            params["return_date"] = return_date
        return self._get(path, params)

    def grouped_prices(self, origin, destination, group_by="departure_at",
                       departure_at=None, return_at=None, direct=False, trip_duration=None):
        """
        Returns the cheapest tickets grouped by a specified attribute.
        (Wraps /aviasales/v3/grouped_prices)

        :param origin: IATA code of departure.
        :param destination: IATA code of destination.
        :param group_by: Grouping parameter ("departure_at" or "month").
        :param departure_at: Optional departure date.
        :param return_at: Optional return date.
        :param direct: If True, only non-stop tickets.
        :param trip_duration: Optional trip duration filter.
        """
        path = "/aviasales/v3/grouped_prices"
        params = {
            "origin": origin,
            "destination": destination,
            "group_by": group_by,
            "direct": str(direct).lower()
        }
        if departure_at:
            params["departure_at"] = departure_at
        if return_at:
            params["return_at"] = return_at
        if trip_duration is not None:
            params["trip_duration"] = trip_duration
        return self._get(path, params)

    def prices_direct(self, origin, destination, depart_date=None, return_date=None):
        """
        Returns the cheapest non-stop tickets.
        (Wraps /v1/prices/direct)

        :param origin: IATA code of departure.
        :param destination: IATA code of destination.
        :param depart_date: Optional departure date.
        :param return_date: Optional return date.
        """
        path = "/v1/prices/direct"
        params = {
            "origin": origin,
            "destination": destination
        }
        if depart_date:
            params["depart_date"] = depart_date
        if return_date:
            params["return_date"] = return_date
        return self._get(path, params)

    def prices_calendar(self, origin, destination, depart_date, calendar_type="departure_date", length=None, return_date=None):
        """
        Returns flight price trends in a calendar format.
        (Wraps /v1/prices/calendar)

        :param origin: IATA code of departure.
        :param destination: IATA code of destination.
        :param depart_date: Departure date (YYYY-MM).
        :param calendar_type: Calendar type ("departure_date" or "return_date").
        :param length: Optional length of stay.
        :param return_date: Optional return date.
        """
        path = "/v1/prices/calendar"
        params = {
            "origin": origin,
            "destination": destination,
            "depart_date": depart_date,
            "calendar_type": calendar_type
        }
        if length is not None:
            params["length"] = length
        if return_date:
            params["return_date"] = return_date
        return self._get(path, params)

    def airline_directions(self, airline_code, limit=10):
        """
        Returns popular routes for a given airline.
        (Wraps /v1/airline-directions)

        :param airline_code: IATA code of the airline.
        :param limit: Number of routes to return.
        """
        path = "/v1/airline-directions"
        params = {
            "airline_code": airline_code,
            "limit": limit
        }
        return self._get(path, params)

    def city_directions(self, origin, currency=None):
        """
        Returns the most popular destinations from a specified city.
        (Wraps /v1/city-directions)

        :param origin: IATA code of the departure city.
        :param currency: Optional currency override.
        """
        path = "/v1/city-directions"
        params = {"origin": origin}
        if currency:
            params["currency"] = currency
        return self._get(path, params)

    def popular_directions(self, destination, locale="en", currency=None, limit=30, page=1):
        """
        Returns the cheapest tickets to popular destinations.
        (Wraps /v3/get_popular_directions)

        :param destination: IATA code of the destination city.
        :param locale: Language of the results.
        :param currency: Optional currency override.
        :param limit: Number of results per page.
        :param page: Page number.
        """
        path = "/v3/get_popular_directions"
        params = {
            "destination": destination,
            "locale": locale,
            "limit": limit,
            "page": page
        }
        if currency:
            params["currency"] = currency
        return self._get(path, params)

    def special_offers(self, origin=None, destination=None, locale="en", airline=None):
        """
        Returns flights special offers.
        (Wraps /aviasales/v3/get_special_offers)

        :param origin: Optional IATA code of departure.
        :param destination: Optional IATA code of destination.
        :param locale: Language for the result.
        :param airline: Optional IATA code of the airline.
        """
        path = "/aviasales/v3/get_special_offers"
        params = {"locale": locale}
        if origin:
            params["origin"] = origin
        if destination:
            params["destination"] = destination
        if airline:
            params["airline"] = airline
        return self._get(path, params)

    def currency_rates(self):
        """
        Returns the current exchange rates to RUB.
        (Uses the currency adaptor endpoint.)
        """
        url = "http://yasen.aviasales.com/adaptors/currency.json"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def airline_logo(self, iata, width=200, height=200):
        """
        Returns the URL of the airline's logo.
        (Constructs URL from http://pics.avs.io)
        
        :param iata: IATA code of the airline.
        :param width: Width of the logo image.
        :param height: Height of the logo image.
        """
        return f"http://pics.avs.io/{width}/{height}/{iata}.png"

# Example usage:
if __name__ == "__main__":
    load_dotenv()
    API_TOKEN = os.getenv("AVIASALES_API_KEY")  # Replace with your token
    currency = "EUR"
    origin="OSL"
    destination="ALC"

    api = AviasalesAPI(API_TOKEN, currency=currency, market="eu")
    
    try:
        # Example: Get airline logo URL.
        # logo_url = api.airline_logo("UN")
        # print("Airline logo URL:", logo_url)
        
        # Example: Get month matrix.
        # month_matrix = api.prices_month_matrix("BCN", "HKT", "2025-10-01")
        # print("Month matrix:")
        # print(month_matrix)
        
        # Example: Get prices for specific dates.
        # data = api.prices_for_dates("MAD", "BCN", "2025-07", "2025-08", one_way=True)
        # print("Prices for dates:")
        # print(data)
        
        # Example: Get latest prices for a period.
        data = api.get_latest_prices(origin, destination, "2025-12-07", "year", one_way=True)
        
        # Define the column widths for the table
        col_widths = [7, 12, 20, 20, 12, 10]

        # Print the header
        headers = ["Origin", "Destination", "Departure", "Arrival", "Provider", "Price"]
        print(f"{headers[0]:<{col_widths[0]}}{headers[1]:<{col_widths[1]}}{headers[2]:<{col_widths[2]}}{headers[3]:<{col_widths[3]}}{headers[4]:<{col_widths[4]}}{headers[5]:<{col_widths[5]}}")

        # Print a separator
        print("-" * sum(col_widths))

        # Loop through the flight data and print each row
        for flight in data['data']:
            depart_time = datetime.fromisoformat(flight['depart_date'])
            arrival_time = depart_time + timedelta(minutes=flight['duration'])
            
            # Format each flight's data into columns
            print(f"{flight['origin']:<{col_widths[0]}}"
                  f"{flight['destination']:<{col_widths[1]}}"
                  f"{depart_time.strftime('%Y-%m-%d %H:%M'):<{col_widths[2]}}"
                  f"{arrival_time.strftime('%Y-%m-%d %H:%M'):<{col_widths[3]}}"
                  f"{flight['gate']:<{col_widths[4]}}"
                  f"${flight['value']:<{col_widths[5]}}")

        # Example: Get special offers.
        data = api.special_offers(origin=origin, destination=destination)
        print("Special offers:")
        
        # Define column widths for table
        col_widths = [12, 12, 15, 15, 12, 10, 10]

        # Print the header
        headers = ["Airline", "Flight No.", "Origin", "Destination", "Departure", "Duration", "Price (€)"]
        print(f"{headers[0]:<{col_widths[0]}}{headers[1]:<{col_widths[1]}}{headers[2]:<{col_widths[2]}}{headers[3]:<{col_widths[3]}}{headers[4]:<{col_widths[4]}}{headers[5]:<{col_widths[5]}}{headers[6]:<{col_widths[6]}}")

        # Print a separator
        print("-" * sum(col_widths))

        # Loop through the flight data and print each row
        for flight in data['data']:
            depart_time = datetime.fromisoformat(flight['departure_at'])
            
            # Format each flight's data into columns
            print(f"{flight['airline_title']:<{col_widths[0]}}"
                  f"{flight['flight_number']:<{col_widths[1]}}"
                  f"{flight['origin_name']:<{col_widths[2]}}"
                  f"{flight['destination_name']:<{col_widths[3]}}"
                  f"{depart_time.strftime('%Y-%m-%d %H:%M'):<{col_widths[4]}}"
                  f"{flight['duration']:<{col_widths[5]}}"
                  f"{flight['price']:<{col_widths[6]}}")
        
    except requests.HTTPError as e:
        print("HTTP error occurred:", e)
    except Exception as e:
        print("An error occurred:", e)
