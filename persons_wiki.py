import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def get_politician_bday(page_url, congress_start_date=None):
    # response = requests.get(page_url, timeout=10) #10 seconds to read
    response = requests.get(page_url)
    if response == None:
        print(page_url)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    #return the first set of text that exceeds 100 characters; should be the summary section
    summary_text = next(p.get_text() for p in soup.find_all("p") if len(p.get_text()) > 100)
    summary_text = summary_text[:200] #get substring for faster processing and other issues



    months_list = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]

    full_dates_list = re.findall(r'\w+\s+\d{1,2},\s+\d{4}', summary_text)
    month_year_list = re.findall(r'\b\w+\s\d{4}\b', summary_text)
    month_year_list = [month_year for month_year in month_year_list if month_year.split()[0] in months_list]
    year_list = re.findall(r'\d{4}', summary_text)


    #make sure there is no overlap in the year_list and the other lists by checking indices
    month_year_index = [summary_text.find(month_year) for month_year in month_year_list]
    full_dates_index = [summary_text.find(full_date) for full_date in full_dates_list]
    year_list = [year for year in year_list if summary_text.find(year) not in month_year_index + full_dates_index]

    first_parenthesis_index = summary_text.find('(')
    closing_parenthesis_index = summary_text.find(')')
    en_dash_index =  summary_text.find('–')

    print(full_dates_list)
    print("fas")
    print(summary_text)
    print(re.findall(r'\w+\s+\d{1,2},\s+\d{4}', "(September 23, 1745 – September 24, 1815) "))

    matches = []
    #format: (born Month day, year)
    if (summary_text.find("born") != -1 and
        (first_parenthesis_index < summary_text.find("born") < closing_parenthesis_index)):
        matches += full_dates_list
        # print("(born Month day, year): " + page_url)

    #check for (month day, year – month day, year)
    elif (len(full_dates_list) >= 2 and
            (first_parenthesis_index < summary_text.find(full_dates_list[0])
            < en_dash_index < summary_text.find(full_dates_list[1]) < closing_parenthesis_index
            )
        ): 
        matches += full_dates_list
        # print("(month day, year – month day, year): " + page_url)


    #check for (month day, year – month year)
    elif (len(full_dates_list) == 1 and len(month_year_list) == 1 and
            (first_parenthesis_index < summary_text.find(full_dates_list[0])
            < en_dash_index < summary_text.find(month_year_list[0]) < closing_parenthesis_index
            )
          ):
        matches += month_year_list
        print("(month day, year – month year): " + page_url)
        print("from " + full_dates_list[0]
              + " to " + month_year_list[0])


    #check for (month year – month day, year)
    elif (len(month_year_list) == 1 and len(full_dates_list) == 1 and
            (first_parenthesis_index < summary_text.find(month_year_list[0])
            < en_dash_index < summary_text.find(full_dates_list[0]) < closing_parenthesis_index
            )
          ):
        matches += month_year_list
        print("(month year – month day, year): " + page_url)
        print("from " + month_year_list[0]
              + " to " + full_dates_list[0])
    
    #check for month year - month year
    elif (len(month_year_list) >= 2 and 
            (
                first_parenthesis_index < summary_text.find(month_year_list[0])
                < en_dash_index < summary_text.find(month_year_list[1]) < closing_parenthesis_index
            )
          ):
        matches += month_year_list
        print("(month year – month year): " + page_url)

    #check for (year – month day, year)
    elif (len(year_list) > 0 and len(full_dates_list) > 0 and
            (first_parenthesis_index < summary_text.find(year_list[0])
             < en_dash_index < summary_text.find(full_dates_list[0]) < closing_parenthesis_index)
            ):
        matches.append(year_list[0])
        print("(year – full date): " + page_url)

    #check for (year – month year)
    elif (len(year_list) > 0 and len(month_year_list) > 0 and
            (first_parenthesis_index < summary_text.find(year_list[0])
             < en_dash_index < len(month_year_list[0]))
            ):
        matches.append(year_list[0])
        print("(year – month year): " + page_url)


    #check for (year - year)
    elif (len(year_list) >= 2 and
           (first_parenthesis_index < summary_text.find(year_list[0]) 
            < en_dash_index < summary_text.find(year_list[1]) < closing_parenthesis_index) 
          ):
        matches += year_list[:2]
        print("(year – year): " + page_url)


    elif "unknown" in summary_text.lower():
        matches.append("")
        print("unknown: " + page_url)

    else: #assuming there is a parenthesis around a date; no word "born" though
        # Regular expression pattern to match "Month day, year" within parentheses

        if len(full_dates_list) > 0:
            possible_match = full_dates_list[0]
            index = summary_text.find(possible_match)
            if first_parenthesis_index < index < closing_parenthesis_index:
                matches.append(possible_match)
        matches.append("")
        print("full date without born" + page_url)
        print("match6: " +  str(matches))

 
    bday_text = matches[0].strip() if len(matches) > 0 else ""

    if page_url == "https://en.wikipedia.org/wiki/John_Vining": #(month day, year - month year)
        bday_text = "December 23, 1758"


    bday = process_unformatted_bday_text(bday_text.strip(), page_url)
    # print(str(matches) + ":\t" + bday)
    if (is_valid_date(bday) == False):
        if page_url == "https://en.wikipedia.org/wiki/Doug_Lamborn": #having "born" in name messes up function
            bday = "May 24, 1954"
        elif page_url == "https://en.wikipedia.org/wiki/John_Laurance": #a pair of parenthesis before dob for nickname
            bday = "January 1, 1750"

        else:
            print("Invalid Date for: " + page_url) 
            print("\t" + bday_text)
            if bday != None:
                print("\t" + bday)
            else:
                print("\tNone")


    age = None
    #do a last check; bday should be before congress start and min difference in years should be 25
    if congress_start_date != None:
        date_format = "%B %d, %Y"
        congress_start = datetime.strptime(congress_start_date, date_format)
        bday_date = datetime.strptime(bday, date_format)
        if bday_date > congress_start:
            print("Invalid BDay: After Congress Start")
            age = (congress_start - bday_date).days//365
            if age < 25:
                print("Invalid BDay:Under 25")
    return bday, age




