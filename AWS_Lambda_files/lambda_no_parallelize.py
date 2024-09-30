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


#video tutorial: https://www.youtube.com/watch?v=I13FPeC5LTw
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
