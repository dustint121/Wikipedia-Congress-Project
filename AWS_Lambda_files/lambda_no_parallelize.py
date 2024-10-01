import json
import persons_wiki

#Instructions: make a AWS Lambda function with this file and persons_wiki.py
    #purpose: use the multiple servers/machines behind AWS Lambda to bypass local systems API limits

#need to make a Lambda layer for non-built-in independencies like wikipediaapi
    #to do so make a set of folders in this format: python/lib/python3.12/site-packages
        #make sure it is in this exact format; "lib", not "Lib"; otherwise, it won't work.
        #the site-packages is in your virtual environment folder: [venv name]/Lib/site-packages; 
            #copy and paste the site-packages into the "python3.12" folder specified above
    #after, compress everything the "python" folder into a "python.zip" folder and upload as the file for your layer

#also set the timeout to 5 seconds instead of the default 3 seconds
def lambda_handler(event, context):
    args = json.loads(event["body"])
    URL = args['URL']
    congress_start_date = args['congress_start_date']
    congress_num = args['congress_num']

    result = persons_wiki.get_politician_data(URL, congress_start_date, congress_num)
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }





#Local python code calling the above lambda function below:

# load_dotenv()
# lambda_api_point = os.getenv("LAMBDA_API_POINT") #place a variable, LAMBDA_API_POINT, into .env file with API point to lambda

# payload = {
#     "URL": URL,
#     "congress_start_date": congress_start_date,
#     "congress_num": congress_num
#     }

# headers = {'Content-Type': 'application/json'}
# result = requests.post(lambda_api_point, data=json.dumps(payload))
# new_data = result.json()
# if result.status_code != 200:
#     print("Status code not 200: " + str(result.status_code))
#     return