def process_unformatted_bday_text(bday_text, page_url):
    if bday_text == "":
        return None
    bday_text = bday_text.replace('\xa0', ' ')  # Replace non-breaking space with a regular space
    bday_text = bday_text.replace('\u2009', ' ') # Replace non-breaking space with a regular space
    bday_list = bday_text.split(" ")
    bday_list = [val.split(',')[0] for val in bday_list if val != ','] #remove possible commas
    if len(bday_list) == 0:
        return None

    month, day, year = None, None, None
    months_list = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]



    if bday_list[0] in months_list:  #first value is the month
        month = bday_list[0] #remove possible commas if "month, year format"
        if (len(bday_list[1]) in (1,2)): #second value is day
            day = bday_list[1] + ","
            year = bday_list[2][:4]
        else: #likey has "month, year format"; will set default day to "1st" of month
            month = bday_list[0]
            year = bday_list[1][:4]
            day = "1,"
    #check for "day month year" or "year month day" 
    elif len(bday_list) >= 3 and bday_list[1] in months_list:
        month = bday_list[1]
        #check for "day month year"
        if bday_list[0].isnumeric() and len(str(bday_list[0])) <= 2 and bday_list[2].isnumeric() and len(str(bday_list[2])) == 4:
            day = bday_list[0] + ","
            year =  bday_list[2][:4]
        #check for "year month day" 
        elif bday_list[0].isnumeric() and len(str(bday_list[0])) == 4 and bday_list[2].isnumeric() and len(str(bday_list[2])) <= 2:
            year = bday_list[0][:4]
            day =  bday_list[2] + ","
        else:
            return None
    else:
        if bday_list[0][:4].isnumeric() == False:
            return None
        #likely has just a "year" for the bday date; set month and day to "January" and "1st"
        year = bday_list[0][:4]
        month = "January"
        day = "1,"
    return " ".join([month, day, year])


def is_valid_date(date_string, date_format="%B %d, %Y"):
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False
    except TypeError:
        return False




# print(get_politician_bday("https://en.wikipedia.org/wiki/Oliver_Ellsworth")) #full date to full date
# get_politician_bday("https://en.wikipedia.org/wiki/William_Smith_(South_Carolina_senator)") #has "c. [year]"
# print(get_politician_bday("https://en.wikipedia.org/wiki/John_Vining")) #has full date to month year
# get_politician_bday("https://en.wikipedia.org/wiki/John_Henry_(Maryland_politician)") #has "month year to full date"
# get_politician_bday("https://en.wikipedia.org/wiki/Cornelius_C._Schoonmaker") #month year - month year
# print(get_politician_bday("https://en.wikipedia.org/wiki/Andrew_Moore_(politician)"))#year - full date
# get_politician_bday("https://en.wikipedia.org/wiki/John_Edwards_(Kentucky_politician)") # year - year

# https://en.wikipedia.org/wiki/Philip_Schuyler  #has a hyphen instead of en-dash; still works
page_url = "https://en.wikipedia.org/wiki/John_Sevier"
# response = requests.get(page_url)
# soup = BeautifulSoup(response.content, 'html.parser')

# summary_text = next(p.get_text() for p in soup.find_all("p") if len(p.get_text()) > 50)
# print(summary_text)
# # # First pattern to match dates between a parenthesis and a dash

# print(get_politician_bday(page_url))