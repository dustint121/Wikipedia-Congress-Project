import json
import sessions_wiki
import boto3


#Instructions: make a AWS Lambda function with this file as lambda_function.py,
                #persons_wiki.py, sessions_wiki.py, and the html_files directory
    #purpose: use the asynch feature to process individual congresses in parallel, massively saving time

#need to make a Lambda layer for non-built-in independencies like wikipediaapi
    #to do so make a set of folders in this format: python/lib/python3.12/site-packages
        #make sure it is in this exact format; "lib", not "Lib"; otherwise, it won't work.
        #the site-packages is in your virtual environment folder: [venv name]/Lib/site-packages; 
            #copy and paste the site-packages into the "python3.12" folder specified above
    #after, compress everything the "python" folder into a "python.zip" folder and upload as the file for your layer

#also set the timeout to 4 minutes instead of the default 3 seconds, since calls can takes up to 3 minutes
s3 = boto3.client('s3')
def lambda_handler(event, context):
    congress_URL = event.get('congress_URL')
    congress_num = event.get('congress_num')
    congress_start_date = event.get('congress_start_date')
    use_lambda = event.get('use_lambda')
    
    result = sessions_wiki.get_congresspeople_for_a_congress(congress_URL, congress_num, congress_start_date, use_lambda)
    
    bucket_name = "congress-wiki-json"
    file_name = "congress" + str(congress_num) + ".json"
    json_data = json.dumps(result)
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=json_data, ContentType='application/json')
    

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }



#Local python code calling the above lambda function below:

# client = boto3.client('lambda', region_name = 'us-west-1',
#             aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
# payload = {
#         "congress_URL": congress_URL,
#         "congress_num": congress_num,
#         "congress_start_date": congress_start_date,
#         "use_lambda": False
#         }    
# response = client.invoke(
#     FunctionName="congress_wiki_lambda_parallize",
#     InvocationType='Event',  # Use 'Event' for asynchronous invocation
#     Payload=json.dumps(payload)
# )     