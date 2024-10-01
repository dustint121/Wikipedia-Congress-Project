import re
from datetime import datetime
import wikipediaapi
import urllib.parse
import random
#THIS WIKI SECTION AND MAIN FUNCTION, GET_POLITICIAN_DATA, IS CALLED ON BY THE SESSIONS_WIKI FILE.


def get_politician_data(page_url, congress_start_date=None, congress_num=None):
    wiki_wiki = wikipediaapi.Wikipedia('Congress Wiki Project(dustintran36@gmail.com)', 'en')
    page_title = page_url.split("wiki/")[1]
    page_py = wiki_wiki.page(page_title)

    summary_text = page_py.summary[:200]
    starting_parenthesis_index, closing_parenthesis_index = get_valid_index_range_for_summary_text(summary_text)
    summary_text = page_py.summary[starting_parenthesis_index : closing_parenthesis_index]

    months_list = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]

    full_dates_list = re.findall(r'\w+\s+\d{1,2},\s+\d{4}', summary_text)
    month_year_list = re.findall(r'\b\w+\s\d{4}\b', summary_text)
    month_year_list = [month_year for month_year in month_year_list if month_year.split()[0] in months_list]

    year_list = re.findall(r'\d{4}', summary_text)
    invalid_years_check = "".join(month_year_list) + "".join(full_dates_list)
    year_list = [year for year in year_list if year not in invalid_years_check]

    #reset parenthesis;
    closing_parenthesis_index -= starting_parenthesis_index
    starting_parenthesis_index -= starting_parenthesis_index

    #first politician sex
    sex = get_sex_from_wiki_page(wiki_page=page_py,congress_num=congress_num, page_url=page_url)
    if congress_num != None and sex == None:
        if page_url == "https://en.wikipedia.org/wiki/Franklin_Ellsworth": #no gender references at all
            sex = "male"
        elif page_url == "https://en.wikipedia.org/wiki/Harold_B._McSween": #no gender references at all
            sex = "male"
        elif page_url == "https://en.wikipedia.org/wiki/Norman_D._Shumway": #no gender references in first 2 sections
            sex = "male"
        else:
            print("Can't find sex: " + page_url)

    bday_text = ""
    death_date_text = ""

    if summary_text.lower().find("before") != -1:
        print("found before; please double check: " + page_url)

    #format: (born Month day, year)
    if (summary_text.find("born") != -1 and len(full_dates_list) == 1 and
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
        cases_to_ignore = [
                    "https://en.wikipedia.org/wiki/Ezra_Baker",
                    "https://en.wikipedia.org/wiki/David_Marchand",
                    "https://en.wikipedia.org/wiki/Andrew_Boden",
                    "https://en.wikipedia.org/wiki/Daniel_H._Miller",
                    "https://en.wikipedia.org/wiki/John_Cramer_(representative)",
                    "https://en.wikipedia.org/wiki/William_Allen_(governor)",
                    "https://en.wikipedia.org/wiki/Jabez_Young_Jackson",
                    "https://en.wikipedia.org/wiki/Ebenezer_J._Shields",
                    "https://en.wikipedia.org/wiki/John_W._Noell",
                    "https://en.wikipedia.org/wiki/Henry_H._Starkweather",
                    "https://en.wikipedia.org/wiki/John_Brown_Gordon",
                    "https://en.wikipedia.org/wiki/Charles_Daniels_(New_York_politician)",
                    "https://en.wikipedia.org/wiki/Chip_Cravaack"
                    ]
        if page_url in cases_to_ignore: #edge cases to ignore
            x = 1
        elif len(full_dates_list) > 0: #found a date in parenthesis
            bday_text = full_dates_list[0]  
            print("Got full date in parentheses: " + page_url)
        elif summary_text.find('(') == -1:
            print("No relavent parentheses found: " + page_url)
        elif page_url not in cases_to_ignore:
            print("UNCAPTURED CASE TYPE FOUND: " + page_url)

    #edge cases; wrong dates determined
    if page_url == "https://en.wikipedia.org/wiki/Thomas_Terry_Davis": #(before year - full year)
        bday_text = ""
    if page_url == "https://en.wikipedia.org/wiki/William_Shepard": #weird case; 3 dates
            bday_text = "December 1, 1737"
            death_date_text = "November 16, 1817"       

    bday = process_unformatted_date_text(bday_text.strip(), page_url)
    death_date = process_unformatted_date_text(death_date_text.strip(), page_url)
    # print(str(matches) + ":\t" + bday)
    if (is_valid_date(bday) == False):
        if page_url == "https://en.wikipedia.org/wiki/Ezra_Baker": #no parentheses to indicate birthday
            bday = "January 1, 1765"
        elif page_url == "https://en.wikipedia.org/wiki/David_Marchand": #no parentheses to indicate birthday
            bday = "January 31, 1772"
            death_date = "March 11, 1832"
        elif page_url == "https://en.wikipedia.org/wiki/Andrew_Boden": #has an unspecified date date in personal section
            death_date = "December 20, 1835"
        elif page_url == "https://en.wikipedia.org/wiki/Daniel_H._Miller": #has an unspecified date date in personal section
            death_date = "January 1, 1846"
        elif page_url == "https://en.wikipedia.org/wiki/John_Cramer_(representative)": #no parentheses to indicate birthday
            bday = "May 17, 1779"
            death_date = "June 1, 1870"       
        elif page_url == "https://en.wikipedia.org/wiki/William_Allen_(governor)": #weird "or" for day in bday  
            bday = "December 18, 1803"
            death_date = "July 11, 1879"  
        elif page_url == "https://en.wikipedia.org/wiki/Jabez_Young_Jackson": #weird format (day month year)
            bday = "August 5, 1790"  
        elif page_url == "https://en.wikipedia.org/wiki/Ebenezer_J._Shields": #unlisted in summary  
            bday = "December 22, 1778"
            death_date = "April 21, 1846"  
        elif page_url == "https://en.wikipedia.org/wiki/John_W._Noell": #unlisted in summary
            bday = "February 22, 1816"
            death_date = "March 14, 1863" 
        elif page_url == "https://en.wikipedia.org/wiki/Henry_H._Starkweather": #unlisted in summary
            bday = "April 19, 1826"
            death_date = "January 28, 1876"      
        elif page_url == "https://en.wikipedia.org/wiki/John_Brown_Gordon": #formatting in summary is messed up by hidden text 
            bday = "February 6, 1832"
            death_date = "January 9, 1904"     
        elif page_url == "https://en.wikipedia.org/wiki/Charles_Daniels_(New_York_politician)": #incomplete parenthesis    
            bday = "March 24, 1825"
            death_date = "December 20, 1897"             
        elif page_url == "https://en.wikipedia.org/wiki/Chip_Cravaack":  # (born year)
            bday = "January 29, 1951"
        else:
            print("Invalid/Unknown Date for: " + page_url) 
            print("\t" + bday_text)
            if bday != None:
                print("\t" + bday)
            else:
                print("\tNone")
    age = None
    age_at_death = None

    #do a last check; bday should be before congress start and min difference in years should be 25
    date_format = "%B %d, %Y"
    congress_start = datetime.strptime(congress_start_date, date_format) if congress_start_date != None else None
    bday_date = datetime.strptime(bday, date_format) if bday != None else None
    death_day = datetime.strptime(death_date, date_format) if death_date != None else None
    if bday_date != None:
        if congress_start != None:
            if bday_date > congress_start:
                print("Invalid BDay: After Congress Start: " + str([congress_start_date, bday]) + "; " + page_url)
            else:
                age = (congress_start - bday_date).days//365
                if age < 25:
                    print("Invalid BDay: Under 25 " + str([congress_start_date, bday]) + "; " + page_url)
        if death_day != None:
            age_at_death = (death_day - bday_date).days//365

    data = {"birth_date":bday, "death_date": death_date, "age_at_congress": age, "age_at_death": age_at_death, "sex": sex}
    return data



def process_unformatted_date_text(date_text, page_url):
    if date_text == "":
        return None
    date_text = date_text.replace('\xa0', ' ')  # Replace non-breaking space with a regular space
    date_text = date_text.replace('\u2009', ' ') # Replace non-breaking space with a regular space
    date_list = date_text.split(" ")
    date_list = [val.split(',')[0] for val in date_list if val != ','] #remove possible commas
    if len(date_list) == 0:
        return None
    month, day, year = None, None, None
    months_list = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]
    if date_list[0] in months_list:  #starting value is the month
        month = date_list[0] #remove possible commas if "month, year format"
        if (len(date_list[1]) in (1,2)): #second value is day
            day = date_list[1] + ","
            year = date_list[2][:4]
        else: #likey has "month, year format"; will set default day to "1st" of month
            month = date_list[0]
            year = date_list[1][:4]
            day = "1,"
    #check for "day month year" or "year month day" 
    elif len(date_list) >= 3 and date_list[1] in months_list:
        month = date_list[1]
        #check for "day month year"
        if date_list[0].isnumeric() and len(str(date_list[0])) <= 2 and date_list[2].isnumeric() and len(str(date_list[2])) == 4:
            day = date_list[0] + ","
            year =  date_list[2][:4]
        #check for "year month day" 
        elif date_list[0].isnumeric() and len(str(date_list[0])) == 4 and date_list[2].isnumeric() and len(str(date_list[2])) <= 2:
            year = date_list[0][:4]
            day =  date_list[2] + ","
        else:
            return None
    else:
        if date_list[0][:4].isnumeric() == False:
            return None
        #likely has just a "year" for the date; set month and day to "January" and "1st"
        year = date_list[0][:4]
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
    if summary_text.find('(') == -1:
        return 0, 0
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
            if parentheses[0] < summary_text.lower().find("unknown") < parentheses[1]:
                return parentheses
    return 0, 0



