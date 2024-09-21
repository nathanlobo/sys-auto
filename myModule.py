def getScrapCount(search_texts, stats=True,file_path='temp.txt'):
    def calculate_list_stats(items):
        from collections import Counter
        if not items:
            return "The list is empty"
        try:
            intOfItems = []
            for item in items:
                intOfItems.append(int(item))
            
            total_sum = sum(intOfItems)
            list_count = len(intOfItems)
            most_common = (Counter(intOfItems)).most_common(1)
            max_item = max(intOfItems)
            min_item = min(intOfItems)

            return {
                'sum': total_sum,
                'list_count': list_count,
                'most_common': most_common,
                'max': max_item,
                'min': min_item
            }
        except TypeError or ValueError:
            return 'List Consist Non Numerical Value'
        except Exception as e:
            return f'Error: {e}'

    def findText(search_text):
        try:
            matched_lines = []
            with open(file_path, 'r') as file:
                for line in file:
                    if search_text in line:
                        # Split the line and take the last element
                        last_number = line.strip().split()[-1]
                        matched_lines.append(int(last_number))
            
            if matched_lines:
                result = ''
                for line in matched_lines:
                    result = result + "+" + (str(line))
                output = {}
                output.update({'count':result})
                if stats:
                    output.update(calculate_list_stats(matched_lines))
                return output
            else:
                return "TextNotFound"
        except ValueError:
            return 'List Consist Non Numerical Value'
        except FileNotFoundError:
            return "FileNotFound"
    
    result = []
    for search_text in search_texts:
        result.append(findText(search_text))
    return result



def analyze(file_path):
    def dataPushed(file_path):
        search_found = [False,False] # Both in array are default false coz search text not found
        i=0
        search_texts = ['Users data_pushed', 'profiles_pushed']
        for search_text in search_texts:
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        if search_text in line:
                            search_found[(i)] = True
                i+=1
            except Exception as e:
                print(f"An error occurred: {e}")
        if (search_found[0] == True) or (search_found[1] == True):
            return True
        else:
            return False
    
    def get_last_words(file_path):
        last_words = []
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    words = line.split()
                    if words:  # If the line is not empty
                        last_words.append(words[-1])
                    else:  # If the line is empty
                        last_words.append('EMPTY_LINE')
            return last_words
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    last_words = get_last_words(file_path)
    previousScrapCount = None
    lineNo = 1
    continuousErrorCount = 1 
    ErrorLine = 0
    MAX_ERROR = 11
    for last_word in last_words:
        currentScrapCount = None
        try:
            currentScrapCount = int(last_word)
        except ValueError:
            if "\'user\'" in last_word:
                # print(f"{lineNo} Found \'user\' word")
                pass
            elif "EMPTY_LINE" in last_word:
                # print(str(lineNo) + " THIS_IS_AN_EMPTY_LINE" + "-"*80)
                pass
            else:
                # print(f"{lineNo} Error UnknownWordFound: {last_word}")
                pass
        if currentScrapCount != None:
            # print(f"{lineNo} Last num updated, Maybe scrap count")
            pass
            if previousScrapCount == currentScrapCount:
                ErrorLine = lineNo
                if ErrorLine == (lineNo):
                    continuousErrorCount+=1
            else:
                continuousErrorCount = 1
            # print(f"Error on LineNo {lineNo}, Continuous Error Count: {continuousErrorCount}")
            if continuousErrorCount == MAX_ERROR:
                if dataPushed(file_path):
                    # print('ErrorXCodeCompleted')
                    return 'ErrorXCodeCompleted'
                else:
                    # print('ErrorXCodeActiveORCrashed')
                    return 'ErrorXCodeActiveORCrashed'
            previousScrapCount = currentScrapCount
        lineNo+=1

def writeToSpreadsheet(userCount, profileCount, spreadsheet_name="vhub_earnings_expt", sheet_name = "Sheet3"):
    from oauth2client.service_account import ServiceAccountCredentials
    import gspread
    import pytz
    from datetime import datetime

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("price-checker.json", scope)
    client = gspread.authorize(creds)

    spreadsheet = client.open(spreadsheet_name)
    sheet = spreadsheet.worksheet(sheet_name)

    all_values = sheet.get_all_values()

    timezone_str = 'Asia/Kolkata'
    timezone = pytz.timezone(timezone_str)
    current_datetime = datetime.now(timezone)
    current_date_str = current_datetime.strftime("%Y-%m-%d")

    date_found = False

    # Iterate through the rows to check if the current date exists
    for i, row in enumerate(all_values):
        if len(row) > 0 and row[1] == current_date_str:  # Check if the row is not empty and the first column matches the date
            date_found = True
            if len(row) >= 3:  # Ensure the row has at least 3 columns
                existingScrapC = int(row[2])
                existingProfileC = int(row[3])
                newUserCount = existingScrapC + userCount
                newProfileCount = existingProfileC + profileCount
                i=i+1
                sheet.update_cell(i, 3, newUserCount)
                sheet.update_cell(i, 4, newProfileCount)
                print(f"Updated row {i}: {newUserCount}, {newProfileCount}")
            else:
                i=i+1
                sheet.update_cell(i, 3, userCount)
                sheet.update_cell(i, 4, profileCount)
                print(f"Updated row {i} with new values {userCount}, {profileCount}")
            break

    if not date_found:
        # If the current date is not found, write a new row with the date and additional value (no time)
        data_to_write = ['', current_date_str, userCount, profileCount]
        sheet.append_row(data_to_write)
        print(f"Appended new row: {data_to_write}")

# getScrapCount()
# writeToSpreadsheet(0, 0)