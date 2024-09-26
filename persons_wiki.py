import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import wikipediaapi
import urllib.parse

def get_politician_data(page_url, congress_start_date=None):
#NOTE: TRY WIKIAPI TO GET SUMMARY TEXT INSTEAD.
    wiki_wiki = wikipediaapi.Wikipedia('Congress Wiki Project(dustintran36@gmail.com)', 'en')
    page_url = urllib.parse.unquote(page_url) #remove possible URL encryption that wikiapi can't handle
    page_title = page_url.split("wiki/")[1]
    page_py = wiki_wiki.page(page_title)

    # name_start_text_index = page_py.summary.find(page_title.split("_")[0])
    # summary_text = page_py.summary[name_start_text_index: name_start_text_index+ 200]
    summary_text = page_py.summary[:200]
    starting_parenthesis_index, closing_parenthesis_index = get_valid_index_range_for_summary_text(summary_text)
    summary_text = page_py.summary[starting_parenthesis_index : closing_parenthesis_index]

    months_list = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]

    full_dates_list = re.findall(r'\w+\s+\d{1,2},\s+\d{4}', summary_text)
    month_year_list = re.findall(r'\b\w+\s\d{4}\b', summary_text)
    month_year_list = [month_year for month_year in month_year_list if month_year.split()[0] in months_list]

    # invalid_dates_check = month_year_list + full_dates_list
    # year_list = get_year_list(summary_text, month_year_list + full_dates_list)
    year_list = re.findall(r'\d{4}', summary_text)
    invalid_years_check = "".join(month_year_list) + "".join(full_dates_list)
    year_list = [year for year in year_list if year not in invalid_years_check]

    # print(full_dates_list)
    # print(month_year_list)
    # print(year_list)

    #reset parenthesis;
    temp = starting_parenthesis_index
    starting_parenthesis_index -= temp
    closing_parenthesis_index -= temp

    bday_text = ""
    death_date_text = ""
    #format: (born Month day, year)
    if (summary_text.find("born") != -1 and
        (starting_parenthesis_index < summary_text.find("born") < closing_parenthesis_index)):
        bday_text = full_dates_list[0]
        # print("(born Month day, year): " + page_url)

    #check for (month day, year – month day, year)
    elif (len(full_dates_list) >= 2 and
            (starting_parenthesis_index < summary_text.find(full_dates_list[0])
            < summary_text.find(full_dates_list[1]) < closing_parenthesis_index
            )
        ): 
        bday_text, death_date_text = full_dates_list[:2]
        # print("(month day, year – month day, year): " + page_url)


    #check for (month day, year – month year)
    elif (len(full_dates_list) >= 1 and len(month_year_list) >= 1 and
            (starting_parenthesis_index < summary_text.find(full_dates_list[0])
            < summary_text.find(month_year_list[0]) < closing_parenthesis_index
            )
          ):
        bday_text, death_date_text = full_dates_list[0], month_year_list[0]
        # print("(month day, year – month year): " + page_url)
        # print("from " + full_dates_list[0]
        #       + " to " + month_year_list[0])


    #check for (month day, year – year)
    elif (len(full_dates_list) >= 1 and len(year_list) >= 1 and
            (starting_parenthesis_index < summary_text.find(full_dates_list[0])
            < summary_text.find(year_list[0]) < closing_parenthesis_index
            )
          ):
        bday_text, death_date_text = full_dates_list[0], year_list[0]
        # print("(month day, year – year): " + page_url)

    #check for (month year – month day, year)
    elif (len(month_year_list) >= 1 and len(full_dates_list) >= 1 and
            (starting_parenthesis_index < summary_text.find(month_year_list[0])
            < summary_text.find(full_dates_list[0]) < closing_parenthesis_index
            )
          ):
        bday_text, death_date_text = month_year_list[0], full_dates_list[0]
        # print("(month year – month day, year): " + page_url)
        # print("from " + month_year_list[0]
        #       + " to " + full_dates_list[0])
    
    #check for month year - month year
    elif (len(month_year_list) >= 2 and 
            (starting_parenthesis_index < summary_text.find(month_year_list[0])
            < summary_text.find(month_year_list[1]) < closing_parenthesis_index
            )
          ):
        bday_text, death_date_text = month_year_list[:2]
        # print("(month year – month year): " + page_url)

    #check for month year - year
    elif (len(month_year_list) > 0 and len(year_list) > 0 and
            (starting_parenthesis_index < summary_text.find(month_year_list[0])
             < summary_text.find(year_list[0]) < closing_parenthesis_index)
            ):
        bday_text, death_date_text = month_year_list[0], year_list[0]
        print("(month year - year): " + page_url)


    #check for (year – month day, year)
    elif (len(year_list) > 0 and len(full_dates_list) > 0 and
            (starting_parenthesis_index < summary_text.find(year_list[0])
             < summary_text.find(full_dates_list[0]) < closing_parenthesis_index)
            ):
        bday_text, death_date_text = year_list[0], full_dates_list[0]
        # print("(year – full date): " + page_url)

    #check for (year – month year)
    elif (len(year_list) > 0 and len(month_year_list) > 0 and
            (starting_parenthesis_index < summary_text.find(year_list[0])
             < summary_text.find(month_year_list[0]) < closing_parenthesis_index)
            ):
        bday_text, death_date_text = year_list[0], month_year_list[0]
        # print("(year – month year): " + page_url)

    #check for (year - year)
    elif (len(year_list) >= 2 and
           (starting_parenthesis_index < summary_text.find(year_list[0]) 
            < summary_text.find(year_list[1]) < closing_parenthesis_index) 
          ):
        if summary_text.find("before") > starting_parenthesis_index:
            print("Double check for before word") 
            death_date_text = year_list[1]
        else:
            bday_text, death_date_text = year_list[:2]
        print("(year – year): " + page_url)


    #check for unknown birth
    elif starting_parenthesis_index < summary_text.lower().find("unknown") < closing_parenthesis_index:
        # print("have unknown value for death, not birth")
        unknown_index = summary_text.lower().find("unknown")
        all_dates_list = full_dates_list + month_year_list + year_list
        for date in all_dates_list:
            if starting_parenthesis_index < summary_text.find(date) < unknown_index:
                bday_text = date
                print("have birth date, with unknown death date: " + page_url)
            elif unknown_index < summary_text.find(date) < closing_parenthesis_index:
                death_date_text = date #have a date for death
                print("have death date, with unknown birth date: " + page_url)

    #check for (died [date])
    elif starting_parenthesis_index < summary_text.lower().find("died") < closing_parenthesis_index:
        print("only has death date: " + page_url)
        all_dates_list = full_dates_list + month_year_list + year_list
        death_date_text = all_dates_list[0]

    else: #assuming there is a parenthesis around a date; no word "born" though
        # Regular expression pattern to match "Month day, year" within parentheses
        cases_to_ignore = ["https://en.wikipedia.org/wiki/John_Paterson_(New_York_politician)",
                    "https://en.wikipedia.org/wiki/John_Laurance",
                    "https://en.wikipedia.org/wiki/John_Rhea",
                    "https://en.wikipedia.org/wiki/Ezra_Baker",
                    "https://en.wikipedia.org/wiki/David_Marchand",
                    "https://en.wikipedia.org/wiki/Martin_Van_Buren",
                    "https://en.wikipedia.org/wiki/Henry_William_Connor",
                    "https://en.wikipedia.org/wiki/Davy_Crockett",
                    "https://en.wikipedia.org/wiki/Jacob_Hibshman",
                    "https://en.wikipedia.org/wiki/Jacob_Burnet",
                    "https://en.wikipedia.org/wiki/Doug_Lamborn",
                    ]
        if len(full_dates_list) > 0: #found a date in parenthesis
            bday_text = full_dates_list[0]  
            print("Got full date in parentheses: " + page_url)
        elif starting_parenthesis_index < 0:
            print("No relavent parentheses found: " + page_url)
        elif page_url not in cases_to_ignore:
            print("UNCAPTURED CASE TYPE FOUND: " + page_url)

    bday = process_unformatted_date_text(bday_text.strip(), page_url)
    death_date = process_unformatted_date_text(death_date_text.strip(), page_url)
    # print(str(matches) + ":\t" + bday)
    if (is_valid_date(bday) == False):
        if page_url == "https://en.wikipedia.org/wiki/John_Paterson_(New_York_politician)": #a pair of preceding parenthesis
            bday = "January 1, 1744"
        elif page_url == "https://en.wikipedia.org/wiki/John_Laurance": #a pair of preceding parenthesis
            bday = "January 1, 1750"
        elif page_url == "https://en.wikipedia.org/wiki/John_Rhea": #a pair of preceding parenthesis
            bday = "January 1, 1753"
        elif page_url == "https://en.wikipedia.org/wiki/Ezra_Baker": #no parentheses to indicate birthday
            bday = "January 1, 1765"
        elif page_url == "https://en.wikipedia.org/wiki/David_Marchand": #no parentheses to indicate birthday
            bday = "January 31, 1772"
        elif page_url == "https://en.wikipedia.org/wiki/Martin_Van_Buren": #a pair of preceding parenthesis
            bday = "December 5, 1782"
        elif page_url == "https://en.wikipedia.org/wiki/Henry_William_Connor": #year_list is improperly filtered
            bday = "August 5, 1793"
        # elif page_url == "https://en.wikipedia.org/wiki/Davy_Crockett": #summary text starts with "David", not "Davy"
        #     bday = "August 17, 1786"
        elif page_url == "https://en.wikipedia.org/wiki/Jacob_Hibshman": #additional text in front of summary
            bday = "January 31, 1772"
        elif page_url == "https://en.wikipedia.org/wiki/Jacob_Burnet": #a pair of preceding parenthesis
            bday = "February 22, 1770"
        elif page_url == "https://en.wikipedia.org/wiki/Doug_Lamborn": #having "born" in name messes up function
            bday = "May 24, 1954"

        else:
            print("Invalid/Unknown Date for: " + page_url) 
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
    return bday, age, death_date



def process_unformatted_date_text(bday_text, page_url):
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
    if bday_list[0] in months_list:  #starting value is the month
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
    





def get_valid_index_range_for_summary_text(summary_text):
    starting_parenthesis_index = summary_text.find('(')
    closing_parenthesis_index = -1

    if starting_parenthesis_index == -1:
        return -1, -1
    stack = []
    indices = []
    for i, char in enumerate(summary_text):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                start = stack.pop()
                indices.append((start, i))
    
    year_list = re.findall(r'\d{4}', summary_text) #get the years in the summary_text
    for parentheses in indices:
        for date in year_list:
            date_index = summary_text.find(date)
            if parentheses[0] < date_index < parentheses[1]:
                return parentheses 
    return -1, -1