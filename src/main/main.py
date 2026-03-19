import csv
import sqlite3

# Connect to the SQLite in-memory database
conn = sqlite3.connect(':memory:')

# A cursor object to execute SQL commands
cursor = conn.cursor()


def main():

    # users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        userId INTEGER PRIMARY KEY,
                        firstName TEXT,
                        lastName TEXT
                      )'''
                   )

    # callLogs table (with FK to users table)
    cursor.execute('''CREATE TABLE IF NOT EXISTS callLogs (
        callId INTEGER PRIMARY KEY,
        phoneNumber TEXT,
        startTime INTEGER,
        endTime INTEGER,
        direction TEXT,
        userId INTEGER,
        FOREIGN KEY (userId) REFERENCES users(userId)
    )''')

    # You will implement these methods below. They just print TO-DO messages for now.
    load_and_clean_users('../../resources/users.csv')
    load_and_clean_call_logs('../../resources/callLogs.csv')
    write_user_analytics('../../resources/userAnalytics.csv')
    write_ordered_calls('../../resources/orderedCalls.csv')

    # Helper method that prints the contents of the users and callLogs tables. Uncomment to see data.
    select_from_users_and_call_logs()

    # Close the cursor and connection. main function ends here.
    cursor.close()
    conn.close()


# TODO: Implement the following 4 functions. The functions must pass the unit tests to complete the project.


# This function will load the users.csv file into the users table, discarding any records with incomplete data
def load_and_clean_users(file_path):

    with open(file_path, "r") as users_file:
    # with open("resources/users.csv", "r") as users_file:
        clean_users = [line.strip() for line in users_file.readlines()]
        all_lines = [tuple(line.split(",")) for line in clean_users]
        columns = all_lines[0]
        rows = all_lines[1:]
        for user in rows:
            if len(user) == 2 and '' not in user:
                cursor.execute(f"INSERT INTO users {columns} VALUES {user}")

# !!!EXPLANATION!!!
# The testCallLogs.csv includes the columns: userId,avgDuration,numCalls
# These columns do not coincide with the callLogs Table columns

# This function will load the callLogs.csv file into the callLogs table, discarding any records with incomplete data
def load_and_clean_call_logs(file_path):

    with open(file_path, "r") as logs_file:
    # with open("resources/callLogs.csv", "r") as logs_file:
        clean_logs = [line.strip() for line in logs_file.readlines()]
        all_lines = [tuple(line.split(",")) for line in clean_logs]
        # columns = all_lines[0]
        # Hard-coding column names because the columns in the testCallLogs.csv are incorrect!
        columns = ("phoneNumber","startTime","endTime","direction","userId")
        rows = all_lines[1:]
        for log in rows:
            if len(log) == 5 and '' not in log:
                cursor.execute(f"INSERT INTO callLogs {columns} values {log}")


# This function will write analytics data to testUserAnalytics.csv - average call time, and number of calls per user.
# You must save records consisting of each userId, avgDuration, and numCalls
# example: 1,105.0,4 - where 1 is the userId, 105.0 is the avgDuration, and 4 is the numCalls.
def write_user_analytics(csv_file_path):
    
    cursor.execute("""SELECT userId, AVG(endTime-startTime) AS avgDuration, count(userId) AS numCalls
                    FROM callLogs
                    GROUP BY userId""")
    results = cursor.fetchall()

    # with open("resources/userAnalytics.csv", "w") as user_file:
    with open(csv_file_path, "w") as user_file:
        columns = "userId,avgDuration,numCalls\n"
        user_file.write(columns)
        for row in results:
            user_file.write(f"{str(row).strip("()")}\n")


# This function will write the callLogs ordered by userId, then start time.
# Then, write the ordered callLogs to orderedCalls.csv
def write_ordered_calls(csv_file_path):

    cursor.execute("SELECT * FROM callLogs ORDER BY userId, startTime")
    results = cursor.fetchall()

    with open(csv_file_path, "w") as file:
    # with open("resources/orderedCalls.csv", "w") as file:
        columns = "callId,phoneNumber,startTime,endTime,direction,userId\n"
        file.write(columns)
        for row in results:
            file.write(f"{str(row).strip("()")}\n")


# No need to touch the functions below!------------------------------------------

# This function is for debugs/validation - uncomment the function invocation in main() to see the data in the database.
def select_from_users_and_call_logs():

    print()
    print("PRINTING DATA FROM USERS")
    print("-------------------------")

    # Select and print users data
    cursor.execute('''SELECT * FROM users''')
    for row in cursor:
        print(row)

    # new line
    print()
    print("PRINTING DATA FROM CALLLOGS")
    print("-------------------------")

    # Select and print callLogs data
    cursor.execute('''SELECT * FROM callLogs''')
    for row in cursor:
        print(row)


def return_cursor():
    return cursor


if __name__ == '__main__':
    main()
