import twint
from geopy.geocoders import Nominatim
geo_locator = Nominatim(user_agent="socom_geo")


def search_twint(query, date_since, date_until, limit):
    date_since_str = date_since.strftime('%Y-%m-%d')
    date_until_str = date_until.strftime('%Y-%m-%d')
    c = twint.Config()
    c.Search = query
    c.Custom["tweet"] = ["id", "tweet", "place", "geo", "date", "created_at"]
    c.Limit = limit
    c.Lang = "en"
    # c.Location = True
    c.Since = date_since_str
    c.Until = date_until_str
    c.Filter_retweets = True
    c.Hide_output = True
    c.Store_csv = True

    # https://www.mapdevelopers.com/draw-circle-tool.php
    countries = {
        "us": {
            "radius_km": 2500,
            "geocode": "39.783730,-100.445882"
        },
        "gb": {
            "radius_km": 500,
            "geocode": "54.702354,-3.276575"
        },
        "in": {
            "radius_km": 1500,
            "geocode": "22.351115,78.667743"
        }
    }

    for country in countries:
        # c.Geo = get_geocode_country(country, countries[country]["radius_km"])
        c.Geo = "{},{}km".format(countries[country]["geocode"], countries[country]["radius_km"])
        c.Output = "{}_{}_{}.csv".format(date_since_str, date_until_str, country.upper())
        twint.run.Search(c)


def get_geocode_country(country_code, km):
    loc = geo_locator.geocode(country_code)
    return "{},{},{}km".format(loc.latitude, loc.longitude, km)
