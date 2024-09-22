import requests
from bs4 import BeautifulSoup
import re




#has 3 tables for congressional session: past, current, future
def get_congress_list():
    page_url = "https://en.wikipedia.org/wiki/List_of_United_States_Congresses"
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    congress_list = []
    #below variables has "previous congress" and "current congress" in two tables in a list
    congress_tables = soup.findAll("table",{'class': "wikitable"})[:2]
    for congress_table in congress_tables:
        for row in congress_table.findAll("tr"):
            if row.find("a") is not None:
                congress_num = int(row.find("a").text.split()[0][:-2])
                URL = "https://en.wikipedia.org" + row.find("a").get("href")
                start_date = row.findAll("td")[0].text.strip()
                end_date = row.findAll("td")[-1].text.strip()
                congress_list.append({'congress_num': congress_num, 'start_date': start_date,
                                    'end_date': end_date, 'URL': URL})
    # for congress in congress_list:
    #     print(congress)
    return congress_list



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
                                        ,'party': party, 'state': state
                                        })





#get political parties/affiations for each congress
def get_all_parties_dict():
    congress_list = get_congress_list()[1:] #will skip the first congress for convience on "previous congress" check
    party_dict = {1: {'A': 'Anti-Administration', 'P': 'Pro-Administration'}}
    for congress in congress_list:
        congress_num = congress['congress_num']
        party_dict[congress_num] = {}
        print("Congress Num: " + str(congress['congress_num']))
        URL = congress["URL"]
        response = requests.get(URL)
        soup = BeautifulSoup(response.content, 'html.parser')

        all_tables = soup.find_all("table",{'class':"wikitable"})
        party_tables = [] #will be a list of 2 HTML elements with the parties in the senate and house respectively 
        for table in all_tables: #will find the two correct tables and add to above list
            for row in table.find_all("th"):
                if row.get("colspan") != None:
                    if "Party" in row.text or "Faction" in row.text: #no parties until 4th congress, only factions
                        party_tables.append(table)

        for table in party_tables:
            for row in table.find_all("a"):
                if row.text in ["previous Congress", "previous congress"]: #indicates end of parties listed
                    break
                if row.text == '[d]': #unique case to skip
                    continue
                temp_list = re.findall('[A-Z][^A-Z]*', row.text) #will separate a string by uppercase letters
                temp_list = [val.strip() for val in temp_list]
                party = ' '.join(temp_list).strip() if temp_list[0][-1] != '-' else ''.join(temp_list).strip()
                #get text inside parenthesis that represents an abbreviation
                temp_list = re.search(r'\((.*?)\)', row.parent.text)
                abbreviation = temp_list.group(1) if temp_list != None else party[0]
                abbreviation = abbreviation if abbreviation != "caucusing withDemocrats" else 'I' #unique case to fix
                print("\t" + abbreviation + ":   " + party)
                party_dict[congress_num][abbreviation] = party
    #fix unique case in 33rd congress
    del party_dict[33]["United States"]
    party_dict[33]['I'] = "Independent"
    #fix unique case in 34th congress
    del party_dict[34]["Know Nothing"]
    party_dict[33]['A'] = "Know Nothing"
    # print(party_dict)
    return party_dict