#CONSIDER DOING PERCENTAGE RATHER THAN FIRST INSTANCE
def get_sex_from_wiki_page(wiki_page, congress_num, page_url):
    sex = None
    male_count = 0
    female_count = 0
    total_count = 0
    if congress_num != None:
        if congress_num < 65:
            sex = "male"
        elif congress_num >= 65: #first female congress was in 65th congress
            # sex_dict = {"she": "female", "he": "male", "his" : "male", "her" : "female"}
            #only get first two section(including their subsections) after the summary
            wiki_page_sections = []
            if len(wiki_page.sections) > 0:
                wiki_page_sections = get_all_wiki_text_by_section(wiki_page.sections[0:2])
            wiki_page_sections.insert(0, wiki_page.summary.lower()) 
            for section in wiki_page_sections:
                if total_count >= 50:
                    break
                text = section.split()
                for word in text:
                    if total_count >= 50:
                        break
                    if word in ["he", "his"]:
                        male_count += 1
                        total_count += 1
                    elif word in ["she", "her"]:
                        female_count += 1
                        total_count += 1     
            if total_count > 0:
                male_probability = male_count/total_count
                sex = "male" if male_probability > 0.5 else "female" 
                if page_url == "https://en.wikipedia.org/wiki/Barbara_Mikulski": #has a quoted speech with lots of male pronouns
                    sex = "female"
                elif 0.3 < male_probability < 0.7:
                    print("Sex determination is close(" + str(male_probability) + ":" + sex + ") " + page_url)
    return sex

def get_all_wiki_text_by_section(sections):
    section_list = []
    for s in sections:
        if s.title not in ["See also", "Notes", "References", "External links","External links"]:
            section_list.append(s.text.lower())
            section_list += get_all_wiki_text_by_section(s.sections)
    return section_list
        