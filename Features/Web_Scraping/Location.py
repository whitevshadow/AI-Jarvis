import bs4
import requests
from geopy import Nominatim
from Body.Speaker import Speak


def My_Location():
    Speak("Getting Your Location Sir")
    google_search = requests.get('https://www.google.com/search?q=Google')
    soup = bs4.BeautifulSoup(google_search.text, 'html.parser')
    search_results = soup.select('.dfB0uf')
    result = str(search_results)
    addressNow = result.replace('[<span class="dfB0uf">', '').replace('</span>]', '')
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(addressNow)
    latitude = str(getLoc.latitude)
    longitude = str(getLoc.longitude)
    Address = f'''Sir , You Are Now In {getLoc.address} .
                  Latitude = {latitude}
                  Longitude =  {longitude}'''
    return Address


