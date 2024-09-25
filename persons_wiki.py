import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def get_politician_bday(page_url):
    # response = requests.get(page_url, timeout=10) #10 seconds to read
    response = requests.get(page_url)
    if response == None:
        print(page_url)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    #return the first set of text that exceeds 50 characters; should be the summary section
    summary_text = next(p.get_text() for p in soup.find_all("p") if len(p.get_text()) > 50)
    # print(summary_text)

    months_list = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]

    matches = []

    #format: (born Month day, year)
    if "born" in summary_text[:150]:
        # print("here1")
        #text is after the word "born", before a ")", and is the last 3 words
        text = " ".join(summary_text[:150].split("born")[1].split(")")[0].split(" ")[-3:])
        pattern = r'\w+\s+\d{1,2},\s+\d{4}'  #find date
        matches += re.findall(pattern, text)

    #(month day, year - month day, year)
    elif len(re.findall(r'\w+\s+\d{1,2},\s+\d{4}', summary_text[:200])) >= 2: 
        print(page_url)
        print("here2")
        matches += re.findall(r'\w+\s+\d{1,2},\s+\d{4}', summary_text[:200])



    #check for month year - month day, year
    elif (len(re.findall(r'\b\w+\s\d{4}\b', summary_text[:200])) == 1
            and re.findall(r'\b\w+\s\d{4}\b', summary_text[:200])[0].split()[0] in months_list
            and len(re.findall(r'\w+\s+\d{1,2},\s+\d{4}', summary_text[:200])) == 1):
        print("here3")
        print(page_url)
        print(re.findall(r'\b\w+\s\d{4}\b', summary_text[:200]))
        print(re.findall(r'\w+\s+\d{1,2},\s+\d{4}', summary_text[:200]))
        matches += re.findall(r'\b\w+\s\d{4}\b', summary_text[:200])

    #check for c. year - month day, year
    elif "c." in summary_text[:200] or "ca." in summary_text[:200]:
        print("here4")
        print(page_url)
        # matches += re.findall(r'c\.\s?\d{4}', summary_text[:200])
        matches += re.findall(r'\d{4}', summary_text[:200])
    
    elif "unknown" in summary_text[:150].lower():
        print("here5")
        print(page_url)
        matches.append("")


    else: #assuming there is a parenthesis around a date; no word "born" though
        # Regular expression pattern to match "Month day, year" within parentheses
        print("here6")
        print(page_url)
        pattern = r'\w+\s+\d{1,2},\s+\d{4}' #get first full date
        possible_match = re.findall(pattern, summary_text[:200])[0]
        index = summary_text[:200].find(possible_match)
        if summary_text[:200].find("(") < index < summary_text[:200].find(")"):
            matches += re.findall(pattern, summary_text[:200])
        else:
            matches.append("")
        print(matches)

 
    bday_text = matches[0].strip() if len(matches) > 0 else ""
    bday = process_unformatted_bday_text(bday_text.strip(), page_url)
    # print(str(matches) + ":\t" + bday)
    if (is_valid_date(bday) == False):
        if page_url == "https://en.wikipedia.org/wiki/Doug_Lamborn": #having "born" in name messes up function
            bday = "May 24, 1954"
        else:
            print("Invalid Date for: " + page_url) 
            print("\t" + bday_text)
            if bday != None:
                print("\t" + bday)
            else:
                print("\tNone")
    return None




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


    if bday_list[0] in ["c.", "ca."]: #got approxiamate year: "c. [year]" or "ca. [year]"
        year = bday_list[1]
        return "January 1, " + year


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





# get_politician_bday("https://en.wikipedia.org/wiki/William_Smith_(South_Carolina_senator)") #has "c. [year]"
# get_politician_bday("https://en.wikipedia.org/wiki/John_Henry_(Maryland_politician)") #has "month year to month day, year"
# page_url = "https://en.wikipedia.org/wiki/Kevin_McCarthy"
# page_url = "https://en.wikipedia.org/wiki/Ann_Wagner"
# response = requests.get(page_url)
# soup = BeautifulSoup(response.content, 'html.parser')

# summary_text = next(p.get_text() for p in soup.find_all("p") if len(p.get_text()) > 50)
# print(summary_text)
# # # First pattern to match dates between a parenthesis and a dash

# get_politician_bday(page_url)

# print("September 8, 1941".split(" "))