import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def get_politician_bday(page_url):
    # print(page_url)
    # response = requests.get(page_url, timeout=10) #10 seconds to read
    response = requests.get(page_url)
    if response == None:
        print("errererer")
        print(page_url)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    infobox = soup.find('table', {'class': 'infobox'})
    if not infobox:
        return None
    for row in infobox.find_all('tr'):
        header = row.find('th')
        if header and 'Born' in header.text:
            # bday = row.find('span', {'class': 'bday'}).text.strip()
            # bday = header.find('td').text.strip()
            # print(bday)
            # print(row.find("td").text)
            bday_text = ''.join([str(content) for content in row.find("td").contents if isinstance(content, str)])
            bday = process_unformatted_bday_text(bday_text.strip(), page_url)
            # print(bday)
            if (is_valid_date(bday) == False):
                if page_url == "https://en.wikipedia.org/wiki/Thomson_J._Skinner":
                    return "May 24, 1752"
                elif page_url == "https://en.wikipedia.org/wiki/William_Cabell_Rives":
                    return "May 4, 1793"
                else:
                    print("Invalid Date for: " + page_url) 
                    print("\t" + bday_text)
                    if bday != None:
                        print("\t" + bday)
                    else:
                        print("\tNone")
            # print("\t" + bday)

        # if header and 'Political party' in header.text:
        #     party = row.findNext('td').text.strip()
        #     return party
    return None




def process_unformatted_bday_text(bday_text, page_url):
    if bday_text in ["", ",", "unknown", "Unknown", ", or now  (then )"]:
        return None
    bday_list = bday_text.split(" ")
    bday_list = [val.split(',')[0] for val in bday_list if val != ','] #remove possible commas
    if len(bday_list) == 0:
        return None

    month, day, year = None, None, None
    months_list = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]


    if bday_list[0] in ["c.", "ca."]: #got approxiamate year: "c. [year]" or "ca. [year]"
        # print("here")
        year = bday_list[1]
        return "January 1, " + year


    if bday_list[0] in months_list:  #first value is the month
        month = bday_list[0] #remove possible commas if "month, year format"
        if (len(bday_list[1]) in (1,2)): #second value is day
            day = bday_list[1] + ", "
            year = bday_list[2][:4]
        else: #likey has "month, year format"; will set default day to "1st" of month
            month = bday_list[0]
            year = bday_list[1][:4]
            day = "1, "
    #check for "day month year" or "year month day" 
    elif len(bday_list) >= 3 and bday_list[1] in months_list:
        month = bday_list[1]
        #check for "day month year"
        if bday_list[0].isnumeric() and len(str(bday_list[0])) <= 2 and bday_list[2].isnumeric() and len(str(bday_list[2])) == 4:
            day = bday_list[0] + ", "
            year =  bday_list[2][:4]
        #check for "year month day" 
        elif bday_list[0].isnumeric() and len(str(bday_list[0])) == 4 and bday_list[2].isnumeric() and len(str(bday_list[2])) <= 2:
            year = bday_list[0][:4]
            day =  bday_list[2] + ", "
        else:
            return None
    else:
        if bday_list[0][:4].isnumeric() == False:
            return None
        #likely has just a "year" for the bday date; set month and day to "January" and "1st"
        year = bday_list[0][:4]
        month = "January"
        day = "1, "
    return " ".join([month, day, year])


def is_valid_date(date_string, date_format="%B %d, %Y"):
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False
    except TypeError:
        return False





# https://en.wikipedia.org/wiki/William_Smith_(South_Carolina_senator)

# get_politician_bday("https://en.wikipedia.org/wiki/William_Smith_(South_Carolina_senator)")

# page_url = "https://en.wikipedia.org/wiki/Kevin_McCarthy"
# response = requests.get(page_url)
# soup = BeautifulSoup(response.content, 'html.parser')
# a = get_politician_data(page_url)
# print(a)