import schedule
import time
import requests
from bs4 import BeautifulSoup as bs
from win10toast import ToastNotifier as tn

n = tn()

def getdata(url):
    r = requests.get(url)
    return r.text

weather_url = "https://weather.com/"

def getweather():
    #beautiful soup variables
    html_data = getdata(weather_url)
    soup = bs(html_data, 'lxml')
    weather_today_card = soup.find('section', {'data-testid' : 'TodaysDetailsModule'})

    #weather variables
    feels_like = weather_today_card.findChild('span', {'data-testid' : 'TemperatureValue'}).text
    chance_rain = soup.find('span', class_="Column--precip--2ck8J").text
    temps = weather_today_card.findChild('div', class_="WeatherDetailsListItem--wxData--2s6HT")
    temp_high = temps.findChild('span') #using this as a reference for temp_low, will print the .text at the print statement
    temp_low = temp_high.find_next_sibling().text
    humidity = weather_today_card.findChild('div', class_="WeatherDetailsListItem--wxData--2s6HT").findChild('span').text
    sunrise = weather_today_card.findChild('div', class_="SunriseSunset--sunriseDateItem--3qqf7").findChild('p', class_="SunriseSunset--dateValue--N2p5B").text
    sunset = weather_today_card.findChild('div', class_="SunriseSunset--sunsetDateItem--34dPe SunriseSunset--sunriseDateItem--3qqf7").findChild('p', class_="SunriseSunset--dateValue--N2p5B").text

    #function
    result = "Current temp: Feels like "+feels_like+"\nChance of rain: "+chance_rain+"\nToday's high: "+temp_high.text+"\nToday's low: "+temp_low+"\nToday's humidity: "+humidity+"\nSunrise: "+sunrise+"\nSunset: "+sunset
    n.show_toast("Weather Update", result, duration=20) #sunset and sunrise don't make the cutoff for the notification. can't find the docs on win10toast
    return

schedule.every(60).minutes.do(getweather)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)

