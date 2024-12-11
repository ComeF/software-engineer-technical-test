from numpy import pi, cos, sin, atan2, sqrt
import pandas as pd

EARTH_RADIUS = 6378

TIME_COLUMN = "time"
PAYOUT_COLUMN = "payout"
MAGNITUDE_COLUMN = "mag"
DISTANCE_COLUMN = "distance"
LATITUDE_COLUMN = "latitude"
LONGITUDE_COLUMN = "longitude"


def get_haversine_distance(latitude_serie, longitude_serie, latitude_origin, longitude_origin):
    """
    This function returns a pandas series containing the distances in km of the points of coordinate (latitude_serie[i], longitude_serie[i]) from the origin, of coordinates(latitude_origin, longitude origin).
    
    Input
        latitude_serie: pandas.core.series.Series or array_like
        longitude_serie: pandas.core.series.Series or array_like
        latitude_origin: float
        longitude_origin: float

    Output
        distances: pandas.core.series.Series or array_like

    """

    a = (sin(to_rad(latitude_serie-latitude_origin)/2.)**2 + cos(to_rad(latitude_serie))*cos(to_rad(latitude_origin))*sin(to_rad(longitude_serie - longitude_origin)/2.)**2) 

    return 2*atan2(sqrt(a), sqrt(1.-a)) * EARTH_RADIUS

def to_rad(x):
    """
    Simple function to convert degrees to radians in a concise manner
    """
    return x*pi/180.




def compute_payouts(data, structure):
    """
    Compute payouts from a dataframe of earthquake, and a payout structure which is a function of row to apply to each row of the dataframe to determine payout. The output is a Serie indexed by year, mapping said year to due payout
    
    Input
        data: pandas.core.frame.Dataframe
        structure: function

    Output
        result: pandas.core.series.Series
    """
    temp_frame = pd.DataFrame({'year': data[TIME_COLUMN].str[:4].astype(int), 'value': data.apply(structure, axis = 1)})
    
    return temp_frame.groupby('year')['value'].max()

    

    
def compute_burning_cost(payouts, start_year = 'min', end_year = 'max'):
    """
    Use a payouts serie to compute a burning_cost between year {start_year} and {end_year}.
    
    Input
        payouts: pandas.core.series.Series
        start_year: int
        end_year: int

    Output
        result: float
    """
    if start_year == 'min':
        start_year = payouts.index[0]

    if end_year == 'max':
        end_year = payouts.index[1]

    loc_start_year = payouts.index.get_loc(payouts.index[payouts.index >= start_year].min()) # this ensures that the code works even if start and end dates are not in the years
    loc_end_year = payouts.index.get_loc(payouts.index[payouts.index <= end_year].max())

    return (payouts[loc_start_year:loc_end_year+1].sum())/float(end_year-start_year+1)
    
