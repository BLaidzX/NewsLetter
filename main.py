import csv
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import pytz
import time
# from datetime
import datetime

import smtplib
from email.message import EmailMessage
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

import os

scopes = ['https://www.googleapis.com/auth/calendar.readonly']
crypto = ("https://coinmarketcap.com/")
base_url = "https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVWRDR2dKSlRDZ0FQAQ?hl=en-IL&gl=IL&ceid=IL%3Aen"
url2 = ("https://www.bbc.com/sport/football")
BBC_news = ("https://www.bbc.com/news")
BBC_xml = ("http://feeds.bbci.co.uk/news/rss.xml")
Football = ("https://www.bbc.com/sport/football/scores-fixtures/")
today = datetime.datetime.now()
today = today.strftime("%Y-%m-%d")
today_datetime = datetime.datetime.strptime(today, "%Y-%m-%d")
yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
yesterday = yesterday.strftime("%Y-%m-%d")
file = open('output.html', 'w', encoding="utf-8")


def get_soup(url):
    if "xml" in url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, features=("xml"))
    else:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
    return soup



# def authenticate_google():
#     creds = None
#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes=scopes)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)
#
#     service = build('calendar', 'v3', credentials=creds)
#     return service
#
#
# def get_events(day, service):
#     date = datetime.datetime.combine(day, datetime.datetime.min.time())
#     end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
#     utc = pytz.UTC
#     date = date.astimezone(utc)
#     end_date = end_date.astimezone(utc)
#     events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
#                                           singleEvents=True, orderBy='startTime').execute()
#     if events_result is not None:
#         events = events_result.get('items', [])
#         if not events:
#             file.write(f'''<div class="line"></div>
#                                           <div class="two-col">
#                                                <h2> You No events today.</h2>''')
#         else:
#             file.write(f'''<div class="line"></div>
#                                           <div class="two-col">
#                                                <h2>You have {len(events)} events today.</h2>''')
#
#         for event in events:
#             start = event['start'].get('dateTime', event['start'].get('date'))
#             start_time = "{:02d}".format(int(start.split("T")[1].split("-")[0].split(":")[0]) - 12) + ":" + \
#                          start.split("T")[1].split("-")[0].split(":")[1]
#             if int(start_time.split(":")[0]) < 12:
#                 start_time = start_time + "am"
#             else:
#                 start_time = "{:02d}".format(int(start_time.split(":")[0]) - 12) + ":" + start_time.split(":")[1]
#                 start_time = start_time + "pm"
#
#
#             file.write(f'''<ul><li>{event['summary']} at {start_time}</li></ul>''')

def get_headlines(item_start_id, links_to_fetch):
    current_item = item_start_id
    soup = get_soup(BBC_xml)
    articles = soup.find_all('item')
    stories = []
    for item in range(links_to_fetch):
        articleurl = articles[item].link.text
        articleheadline = articles[item].title.text
        # Append a tuple of the article title and URL to the stories list
        stories.append((articleheadline, articleurl))
        current_item += 1

    # Use a list comprehension to filter the stories list to only include articles posted within the past 24 hours
    stories_posted_u24 = [story for story in stories if get_time_of_posting_bbc(story[1])]
    file.write('''<div class="line"></div>
                  <div class="two-col">
                       <h2>Every BBC news article Released in the past 24 hours</h2>''')
    for story in stories_posted_u24:
        file.write(f"<ul><li><a href={story[1]}>{story[0]}</a></li></ul>")
    # print(stories_posted_u24)
    # print(len(stories_posted_u24))


def get_time_of_posting_bbc(article_url):
    try:
        # Attempt to fetch the content of the URL
        soup = get_soup(article_url)
    except requests.exceptions.RequestException as e:
        # An exception will be raised if the URL is invalid or the request fails
        print(f"An error occurred while trying to fetch the URL: {e}")
        return False
    try:
        time_article = soup.find('time')
        #print(time_article)
        if time_article is not None:
            result = re.sub(r'[-+:a-zA-Z]', '', time_article['datetime'])
            #print(result)
            result = result[:-4]
            date = datetime.datetime.strptime(result, '%Y%m%d%H%M%S')
            seconds_of_time_since_posting = date.timestamp()
            current_time = time.time()
            if current_time - seconds_of_time_since_posting < 86400:
                return True
            else:
                return False
            #print(result)
    except ValueError:
        time_article1 = soup.find('time',class_='gs-o-bullet__text qa-status-date gs-u-align-middle gs-u-display-inline')
        # print(time_article)
        if time_article is not None:
            result = re.sub(r'[-+:a-zA-Z]', '', time_article1['datetime'])
            result = result[:-4]
            date = datetime.datetime.strptime(result, '%Y%m%d%H%M%S')
            seconds_of_time_since_posting = date.timestamp()
            current_time = time.time()
            if current_time - seconds_of_time_since_posting < 86400:
                return True
            else:
                return False






