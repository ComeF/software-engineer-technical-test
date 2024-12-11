from urllib.parse import urlencode, urljoin
from urllib.request import urlopen
import pandas as pd
from io import StringIO
from datetime import datetime
import asyncio

def get_earthquake_data(latitude = 0,
                        longitude = 0,
                        radius = 1,
                        minimum_magnitude = 1,
                        end_date=datetime(year=2021, month=10, day=21)):
    """
    Function takes a number of parameter regarding the location, radius, magnitude and time of the desired earthquake data, and return a pandas dataframe containing said data.

    Inputs:
        latitude: float
        longitude: float
        radius: float
        minimum_magnitude: float
        end_date: datetime.datetime
    
    Output:
        data: pandas.core.frame.DataFrame
    """
    query_params = {
        "format" : "csv",
        "latitude": latitude,
        "longitude": longitude,
        "maxradiuskm": radius,
        "minmagnitude": minimum_magnitude,
        "endtime": end_date.isoformat(),
        "starttime": "1821-10-21"
    }
    raw_data = StringIO(build_api_url(query_params = query_params).read().decode('utf-8'))
    return pd.read_csv(raw_data)





def build_api_url(query_params = {}, method = "query"):
    """
    Function takes a parameter dic, and a method, and return the html request associated with desired parameters. Method is left as a kwarg for testing purpose

    Inputs:
        query_params: dict
        method: str
    Output:
        response: http.client.HTTPResponse
    """
    base_url = f"https://earthquake.usgs.gov/fdsnws/event/1/{method}"

    encoded_params = urlencode(query_params)
    full_url = urljoin(base_url, "?" + encoded_params)

    # Send the GET request
    return urlopen(full_url)


async def get_earthquake_data_wrapper(**kwargs):
    """
    Wrapper for concurrent call of get_earthquake. Private function
    """
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, get_earthquake_data, *tuple(kwargs.values()))
    return result


async def get_earthquake_data_for_multiple_locations(assets, **kwargs):
    """
    Function concurrently runs directly get_earthquake_data on each asset.
    Input
        asset: list of tuple (latitude, longitude)
        radius: float
        minimum_magnitude: float
        end_date: datetime.datetime
    
    Output:
        data: pandas.core.frame.DataFrame
    """
    results = await asyncio.gather(*(get_earthquake_data_wrapper(latitude = asset[0],
                                                                longitude = asset[1],
                                                                **kwargs) for asset in assets))
    return pd.concat(results)
