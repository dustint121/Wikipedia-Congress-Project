import persons_wiki
import wikipediaapi
import urllib.parse
#edge cases to work on

# "https://en.wikipedia.org/wiki/William_Shepard" doable but weird

#https://en.wikipedia.org/wiki/Jacob_Hibshman  ; additional text in front
#"https://en.wikipedia.org/wiki/John_Paterson_(New_York_politician)": #a pair of preceding parenthesis

#"https://en.wikipedia.org/wiki/Henry_William_Connor" #dates after parentheses can mess things up; will not get most accurate
#page_url == "https://en.wikipedia.org/wiki/Doug_Lamborn": #having "born" in name messes up function

#https://en.wikipedia.org/wiki/Thomas_Terry_Davis #has the word before

#"https://en.wikipedia.org/wiki/John_Steele_(North_Carolina_politician)", #24 when serving congress

#text length considerations below
# "https://en.wikipedia.org/wiki/Philip_Key_(U.S._politician)"  #summary text is only 96 characters
# "https://en.wikipedia.org/wiki/John_Sevier" #there is another text before sumamry text that is 73 characters



#test cases below

# "https://en.wikipedia.org/wiki/John_Stewart_(Pennsylvania_politician)" #unknown case
# "https://en.wikipedia.org/wiki/Pleasant_Moorman_Miller" #unknown case
# "https://en.wikipedia.org/wiki/John_Morrow_(Virginia_politician)" #unknown case
# page_url == "https://en.wikipedia.org/wiki/Abram_Trigg": #has an unknown date of death

# page_url = "https://en.wikipedia.org/wiki/Peter_Silvester_(1734%E2%80%931808)" #has encrypted URL
# page_url == "https://en.wikipedia.org/wiki/Joseph_F._Wingate": #unknown date of death

# print(get_politician_bday("https://en.wikipedia.org/wiki/Oliver_Ellsworth")) #full date to full date
# print(get_politician_bday("https://en.wikipedia.org/wiki/John_Vining")) #has full date to month year
# print(get_politician_bday("https://en.wikipedia.org/wiki/Peter_Van_Gaasbeck")) #full date to year

# get_politician_bday("https://en.wikipedia.org/wiki/John_Henry_(Maryland_politician)") #has "month year to full date"
# get_politician_bday("https://en.wikipedia.org/wiki/Cornelius_C._Schoonmaker") #month year - month year

# print(get_politician_bday("https://en.wikipedia.org/wiki/Andrew_Moore_(politician)"))#year - full date
# print(get_politician_bday("https://en.wikipedia.org/wiki/John_Culpepper"))  #year - month year
# get_politician_bday("https://en.wikipedia.org/wiki/John_Edwards_(Kentucky_politician)") # year - year

#page_url == "https://en.wikipedia.org/wiki/Samuel_Smith_(Pennsylvania_politician)": #(before year - year)

# get_politician_bday("https://en.wikipedia.org/wiki/William_Smith_(South_Carolina_senator)") #has "c. [year]"



page_url = "https://en.wikipedia.org/wiki/Kevin_McCarthy"
wiki_wiki = wikipediaapi.Wikipedia('Congress Wiki Project(dustintran36@gmail.com)', 'en')
page_title = page_url.split("wiki/")[1]
page_title = urllib.parse.unquote(page_title)
page_py = wiki_wiki.page(page_title)
# summary_text = page_py.summary
# print(len(summary_text))
# print(summary_text)

# print(persons_wiki.get_valid_index_range_for_summary_text(summary_text))
# a, b = persons_wiki.get_valid_index_range_for_summary_text(summary_text)
# print(a)
# print(b)
# print(persons_wiki.get_politician_data(page_url, congress_num=100, congress_start_date=None))



# print(page_py.sections[1])

# print(persons_wiki.get_sex_from_wiki_page(page_py, 66))
# print(persons_wiki.get_all_wiki_text_by_section(page_py.sections[0:3]))



    # if len(summary_text) == 0:
    #     response = requests.get(page_url)
    #     soup = BeautifulSoup(response.content, 'html.parser')
    #     summary_text = next(p.get_text() for p in soup.find_all("p") if len(p.get_text()) > 75)
    #     summary_text = summary_text[:200] #get substring for faster processing and other issues
    #     print("Using html request for: " + page_url)