import twint
from geopy.geocoders import Nominatim
geo_locator = Nominatim(user_agent="socom_geo")

def search_twint(query, date_since, date_until, limit, type):
    date_since_str = date_since.strftime('%Y-%m-%d')
    date_until_str = date_until.strftime('%Y-%m-%d')
    c = twint.Config()
    c.Limit = limit
    c.Lang = "en"
    # c.Location = True
    c.Since = date_since_str
    c.Until = date_until_str
    c.Hide_output = True
    c.Store_csv = True

    if type == "country":
        c.Search = query
        c.Custom["tweet"] = ["id", "tweet", "place", "geo", "date", "created_at"]
        c.Filter_retweets = True
        search_twint_country(c, date_since_str, date_until_str)
    elif type == "account":
        c.Custom["tweet"] = ["id", "name", "tweet", "date", "created_at"]
        c.Filter_retweets = False
        search_twint_account(c, date_since_str, date_until_str)


def search_twint_country(config, date_since_str, date_until_str):
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
        config.Geo = "{},{}km".format(countries[country]["geocode"], countries[country]["radius_km"])
        config.Output = "country_{}_{}_{}.csv".format(date_since_str, date_until_str, country.upper())
        twint.run.Search(config)


def search_twint_account(config, date_since_str, date_until_str):

    accounts = [
        "airqualityindia",
        "DelhiBreathe",
        "MRTB_India",
        "moefcc",
        "icareforlungs",
        "ChintanIndia",
        "CSEINDIA",
        "down2earthindia",
        "MongabayIndia",
        "Letssavedelhi",
    ]

    for account in accounts:
        config.Username = account
        config.Output = "account_{}_{}_{}.csv".format(date_since_str, date_until_str, account)
        twint.run.Search(config)


def get_geocode_country(country_code, km):
    loc = geo_locator.geocode(country_code)
    return "{},{},{}km".format(loc.latitude, loc.longitude, km)
