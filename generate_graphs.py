import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
import shutil

# Connect to Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
client = gspread.authorize(credentials)


# Open the spreadsheet and select the worksheet
spreadsheet_name = 'test1'
worksheet_name = 'Sheet1' # Change this to the actual name of your worksheet
worksheet = client.open(spreadsheet_name).worksheet(worksheet_name)

# Get all records from the worksheet
records = worksheet.get_all_records()

# Extract the required columns
columns = ["1)Articulation -  Effective communication and clarity in explanation",
           "2) Class Control: Enforcement of discipline in the class to engage the students",
           "3) Helping Attitude Availability- accessibility and approachability for clarifications/ any help/suggestions",
           "4)Subject Command-  Preparedness and depth of subject knowledge, connecting to current practical relevance, wherever applicable.",
           "5)Time Management - Regularity and timely coverage of syllabus, assignments, seminar, class tests, etc",
           "6) Teaching Aid-Effective usage of blackboard, PPTs,  models, practical touch, different teaching methods, and pedagogical initiatives",
           "7) Enhanced Learning-  Invites questions and encourage thinking with motivation",
           "8) Subject Resources- Providing study materials such as lecture notes, handouts, PPTs, video, web link, etc.",
           "9) Assessment- Evaluation of tests/assignments/seminar/quiz with suggestions for improvement"]

data = pd.DataFrame.from_records(records)[["Email address"] + columns]

# Convert ratings to numerical values
data[columns] = data[columns].apply(lambda x: pd.to_numeric(x.str[0]), axis=1)

# Calculate the average rating for each criterion
averages = data[columns].mean()

# Delete the 'graphs' folder if it exists
if os.path.exists('graphs'):
    shutil.rmtree('graphs')


# Create a pie chart for each criterion and save it to a file
for i, (criterion, average) in enumerate(averages.iteritems()):
    # Extract the criterion number from the column name
    criterion_number = re.search(r'\d+', criterion).group()
    counts = data[criterion].value_counts()
    labels = [f"{rating}-{'Excellent' if rating == 5 else 'Good' if rating == 4 else 'Satisfactory' if rating == 2 else 'Unsatisfactory' if rating == 1 else 'Poor'}" for rating in counts.index]
    sizes = counts.values
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title(criterion)
    # Create a new directory to store the graphs if it doesn't exist
    directory = 'graphs'
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Save the graph with the criterion number as the filename
    filename = f"{directory}/{i+1}.png"
    plt.savefig(filename)
    plt.close()