def scrape_links(base_url, limit=20, file=None):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a", class_="WwrzSb")
    titles = soup.find_all("h4", class_="JtKRv")
    counter = 0

    file.write("<ul>\n")  # Start the unordered list
    file.write('<div class="line"></div>\n')
    file.write('<div class="two-col">\n')
    file.write('<h2>Tech News & Stories</h2>\n')

    for link, title in zip(links, titles):
        counter += 1
        href = link.get("href")
        if href.startswith("./"):
            href = href[2:]  # Remove the './' at the beginning of the link
        complete_url = urljoin("https://news.google.com/", href)
        link_title = title.get_text(strip=True)

        file.write(f"<li><a href='{complete_url}'>{link_title}</a></li>\n")  # Write link and title as a list item

        if counter == limit:
            break

    file.write('</div>\n')
    file.write("</ul>\n")  # End the unordered list


def get_crypto():
    doc_for_crypto = get_soup(crypto)
    tbody = doc_for_crypto.tbody
    trs = tbody.contents
    prices = {}
    for tr in trs[:10]:
        name, price = tr.contents[2:4]
        fixed_name = name.p.string
        fixed_price = price.a.string
        prices[fixed_name] = fixed_price
    df = pd.DataFrame(prices.items(), columns=['Name', 'Price'])
    df = df.to_html()
    info = doc_for_crypto.find(class_="sc-aef7b723-0 EPENP")
    text = []
    for tag in info:
        test_str = tag.text.strip()
        result = test_str.replace("Read More", "")
        text.append(result)
    text_to_string = "".join(text)
    file.write(f'''
        <div class="line"></div>
            <h2>The Crypto Market</h2>
             <p>{text_to_string}</p>
             <p>{df}</p>
        <div class="line"></div>
             <h2>Football Fixtures</h2>''')


def swap_positions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]


def clean_data(list):
    prem_header = ">Premier League</h3>"
    EPL_header = ">English Premier League</h3>"
    prem_span = "$0Premier League"
    EPL_span = "$0English Premier League"

    for indx, item in enumerate(list):
        if prem_header in item:
            list[indx] = list[indx].replace(prem_header, EPL_header)
        elif prem_span in item:
            list[indx] = list[indx].replace(prem_span, EPL_span)
        else:
            item

    leagues = (['English Premier League', 'Spanish La Liga', 'German Bundesliga', 'Italian Serie A',
                'French Ligue 1', 'Champions League'])

    list = [i[-145:] for i in list]
    left, right = '">', '</'
    list = [[l[l.index(left) + len(left):l.index(right)] for l in list if i in l] for i in leagues]

    return list


def home_and_away(list):
    for i in list:
        while '' in i:
            swap_positions(i, i.index(''), i.index('') - 2)
            blank = i.index('')
            blank_2 = i.index('') + 2
            i[blank] = '(H)'
            i.insert(blank_2, '(A)')





def choose_date(day=today):
    date_to_look = day
    match = re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", date_to_look)
    year, month, day = (int(x) for x in date_to_look.split('-'))
    ans = datetime.date(year, month, day)
    date = datetime.datetime.strptime(date_to_look, "%Y-%m-%d")
    day_name = date.strftime("%A")
    day_date = date.strftime("%Y-%m-%d")
    file.write(f'''
                    <div class="two-col">
			             <h3>   Fixtures & Results for {day_name}, {day_date}:</h3>
                            <br>''')
    return str(date_to_look)


