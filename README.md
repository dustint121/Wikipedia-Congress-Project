# About
My project repo for webscraping Wikipedia for United States Congress data from nearly 250 years (1789-2023) to later analyze the Tableau project: [here.](https://public.tableau.com/app/profile/dustin.tran.d/viz/USCongressProject/NumberofCongresspeopleOverTime)

This project was initially ran fully using the local machine but faced API request limits for a single machine. **AWS Lambda** is used to overcome this limit by distributed its request over multiple machines. 
Later, Lambda is also used for asynchronous function calls to make more efficient use of time, dropping the time to run the code from 6 hours to under 30 minutes. 
The code used for AWS Lambda is store in the 
'AWS_Lambda_files' folders.

This projects uses Python, AWS(S3 and Lambda), MySQL, and Tableau.


# Instructions for Running Code Repo on Local Machine

## In Project File after git cloning

1. Add **.env** file for MySQL connection information and AWS connection information.


>USER= [MySQL username]

>PASSWORD=[MySQL password]

>PORT=[MySQL port]

>DB= [MySQL database name]

>HOST= [MySQL Host]

>LAMBDA_API_POINT = [AWS Lambda URL for function]

>AWS_ACCESS_KEY_ID = [AWS access key]

>AWS_SECRET_ACCESS_KEY = [AWS secret key value]

2. Run
>`pip install -r requirements.txt`

3. Run
>`python sessions_wiki.py `

**Note**: There are 2 variables you can manually change in the code.
* use_lambda = [True/False] # decides whether you use code/URL using AWS Lamdba (overcomes local machine limit for API requests)
* lambda_parallelize = [True/False] # if using Lamdba, determines if you are storing the resulting json files asynchronously (through parallelize function calls) into a AWS S3 bucket or locally on your machine.
