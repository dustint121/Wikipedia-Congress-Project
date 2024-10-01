import persons_wiki
import wikipediaapi
import urllib.parse
import boto3
from dotenv import load_dotenv
import os
import json
#This file is just for testing use-cases.

#edge cases: DONE
# "https://en.wikipedia.org/wiki/William_Shepard" #3 dates
#https://en.wikipedia.org/wiki/Jacob_Hibshman  ; additional text in front
#"https://en.wikipedia.org/wiki/John_Paterson_(New_York_politician)": #a pair of preceding parenthesis

#"https://en.wikipedia.org/wiki/Henry_William_Connor" #dates after parentheses can mess things up; will not get most accurate
#page_url == "https://en.wikipedia.org/wiki/Doug_Lamborn": #having "born" in name messes up function

#https://en.wikipedia.org/wiki/Thomas_Terry_Davis #has the word before

#"https://en.wikipedia.org/wiki/John_Steele_(North_Carolina_politician)", #24 when serving congress

#"https://en.wikipedia.org/wiki/Dennis_Ch%C3%A1vez" #encrypted URL; should be handled before going into politician data funtion
# 
# ext length considerations below
# "https://en.wikipedia.org/wiki/Philip_Key_(U.S._politician)"  #summary text is only 96 characters
# "https://en.wikipedia.org/wiki/John_Sevier" #there is another text before sumamry text that is 73 characters

# page_url = "https://en.wikipedia.org/wiki/John_Morrow_(Virginia_politician)" #need first set of parenthesis, not second




#close gender determination at first 50 words
# page_url = "https://en.wikipedia.org/wiki/Robert_L._Owen" #has a paragraph dedication to mom
# page_url = "https://en.wikipedia.org/wiki/Leslie_Jasper_Steele" #not that many words; male


#interesting cases; not relevant to project
#https://en.wikipedia.org/wiki/Winnifred_Mason_Huck #third women in congress for 67th congress; unconsidered due to being a replacement
#https://en.wikipedia.org/wiki/Mae_Nolan #replaced her husband;
#https://en.wikipedia.org/wiki/Edith_Nourse_Rogers #replaced her husband;
#https://en.wikipedia.org/wiki/Effiegene_Wingo  #replaced her husband for 1st time in Congress
#https://en.wikipedia.org/wiki/Willa_Blake_Eslick #replaced her husband; unconsidered
#https://en.wikipedia.org/wiki/Marian_W._Clarke #replaced her husband; unconsidered
#https://en.wikipedia.org/wiki/Elizabeth_Hawley_Gasque  #replaced her husband; unconsidered
#https://en.wikipedia.org/wiki/Clara_G._McMillan #replaced her husband; unconsidered
#https://en.wikipedia.org/wiki/Frances_P._Bolton #replaced her husband;
#https://en.wikipedia.org/wiki/Katharine_Byron #replaced her husband; unconsidered
#https://en.wikipedia.org/wiki/Elizabeth_Kee #replaced her husband; unconsidered
#https://en.wikipedia.org/wiki/Vera_Buchanan #replaced her husband
#https://en.wikipedia.org/wiki/Elizabeth_P._Farrington #replaced her husband
#https://en.wikipedia.org/wiki/Irene_Baker    #replaced her husband; unconsidered
#https://en.wikipedia.org/wiki/Lera_Millard_Thomas #replaced her husband; unconsidered
#https://en.wikipedia.org/wiki/Elizabeth_B._Andrews #replaced her husband; unconsidered
#https://en.wikipedia.org/wiki/Cardiss_Collins #replaced her husband;
#https://en.wikipedia.org/wiki/Shirley_Neil_Pettis #replaced her husband;
#https://en.wikipedia.org/wiki/Jean_Spencer_Ashbrook #replaced her husband; unconsidered
#https://en.wikipedia.org/wiki/Sala_Burton #replaced her husband;
#https://en.wikipedia.org/wiki/Catherine_Small_Long #replaced her husband;
#https://en.wikipedia.org/wiki/Jo_Ann_Emerson #replaced her husband;
#https://en.wikipedia.org/wiki/Lois_Capps #replaced her husband in 1998
#https://en.wikipedia.org/wiki/Doris_Matsui #replaced her husband in 2005
#https://en.wikipedia.org/wiki/Niki_Tsongas #replaced her husband in 2007
#https://en.wikipedia.org/wiki/Julia_Letlow #replaced her husband in 2021
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



page_url = "https://en.wikipedia.org/wiki/William_Shepard"
wiki_wiki = wikipediaapi.Wikipedia('Congress Wiki Project(dustintran36@gmail.com)', 'en')
page_title = page_url.split("wiki/")[1]
page_title = urllib.parse.unquote(page_title)
page_py = wiki_wiki.page(page_title)
# summary_text = page_py.summary
# print(len(summary_text))
# print(summary_text)


# for s in page_py.sections:
#     print(s.title)

# print(page_py.sections[1])

# print(persons_wiki.get_sex_from_wiki_page(page_py, 66, page_url))
# print(persons_wiki.get_all_wiki_text_by_section(page_py.sections[0:3]))

# print(persons_wiki.get_politician_data(page_url,None,43))

    # if len(summary_text) == 0:
    #     response = requests.get(page_url)
    #     soup = BeautifulSoup(response.content, 'html.parser')
    #     summary_text = next(p.get_text() for p in soup.find_all("p") if len(p.get_text()) > 75)
    #     summary_text = summary_text[:200] #get substring for faster processing and other issues
    #     print("Using html request for: " + page_url)


load_dotenv()
# LAMBDA_API_POINT 
lambda_api_point = os.getenv("LAMBDA_API_POINT") #place a variable, LAMBDA_API_POINT, into .env file with API point to lambda

aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')


# client = boto3.client('lambda', region_name = 'us-west-1',
#                       aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
# payload = {
#         "congress_URL": "https://en.wikipedia.org/wiki/1st_United_States_Congress",
#         "congress_num": 1,
#         "congress_start_date": "March 4, 1789",
#         "use_lambda": False
#         }    
# response = client.invoke(
#     FunctionName="congress_wiki_lambda_parallize",
#     InvocationType='Event',  # Use 'Event' for asynchronous invocation
#     Payload=json.dumps(payload)
# )   

# response = client.invoke(
#     FunctionName="congress_wiki_lambda_parallize",
#     InvocationType='RequestResponse',  # Use 'Event' for asynchronous invocation
#     Payload=json.dumps(payload)
# )   

# response_payload = json.loads(response['Payload'].read())
# print(response_payload)





# payload = {
#         "congress_URL": "https://en.wikipedia.org/wiki/118st_United_States_Congress",
#         "congress_num": 118,
#         "congress_start_date": "January 3, 2023",
#         "use_lambda": False
#         }  