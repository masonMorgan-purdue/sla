#=========================================================------
#***PURPOSE***
#-------------
# Update "program_data.json" to include new program details when
# an SLA employee enters information into the program creation form
#
#***Data required***
#-------------------
# The URL of the creation form to check

import json
import numpy as np
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from authentication import authenticate_google_account

CREATION_FORM_ID = "1GCE8SIKYwvZ8YNni_V0cHsCPmJD9pfps2NY1AjdBOJg"
#Id to the sheet that receives responses from the SLA Program Creation form

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/forms', 'https://www.googleapis.com/auth/spreadsheets']  
#Permissions we request

def get_range(spreadsheet_id, range_name):
    '''
    Retrieves a range from any spreadsheet
    Returns a result which you can access values from with .get("values", [])
    '''
    creds = authenticate_google_account(SCOPES)
    # pylint: disable=maybe-no-member

    try:
        service = build("sheets", "v4", credentials=creds)

        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=range_name)
            .execute()
        )
        rows = result.get("values", [])
        print(f"{len(rows)} rows retrieved")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
    
def read_new_rows(spreadsheet_id):
    '''
    Checks for any new rows in the given spreadsheet and returns the values
    TODO add code to update the completed/uncompleted field in the spreadsheet (Change to TRUE once it has been accessed). Consider having it as a seperate function to be called after the values have been used.
    '''

    #Set the range to all rows and get the values from this range
    range_string = "A2:E"
    result = get_range(spreadsheet_id, range_string)
    all_values = np.array(result.get("values", []))

    #Filter out to new rows
    completed_column = all_values[:, 0]
    values = [all_values[index, 1:].tolist() for index, val in enumerate(completed_column) if val != 'TRUE']

    return values

if __name__ == "__main__":
    values = read_new_rows(CREATION_FORM_ID)
    print(values)