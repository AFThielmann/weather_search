# weather_search

Simple web scraping for finding the perfect biking weather.

At the moment the temperature has to be 20° and the probability of rain <5%.

In the folder email_sender, there has to be a login.json file of the following format:  

{ "email_sender": "gmail account from which email is send", 
"email_recipient":"email recipient", 
"email_password": "password of gmail account" }

Allow gmail to be opened by python with this link: https://myaccount.google.com/lesssecureapps

If the conditions are true at any of the two following as well as the current day, an email will be send with an attach xlsx file that displays the weather and rain probability highlighted accordingly. 
