import json
import sessions_wiki
import MySQLdb
import os
from dotenv import load_dotenv
from datetime import datetime

# Loads Enviroment Variables from .env file use command: 'touch .env' to create
load_dotenv()

PORT = int(os.getenv("PORT"))
DB = os.getenv("DB")
HOST = os.getenv("HOST")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

def drop_tables(conn = None,file_path="sql_files/mysql_cleanup.sql"):
    cursor = conn.cursor()
    with open(file_path) as cleanup:
        drop = cleanup.read()
        cursor.execute(drop)
    print("Dropped Tables")

def build_tables(conn = None,file_path="sql_files/mysql_setup.sql"):
    cursor = conn.cursor()
    with open(file_path) as setup:
        tables = setup.read()
        cursor.execute(tables)
    print("Built Tables")


def insert_data(conn=None):
    cursor = conn.cursor(MySQLdb.cursors.DictCursor) #returns results as dictionaries, instead of tuples like normal
    congress_list = sessions_wiki.get_full_congress_dict()
    states_list = states = [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
        "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
        "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
        "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
        "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
        ]
    chamber_list = ["Senator", "Representative"]
    party_URL_dict = sessions_wiki.get_party_to_URL_dict_fast()

    sql = "INSERT INTO Congress(congress_id, start_date, end_date, URL) VALUES (%s, %s, %s, %s)"
    cursor.executemany(sql, [[congress_num,
                              datetime.strptime(congress_list[congress_num ]["start_date"], "%B %d, %Y").date(), 
                              datetime.strptime(congress_list[congress_num ]["end_date"], "%B %d, %Y").date(),
                              congress_list[congress_num ]["URL"]] 
                             for congress_num in congress_list.keys()])

    sql = "INSERT INTO State(state_name) VALUES (%s)"
    cursor.executemany(sql, [[state] for state in states])

    sql = "INSERT INTO Chamber(seat_type) VALUES (%s)"
    cursor.executemany(sql, [[seat_type] for seat_type in chamber_list])

    sql = "INSERT INTO Party(party_name, URL) VALUES (%s, %s)"
    cursor.executemany(sql, [[party_name, party_URL_dict[party_name]] for party_name in party_URL_dict.keys()])

    congress_num_list = [i for i in range(1,119)]
    #fetchone() return a dictionary, fetchall() returns a tuple/list of dictionary; 
        #returns None and () if there no match respectively
    # process data for Person and Congressperson
    for congress_num in congress_num_list:
        file_location = "json_data/" + "congress" + str(congress_num) + ".json"
        with open(file_location, 'r') as file:
            print("Congress: " + str(congress_num))
            list_of_congressmen_dict = json.load(file)
            for congressmen_dict in list_of_congressmen_dict:
                #need to "decrypt URLs and names?"; unneccessary so far; more testing needed
                name = congressmen_dict["name"]
                URL = congressmen_dict["URL"]
                party = congressmen_dict["party"]
                seat_type = congressmen_dict["type"]
                state = congressmen_dict["state"]

                birth_date = None
                if congressmen_dict["birth_date"] != None:
                    birth_date = datetime.strptime(congressmen_dict["birth_date"], "%B %d, %Y").date()
                death_date = None
                if congressmen_dict["death_date"] != None:
                    death_date = datetime.strptime(congressmen_dict["death_date"], "%B %d, %Y").date()

                age_at_congress = congressmen_dict["age_at_congress"]
                age_at_death = congressmen_dict["age_at_death"]
                sex = congressmen_dict["sex"]
                try:
                    sql = """INSERT INTO Person(name, sex, birth_date, death_date, age_at_death, URL) 
                            VALUES (%s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql, [name, sex, birth_date, death_date, age_at_death, URL])
                except MySQLdb.Error as e: #ignore duplicate data
                    # print(f"Error: {e}")
                    pass

                try:
                    cursor.execute("""SELECT * FROM Person where URL = %s""", [URL])
                    person_id = cursor.fetchone()["person_id"]
                    # print(person_id)
                    state_id = states_list.index(state) + 1      
                    chamber_id = 1 if seat_type == "Senator" else 2
                    


                    party_id = list(party_URL_dict.keys()).index(party) + 1          
                    # [congress_num, ]
                    sql = """INSERT INTO Congressperson(congress_id, person_id, state_id, chamber_id, party_id, age_at_congress) 
                            VALUES (%s, %s, %s, %s, %s, %s)"""
                    
                    #John Brown's seat, orginally in Virginia, becomes part of Kentucky later in same congress
                    if congress_num == 2 and name == "John Brown" and state == "Kentucky": 
                        continue
                    #later elected to Senate in same session
                    elif congress_num == 12 and name == "Joseph Bradley Varnum" and state == "New Hampshire": 
                        continue 
                    #later elected to Senate for new state, away from Massachusetts
                    elif congress_num == 16 and name == "John Holmes" and state == "Maine": 
                        continue 
                    #later elected to Senate in same session
                    elif congress_num == 17 and name == "Caesar A. Rodney" and seat_type == "Senator": 
                        continue 
                    #later elected to Senate in same session
                    elif congress_num == 20 and name == "Daniel Webster" and seat_type == "Senator": 
                        continue
                    #later elected to Senate in same session
                    elif congress_num == 40 and name == "Roscoe Conkling" and seat_type == "Senator": 
                        continue
                    #later elected to Senate in same session
                    elif congress_num == 48 and name == "John E. Kenna" and seat_type == "Senator": 
                        continue
                    #later elected to Senate in same session
                    elif congress_num == 50 and name == "John H. Reagan" and seat_type == "Senator": 
                        continue
                    #later elected to Senate in same session
                    elif congress_num == 53 and name == "John L. Wilson" and seat_type == "Senator": 
                        continue
                    #later elected to Senate in same session
                    elif congress_num == 57 and name == "L. Heisler Ball" and seat_type == "Senator": 
                        continue
                    #later elected to Senate in same session
                    elif congress_num == 59 and name == "Elmer J. Burkett" and seat_type == "Senator": 
                        continue
                    #later elected to Senate in same session
                    elif congress_num == 61 and name == "William Lorimer" and seat_type == "Senator": 
                        continue
                    #later elected to Senate in same session
                    elif congress_num == 63 and name == "John W. Weeks" and seat_type == "Senator": 
                        continue
                    else:
                        cursor.execute(sql, [congress_num, person_id, state_id, chamber_id, party_id, age_at_congress])
                except MySQLdb.Error as e:
                    print(f"Error: {e}")
                    print(URL)
                    # return

    print("Insertions Done")
    conn.commit()

#WE USE THE BELOW LINE FOR ALL PYTHON FILES; OTHERWISE, THEY WILL ALL RUN AS WELL REGARDLESS OF THE FILE WE SPECIFY 
if __name__ == "__main__":
    conn = MySQLdb.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DB)
    drop_tables(conn)
    build_tables(conn)
    insert_data(conn)
    conn.close()


#NOTE: do not use mysql.connector library from pip install mysql-connector-python; has connectivity issues 