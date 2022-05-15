from datetime import datetime
import requests
import csv
from twilio.rest import Client
import pandas as pd


# Twilio Authentication
ACCOUNT_SID = 'AC911f113cfcd849f9d099a5136a2d83eb'
AUTH_TOKEN = 'ffae61ef343c66b3f79dd245b930beb7'
client = Client(ACCOUNT_SID, AUTH_TOKEN)


# Every day at 8:00 AM, Send SMS Message to Phone with Current Updated CDC Information
today = datetime.today()
now = datetime.now()


current_date = today.strftime('%A, %B %d, %Y')
current_time = now.strftime("%H:%M")
test_case = True
if test_case == True:
# if current_time == '08:00':


    # Covid Database API
    county_request = requests.get('https://api.covidactnow.org/v2/county/06085.json?apiKey=c8275ae6f8074670ab819ba7937aa71a')
    county_data = county_request.json()


    # Gathering Data from API
    daily_cases = round(county_data['metrics']['weeklyNewCasesPer100k'])
    vaccinated = "{:.0%}".format(county_data['metrics']['vaccinationsCompletedRatio'])
    booster_shot = "{:.0%}".format(county_data['metrics']['vaccinationsAdditionalDoseRatio'])
    unvaccinated_population = county_data['population'] - county_data['actuals']['vaccinationsCompleted']
    unvaccinated = "{:.0%}".format(unvaccinated_population / county_data['population'])
    TodayDate = county_data['lastUpdatedDate']


    # Determine Risk Level of County
    if daily_cases < 200:
        riskLevel = 'Low 🟢'
        riskDesc = 'Covid Case Rates have remained at an alltime low, and masks are not mandatory. All social events such as ' \
               'bars, restaurants, and other indoor social gatherings will remain open. Masking is optional, but encouraged ' \
               'to practice safety.'
    elif 200 < daily_cases < 549:
        riskLevel = 'Medium 🟡'
        riskDesc = 'Covid Case Rates have become more common, but not at a dangerous level. While the mask mandate is optional, county ' \
               'residents are encouraged to mask up when going out in public. All social events such as bars, restaurants, and other ' \
               'indoor social gatherings will remain open. However, if cases continue to rise, then these events may be shut down.'
    else:
        riskLevel = 'High 🔴'
        riskDesc = 'Covid Case Rates are at an all time high, and masks are mandatory. All social events, bars, restaurants, ' \
               'and other indoor social gathering are to be discontinued until cases are reduced. Furthermore, all businesses ' \
               'that are do not provide governmental, or food, services are to be shutdown effective immediately. Employees are now required to work from home, ' \
               'until further notice.'


    # CSV file that Contains Past Dates and their Data to Compare against Most Recent.
    with open('history.csv', 'a') as File:
        writer = csv.writer(File)
        writer.writerow([TodayDate, daily_cases])
        File.close()


    # Open the same CSV file from earlier, but instead of adding onto it, we're going to read it.
    with open('history.csv', 'r') as File:
        csvreader = csv.reader(File)
        header = next(csvreader)
        rows = []
        for row in csvreader:
            rows.append(row)
        print(rows)
        File.close()


    # Showcase if Cases have Risen or Dropped since Yesterday
    yesterday_cases = 232
    difference = abs(daily_cases - yesterday_cases)
    up_down = None
    caseDiff = None
    if daily_cases > yesterday_cases:
        up_down = '🔺'
        caseDiff = f'(+{difference} from yesterday)'
    elif daily_cases < yesterday_cases:
        up_down = '🔻'
        caseDiff = f'(-{difference} from yesterday)'
    else:
        up_down = ''
        caseDiff = f'County Covid Cases have remained at the same number since yesterday.'


    # SMS Text Format
    text_message = [f'.\n\nSanta Clara County \nCOVID Update \n{current_date}\n\n----------------------------'
                    f'\n\nRisk Level: \n\n{riskLevel}\n\nActive Cases: \n\n{daily_cases}{up_down} {caseDiff}\n\n----------------------------'
                    f'\n\nCounty Statistics: \n\nUnvaccinated: {unvaccinated} \nFully Vaccinated: {vaccinated} \nBooster Shot: {booster_shot}\n\n----------------------------'
                    f'\n\nCounty Message to Residents: \n\n{riskDesc}']


    # Send Covid Tracker SMS
    message = client.messages.create(
        body= text_message,
        from_= '+19035322609',
        to= "MY NUMBER"
    )


else:
    pass