def scraping(day):
    url = Football + choose_date(day)

    # html_content = requests.get(url).text

    soup = get_soup(url)

    tags = ["span", "h3"]
    classes = (["gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc",
                "sp-c-fixture__status-wrapper qa-sp-fixture-status",
                'sp-c-fixture__number sp-c-fixture__number--time', "sp-c-fixture__number sp-c-fixture__number--home",
                "sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--ft",
                "sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--live-sport",
                "sp-c-fixture__number sp-c-fixture__number--away sp-c-fixture__number--live-sport",
                "sp-c-fixture__number sp-c-fixture__number--away sp-c-fixture__number--ft",
                'gel-minion sp-c-match-list-heading'])

    scraper = soup.find_all(tags, attrs={'class': classes})
    data = [str(l) for l in scraper]

    data = clean_data(data)
    home_and_away(data)

    data = [l for l in data if len(l) != 0]

    return data


def change_time(day):
    data = scraping(day)

    curr_time = time.localtime()
    curr_clock = time.strftime("%Y:%m:%d %H:%M:%S %Z %z", curr_time)

    IST = pytz.timezone('Asia/Amman')
    datetime_ist = datetime.datetime.now(IST)
    london = datetime_ist.strftime("%Y:%m:%d %H:%M:%S %Z %z")

    curr_hour, curr_min = curr_clock[-5:-2], curr_clock[14:16]
    lndn_hour, lndn_min = london[-5:-2], london[14:16]

    hour_diff = int(lndn_hour) - int(curr_hour)
    min_diff = int(lndn_min) - int(curr_min)

    if min_diff == 0:
        min_diff = str(min_diff) + '0'

    for k in data:
        for indx, item in enumerate(k):

            if ":" in item:

                if min_diff == '00':
                    val = str(int(item[:item.index(":")]) - hour_diff) + item[item.index(":"):]

                if min_diff != '00':
                    val = str(int(item[:item.index(":")]) - hour_diff) + ":" + str(
                        abs(min_diff) + int(item[item.index(":") + 1:]))

                if int(val[val.index(":") + 1:]) >= 60:
                    val = str(int(val[:val.index(":")]) + 1) + ":" + str(int(val[val.index(":") + 1:]) - 60)

                if int(val[:val.index(":")]) >= 24:
                    # If the new hours value is >= 24, subtract 24 from the hours and add a '+1' to the end
                    # to signify game is taking place the following day
                    val = "0" + str(int(item[:item.index(":")]) - 24) + ":" + str(
                        int(item[item.index(":") + 1:])) + " +1"

                if val[val.index(":") + 1:] == '0':
                    val = i + '0'

                try:
                    if int(val[val.index(":") + 1:]) < 10 and int(val[val.index(":") + 1:]) > 0:
                        colon = val.find(":")
                        val = val[:colon + 1] + '0' + val[colon + 1:]
                except ValueError:
                    k[indx] = val
                    continue
                k[indx] = val

    data = [[i.replace('&amp;', '&') for i in group] for group in data]  # Brighton & Hove Albion problem

    return data


def final_print(day):
    ct = 0
    league_in = 0
    h_team, h_score, a_team, a_score, time = 1, 2, 3, 4, 5

    data = change_time(day)

    no_games = all(len(l) == 0 for l in data)
    if (no_games):  # If all the lists are empty
        print('NO GAMES ON THIS DATE')
        file.write('NO GAMES ON THIS DATE')
        return

    for i in data:
        # print(i[0])
        # print('-')
        # file.write(i[0])
        file.write(f"<b>{i[0]}</b>")
        file.write('-')

        while ct < len(data[league_in][1:]) // 5:
            file.write(
                f'''<br><p>{i[h_team]:<25} {i[h_score]:^5} vs {i[a_team]:<25} {i[a_score]:^3} | {i[time]:>7}</p>''')

            ct += 1
            h_team += 5
            h_score += 5
            a_team += 5
            a_score += 5
            time += 5

        file.write(" ")
        league_in += 1
        ct, h_team, h_score, a_team, a_score, time = 0, 1, 2, 3, 4, 5



def write_footer():
    file.write('<p>Don\'t want to receive this Newsletter anymore? Unsubscribe by following this <a href="/unsubscribe" class="btn btn-danger">Unsubscribe page</a>.</p>')


def write_body():
    # Generate the email content for the specified city and name
    # Use the personalized heading in the email content
    get_headlines(1, 20)
    scrape_links(base_url, limit=20, file=file)
    get_crypto()
    final_print(day=today)
    final_print(day=yesterday)
    file.close()



write_body()













