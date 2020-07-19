import json
import pandas as pd
import webbot
import time
import bs4


class WebScraper:
    """
    WebScraper
    """

    def __init__(self):
        self.url = "https://www.wetter.com/wetter_aktuell/wettervorhersage/3_tagesvorhersage/deutschland/goettingen/DE0003197.html"
        self.web = webbot.Browser()
        self.web.go_to(self.url)
        self.delay = 3
        time.sleep(self.delay)
        self.web.click("EINWILLIGEN")


    def scrape(self):
        page = self.web.get_page_source()
        soup = bs4.BeautifulSoup(page, features='html.parser')
        rains = soup.find_all('div', {'class': 'swg-col-wv1 swg-row'})
        daytime = soup.find_all('div', {'class': 'swg-col-period swg-row'})
        daytime_temp = soup.find_all('span', {'class': 'swg-text-large'})

        daytime_list = []


        for d, dt, r in zip(daytime, daytime_temp, rains):
            daytime = d.text.strip()
            time_temp = dt.text.strip()
            rain = r.text.strip()

            time_temp = time_temp.split('°')[0].strip()
            rain = int(rain.strip("%\n "))
            time_dict = {'daytime': daytime, 'temp': time_temp, 'rain': rain}
            daytime_list.append(time_dict)

        df = pd.DataFrame(daytime_list)
        df['temp'] = df['temp'].astype(int)

        return df

if __name__ == "__main__":
    ws = WebScraper()

    df = ws.scrape()
