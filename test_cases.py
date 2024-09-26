import persons_wiki
import wikipediaapi
import urllib.parse
#edge cases to work on

# "https://en.wikipedia.org/wiki/William_Shepard" doable but weird
# "https://en.wikipedia.org/wiki/Abram_Trigg" ;broken; fixed; has unknown as date of dead

#https://en.wikipedia.org/wiki/Jacob_Hibshman  ; additional text in front

#text length considerations below
# "https://en.wikipedia.org/wiki/Philip_Key_(U.S._politician)"  #summary text is only 96 characters
# "https://en.wikipedia.org/wiki/John_Sevier" #there is another text before sumamry text that is 73 characters



#test cases below

# "https://en.wikipedia.org/wiki/John_Stewart_(Pennsylvania_politician)" #unknown case
# "https://en.wikipedia.org/wiki/Pleasant_Moorman_Miller" #unknown case
# "https://en.wikipedia.org/wiki/John_Morrow_(Virginia_politician)" #unknown case


# page_url = "https://en.wikipedia.org/wiki/Peter_Silvester_(1734%E2%80%931808)" #has encrypted URL


# print(get_politician_bday("https://en.wikipedia.org/wiki/Oliver_Ellsworth")) #full date to full date
# print(get_politician_bday("https://en.wikipedia.org/wiki/John_Vining")) #has full date to month year
# print(get_politician_bday("https://en.wikipedia.org/wiki/Peter_Van_Gaasbeck")) #full date to year

# get_politician_bday("https://en.wikipedia.org/wiki/John_Henry_(Maryland_politician)") #has "month year to full date"
# get_politician_bday("https://en.wikipedia.org/wiki/Cornelius_C._Schoonmaker") #month year - month year

# print(get_politician_bday("https://en.wikipedia.org/wiki/Andrew_Moore_(politician)"))#year - full date
# print(get_politician_bday("https://en.wikipedia.org/wiki/John_Culpepper"))  #year - month year
# get_politician_bday("https://en.wikipedia.org/wiki/John_Edwards_(Kentucky_politician)") # year - year

# get_politician_bday("https://en.wikipedia.org/wiki/William_Smith_(South_Carolina_senator)") #has "c. [year]"



page_url = "https://en.wikipedia.org/wiki/Davy_Crockett"
wiki_wiki = wikipediaapi.Wikipedia('Congress Wiki Project(dustintran36@gmail.com)', 'en')
# page_title = page_url.split("wiki/")[1]
# print(page_title)
# page_title = urllib.parse.unquote(page_title)
# print(page_title)
# page_py = wiki_wiki.page(page_title)
# summary_text = page_py.summary
# print(len(summary_text))
# print(summary_text)

print(persons_wiki.get_politician_bday(page_url))