#need to add A:
#1-3 = {'A': 'Anti-Administration', 'P': 'Pro-Administration'}
#4-18 = {'DR': 'Democratic-Republican', 'F': 'Federalist'}
#19-24 = Jacksonian era
#25-34    = Democratic vs Whig vs Others
#100 - Present = Only Democrat, Republican, and Independent now
def get_all_parties_dict_fast():
    return {1: {'A': 'Anti-Administration', 'P': 'Pro-Administration'}, 2: {'A': 'Anti-Administration', 'P': 'Pro-Administration'}, 3: {'A': 'Anti-Administration', 'P': 'Pro-Administration'}, 
            4: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 5: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 6: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 7: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 8: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 9: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 10: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 11: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 12: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 13: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 14: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 15: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 16: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 17: {'DR': 'Democratic-Republican', 'F': 'Federalist'}, 18: {'DR': 'Democratic-Republican', 'F': 'Federalist', 'D': 'Democratic-Republican'}, 19: {'A': 'Anti-Jacksonian', 'J': 'Jacksonian'}, 20: {'NR': 'National Republican', 'J': 'Jacksonian'}, 21: {'NR': 'National Republican', 'J': 'Jacksonian', 'AM': 'Anti-Masonic'}, 22: {'NR': 'National Republican', 'J': 'Jacksonian', 'N': 'Nullifier', 'AM': 'Anti-Masonic'}, 23: {'NR': 'National Republican', 'J': 'Jacksonian', 'N': 'Nullifier', 'AM': 'Anti-Masonic'}, 24: {'NR': 'National Republican', 'J': 'Jacksonian', 'N': 'Nullifier', 'AM': 'Anti-Masonic', 'SR': "States' Rights"}, 
            25: {'D': 'Democratic', 'W': 'Whig', 'AM': 'Anti-Masonic', 'N': 'Nullifier'}, 26: {'D': 'Democratic', 'W': 'Whig', 'AM': 'Anti-Masonic', 'C': 'Conservative'}, 27: {'D': 'Democratic', 'W': 'Whig', 'ID': 'Independent Democratic'}, 28: {'D': 'Democratic', 'LO': 'Lawand Order', 'W': 'Whig', 'ID': 'Independent Democratic', 'IW': 'Independent Whig'}, 29: {'D': 'Democratic', 'L': 'Liberty', 'W': 'Whig', 'A': 'American'}, 30: {'D': 'Democratic', 'ID': 'Independent Democratic', 'L': 'Liberty', 'W': 'Whig', 'A': 'American', 'I': 'Independent'}, 31: {'D': 'Democratic', 'FS': 'Free Soil', 'W': 'Whig', 'A': 'Know Nothing', 'I': 'Independent'}, 32: {'D': 'Democratic', 'FS': 'Free Soil', 'W': 'Whig', 'ID': 'Independent Democratic', 'SR': 'Southern Rights', 'U': 'Union'}, 33: {'A': 'Know Nothing', 'D': 'Democratic', 'F': 'Free Soil', 'W': 'Whig', 'ID': 'Independent Democratic', 'FS': 'Free Soil', 'I': 'Independent'}, 34: {'D': 'Democratic', 'O': 'Opposition', 'FS': 'Free Soil', 'R': 'Republican', 'W': 'Whig'}, 35: {'A': 'Know Nothing', 'D': 'Democratic', 'R': 'Republican', 'ID': 'Independent Democratic'}, 36: {'A': 'Know Nothing', 'D': 'Democratic', 'R': 'Republican', 'ALD': 'Anti-LecomptonDemocratic', 'ID': 'Independent Democratic', 'O': 'Opposition'}, 37: {'D': 'Democratic', 'R': 'Republican', 'UU': 'Unconditional Union', 'U': 'National Union', 'CU': 'Constitutional Union', 'ID': 'Independent Democratic'}, 38: {'D': 'Democratic', 'R': 'Republican', 'U': 'Unionist', 'UU': 'Unconditional Unionist', 'IR': 'Independent Republican'}, 39: {'D': 'Democratic', 'R': 'Republican', 'U': 'Unionist', 'UU': 'Unconditional Unionist', 'IR': 'Independent Republican'}, 40: {'D': 'Democratic', 'R': 'Republican', 'IR': 'Independent Republican', 'CR': 'Conservative Republican', 'C': 'Conservative'}, 41: {'D': 'Democratic', 'R': 'Republican', 'C': 'Conservative'}, 42: {'D': 'Democratic', 'LR': 'Liberal Republican', 'R': 'Republican', 'IR': 'Independent Republican'}, 43: {'D': 'Democratic', 'AM': 'Anti-Monopoly', 'LR': 'Liberal Republican', 'R': 'Republican', 'ID': 'Independent Democratic', 'I': 'Independent', 'IR': 'Independent Republican'}, 44: {'D': 'Democratic', 'AM': 'Anti-Monopoly', 'R': 'Republican', 'ID': 'Independent Democratic', 'I': 'Independent', 'IR': 'Independent Republican'}, 45: {'AM': 'Anti-Monopoly', 'D': 'Democratic', 'R': 'Republican', 'I': 'Independent Republican', 'ID': 'Independent Democratic', 'G': 'Greenback'}, 46: {'AM': 'Anti-Monopoly', 'D': 'Democratic', 'R': 'Republican', 'I': 'Independent', 'ID': 'Independent Democratic', 'GB': 'Greenback'}, 47: {'D': 'Democratic', 'I': 'Independent', 'RA': 'Readjuster', 'R': 'Republican', 'ID': 'Independent Democrat', 'GB': 'Greenback', 'IR': 'Independent Republican'}, 48: {'D': 'Democratic', 'RA': 'Readjuster', 'R': 'Republican', 'ID': 'Independent Democratic', 'I': 'Independent', 'GB': 'Greenback', 'IR': 'Independent Republican', 'AM': 'Anti-Monopoly'}, 49: {'D': 'Democratic', 'RA': 'Readjuster', 'R': 'Republican', 'GB': 'Greenback'}, 50: {'D': 'Democratic', 'RA': 'Readjuster', 'R': 'Republican', 'L': 'Labor', 'GB': 'Greenback', 'I': 'Independent', 'IR': 'Independent Republican'}, 51: {'D': 'Democratic', 'R': 'Republican', 'L': 'Labor'}, 52: {'D': 'Democratic', 'P': 'Populist', 'I': 'Independent', 'R': 'Republican'}, 53: {'D': 'Democratic', 'P': 'Populist', 'R': 'Republican', 'S': 'Silver', 'ID': 'Independent Democratic'}, 54: {'D': 'Democratic', 'P': 'Populist', 'R': 'Republican', 'SR': 'Silver Republican', 'S': 'Silver'}, 55: {'D': 'Democratic', 'P': 'Populist', 'R': 'Republican', 'SR': 'Silver Republican', 'S': 'Silver', 'IR': 'Independent Republican'}, 56: {'D': 'Democratic', 'P': 'Populist', 'R': 'Republican', 'SR': 'Silver Republican', 'S': 'Silver'}, 57: {'D': 'Democratic', 'P': 'Populist', 'R': 'Republican', 'SR': 'Silver Republican', 'S': 'Silver'}, 58: {'D': 'Democratic', 'P': 'Populist', 'R': 'Republican', 'SR': 'Silver Republican'}, 59: {'D': 'Democratic', 'R': 'Republican'}, 60: {'D': 'Democratic', 'R': 'Republican', 'ID': 'Independent Democratic'}, 61: {'D': 'Democratic', 'R': 'Republican', 'ID': 'Independent Democratic'}, 62: {'D': 'Democratic', 'Prog.': 'Bull Moose', 'R': 'Republican', 'S': 'Socialist'}, 63: {'D': 'Democratic', 'Prog.': 'Bull Moose', 'R': 'Republican', 'I': 'Independent'}, 64: {'D': 'Democratic', 'R': 'Republican', 'Prog.': 'Bull Moose', 'Soc.': 'Socialist', 'I': 'Independent', 'Proh.': 'Prohibition'}, 65: {'D': 'Democratic', 'R': 'Republican', 'Prog.': 'Bull Moose', 'Soc.': 'Socialist', 'Proh.': 'Prohibition'}, 66: {'D': 'Democratic', 'R': 'Republican', 'Soc.': 'Socialist', 'FL': 'Farmer-Labor', 'IR': 'Independent Republican', 'Proh.': 'Prohibition'}, 67: {'D': 'Democratic', 'FL': 'Farmer– Labor', 'R': 'Republican', 'Soc.': 'Socialist', 'IR': 'Independent Republican'}, 68: {'D': 'Democratic', 'FL': 'Farmer– Labor', 'R': 'Republican', 'Soc.': 'Socialist'}, 69: {'D': 'Democratic', 'FL': 'Farmer– Labor', 'R': 'Republican', 'Soc.': 'Socialist'}, 70: {'D': 'Democratic', 'FL': 'Farmer– Labor', 'R': 'Republican', 'S': 'Socialist'}, 71: {'D': 'Democratic', 'FL': 'Farmer– Labor', 'R': 'Republican'}, 72: {'D': 'Democratic', 'FL': 'Farmer– Labor', 'R': 'Republican', 'F': 'Farmer– Labor'}, 73: {'D': 'Democratic', 'F': 'Farmer– Labor', 'P': 'Progressive', 'R': 'Republican'}, 74: {'D': 'Democratic', 'FL': 'Farmer– Labor', 'P': 'Wisconsin Progressive', 'R': 'Republican'}, 75: {'D': 'Democratic', 'F': 'Farmer– Labor', 'P': 'Wisconsin Progressive', 'R': 'Republican', 'I': 'Independent', 'FL': 'Farmer– Labor'}, 76: {'D': 'Democratic', 'FL': 'Farmer– Labor', 'P': 'Wisconsin Progressive', 'R': 'Republican', 'I': 'Independent', 'AL': 'American Labor', 'WP': 'Wisconsin Progressive'}, 77: {'D': 'Democratic', 'FL': 'Farmer– Labor', 'P': 'Wisconsin Progressive', 'R': 'Republican', 'I': 'Independent', 'AL': 'American Labor'}, 78: {'D': 'Democratic', 'WP': 'Wisconsin Progressive', 'R': 'Republican', 'FL': 'Farmer– Labor', 'AL': 'American Labor'}, 79: {'D': 'Democratic', 'P': 'Progressive', 'R': 'Republican', 'FL': 'Farmer– Labor', 'AL': 'American Labor'}, 80: {'D': 'Democratic', 'P': 'Progressive', 'R': 'Republican', 'A': 'American Labor'}, 81: {'D': 'Democratic', 'R': 'Republican', 'AL': 'American Labor', 'Lib': 'Liberal', 'I': 'Independent'}, 82: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 83: {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}, 84: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 85: {'D': 'Democratic', 'R': 'Republican'}, 86: {'D': 'Democratic', 'R': 'Republican'}, 87: {'D': 'Democratic', 'R': 'Republican'}, 88: {'D': 'Democratic', 'R': 'Republican'}, 89: {'D': 'Democratic', 'R': 'Republican'}, 90: {'D': 'Democratic', 'R': 'Republican'}, 91: {'D': 'Democratic', 'R': 'Republican'}, 92: {'D': 'Democratic', 'R': 'Republican'}, 93: {'D': 'Democratic', 'R': 'Republican', 'C': 'Conservative', 'I': 'Independent'}, 94: {'D': 'Democratic', 'I': 'Independent', 'C': 'Conservative', 'R': 'Republican'}, 95: {'C': 'Conservative', 'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 96: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican', 'C': 'Conservative'}, 97: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican', 'C': 'Conservative'}, 98: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican', 'C': 'Conservative'}, 99: {'D': 'Democratic', 'R': 'Republican', 'C': 'Conservative'}, 100: {'D': 'Democratic', 'R': 'Republican'}, 101: {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}, 102: {'D': 'Democratic', 'R': 'Republican'}, 103: {'D': 'Democratic', 'R': 'Republican'}, 104: {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}, 105: {'R': 'Republican', 'D': 'Democratic'}, 106: {'D': 'Democratic', 'R': 'Republican'}, 107: {'D': 'Democratic', 'I': 'Independent', 'IPM': 'Independence', 'R': 'Republican'}, 108: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 109: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 110: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 111: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 112: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 113: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 114: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 115: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}, 116: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican', 'L': 'Libertarian'}, 117: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican', 'L': 'Libertarian'}, 118: {'D': 'Democratic', 'I': 'Independent', 'R': 'Republican'}}

get_all_parties_dict()