import requests
from bs4 import BeautifulSoup
import re




#has 3 tables for congressional session: past, current, future
def get_congress_list():
    page_url = "https://en.wikipedia.org/wiki/List_of_United_States_Congresses"
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    congress_tables = soup.findAll("table",{'class': "wikitable"}) 

    previous_congress_table = congress_tables[0]
    for row in previous_congress_table.findAll("tr"):
        if row.find("a") is not None:
            congress_num = int(row.find("a").text.split()[0][:-2])
            URL = "https://en.wikipedia.org" + row.find("a").get("href")
            start_date = row.findAll("td")[0].text.strip()
            end_date = row.findAll("td")[-1].text.strip()
            # print((start_date, end_date))

    present_congress_table = congress_tables[1]
    print(present_congress_table.find("a"))
    print(present_congress_table.find("a").get("href"))







def get_congresspeople_for_a_congress(page_url):
    # page_url = "https://en.wikipedia.org/wiki/1st_United_States_Congress"
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    senate_table, representative_table = soup.find_all("table",{'class':"col-begin", 'role':"presentation"})


    # senate_table = representative_table





    states = [heading.find("h4").text for heading in senate_table.find_all('div', class_='mw-heading4')]

    congressmen_by_state_HTML = senate_table.find_all("dl") #need to remove senators not at the start of congress session
    #below line: removes senators not at start of congress session; is written as a sub-dl tag in the html code 
    congressmen_by_state_HTML = [dl for dl in congressmen_by_state_HTML if dl.find_parent('dl') is None] 


    for index in range(len(states)): #for each state
        state = states[index]
        congressmen_data = []
        for a in congressmen_by_state_HTML[index].find_all('a', resurive=False):
            # Check if the parent of the <a> tag is a direct child of the <dl> tag; 
                # to prevent recording of substitute congressman
            #filter for no "span" direct parent tag; is unneeded data
            if a.find_parent('dl') == congressmen_by_state_HTML[index] and a.parent.name != "span":
                #get party affiation below
                text = a.parent.text
                match = re.search(r'\((.*?)\)', text) #get text inside parenthesis that represents party affiation
                party = match.group(1)
                print(party)
                congressmen_data.append({'name':a.text, 'URL': "https://en.wikipedia.org" + a.get("href")
                                        ,'party': party
                                        })




    # print(state)
    # print(congressmen_data)
    # print("\n")





