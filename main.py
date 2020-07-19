import json
from weather_scrape import WebScraper
from email_sender import EmailSender
import pandas as pd

# create writer for creating colored excel file
writer = pd.ExcelWriter('output.xlsx')

# initialize classes
ws = WebScraper()
es = EmailSender()

# open login files for email sending
with open("pkg/login.json", "r") as lg:
    LG = json.load(lg)

# create dataframe with temperature, days and rain
df = ws.scrape()

# create threshholds for good weather
index_label_temp = set(df[df['temp']>=20].index.tolist())
index_label_rain = df[df['rain']<=5].index.tolist()

index = list(index_label_temp.intersection(index_label_rain))

# define color coding
def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'green' if val <= 0.05 or val >= 18 else 'red'
    return 'background-color: %s' % color

def color_blue(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'blue'
    #color = 'blue' if val == 'Heute' or val == 'Morgen' or val == 'Übermorgen' else 'lightblue'
    return 'background-color: %s' % color


# color entries when weather is good
df = df.style.applymap(color_negative_red,
                  subset=pd.IndexSlice[index, ['temp', 'rain']])

# mark the days
df = df.applymap(color_blue,
                      subset=pd.IndexSlice[[0, 5, 10], ['daytime', 'temp', 'rain']])

# save the file as excel sheet (colored)
df.to_excel(writer, 'sheet1')
writer.save()

# send email when weather is good, otherwise not
if (not index)==False:
    es.send(file="C:/Users/anton/Desktop/weather_search/output.xlsx")
else:
    print('bad weather')