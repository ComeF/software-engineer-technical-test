from earthquakes.usgs_api import build_api_url

def test_api_response():
    assert build_api_url(method = "version").getcode() == 200