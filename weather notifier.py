from webbrowser import get
import schedule
import time
import requests
from bs4 import BeautifulSoup as bs
from win10toast import ToastNotifier as tn

weather_url = "https://wunderground.com/weather/us"
city = None
state = None
n = tn()

def get_data(url):
    global city
    global state
    if (city == None or state == None): city,state = search_city() #assigns city and state by user input only once per program run.
    full_url = url+state.lower()+'/'+city.replace(" ", "-").lower() #i.e "https://wunderground.com/weather/us/new york/new york city"
    r = requests.get(full_url)
    return r.text

def search_city():
    try:
        city, state = input("Please enter a city, followed by a state separated by a comma. i.e new york city, ny: ").split(',')
    except:
        print("Invalid input, please enter a city, followed by a state separated by a comma. i.e new york city, ny: ")
    return [city,state]

def get_weather():
    #beautiful soup variables
    html_data = get_data(weather_url) #grabs the desired web page
    soup = bs(html_data, 'lxml')
    f = open("html.txt","w", encoding="utf-8")
    f.write(soup.prettify())
    f.close()

    #weather variables
    temp = soup.find('div',{'class' : 'current-temp'}).text
    temp_high = soup.find('div', {'class' : 'hi-lo'}).findChild('span',{'class' : 'hi'}).text
    temp_low = soup.find('div', {'class' : 'hi-lo'}).findChild('span',{'class' : 'lo'}).text
    print(temp,temp_high,temp_low)
    feels_like = soup.find('div', {'class' : 'feels-like'}).findChild('span').text
    #chance_rain = soup.find({'div' : 'precipBarChart'}).findChild('svg').findChild('text', {'style' : 'fill'}).text
    #humidity = soup.find({'span' : 'test-false wu-unit wu-unit-humidity ng-star-inserted'}).findChild({'span' : 'wu-value wu-value-to'}).text

    #function
    #result = "Current temp: Feels like "+feels_like+"\nChance of rain: "+chance_rain+"\nToday's high: "+temp_high.text+"\nToday's low: "+temp_low+"\nToday's humidity: "+humidity
    result = "Current temp: "+temp+"\nToday's high: "+temp_high+"\nToday's low: "+temp_low
    n.show_toast("Weather Update", result, duration=20) #sunset and sunrise don't make the cutoff for the notification. can't find the docs on win10toast
    return

get_weather()
schedule.every(30).minutes.do(get_weather) #seems to be a bit broken, returns the same temp every time.

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)
