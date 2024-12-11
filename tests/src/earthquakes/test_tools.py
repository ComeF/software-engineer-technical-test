from earthquakes.tools import get_haversine_distance
import numpy as np
import pytest

@pytest.mark.parametrize("lat1, lon1, lat2, lon2, expected",
        [
            (52.2296756, 21.0122287, 52.2296756, 21.0122287, 0), #Warsaw to Warsaw
            (52.2296756, 21.0122287, 41.8919300, 12.5113300, 1316.96), #Warsaw to Rome
            (52.2296756, 21.0122287, 40.712776, -74.005974, 6854.21), #Warsaw to New York
            (52.2296756, 21.0122287, 35.6762, 139.6503, 8577.74), #Warsaw to Tokyo
            (41.8919300, 12.5113300, 40.712776, -74.005974, 6899.19), #Rome to New York
            (41.8919300, 12.5113300, 35.6762, 139.6503, 9863.32), #Rome to Tokyo
            (40.712776, -74.005974, 35.6762, 139.6503, 10863.66) #New York to Tokyo
        ]
)
def test_haversine(lat1, lon1, lat2, lon2, expected):
    distance = get_haversine_distance(lat1, lon1, lat2, lon2)
    np.testing.assert_allclose(distance, expected, atol=1e-2)


def test_haversine():
    distance = get_haversine_distance(52.2296756, 21.0122287, 52.2296756, 21.0122287)
    np.testing.assert_allclose(distance, 0, atol=1e-2)