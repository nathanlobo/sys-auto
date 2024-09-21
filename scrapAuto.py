import pyautogui as gui
import pyperclip as clip
import PIL
import time, os
from myModule import getScrapCount, analyze, writeToSpreadsheet

def dragSelect(startX, startY, endX, endY):
    gui.moveTo(startX, startY,duration=0.5)
    gui.mouseDown()
    gui.sleep(.5)
    gui.dragTo(endX, endY,duration=0.5)
    gui.mouseUp()
    gui.sleep(.5)

def checkText(file_path, search_text):
    found = 0
    if type(search_text) == list or type(search_text) == tuple :
        countToFind = len(search_text)
    else:
        countToFind = 1
    # print(countToFind)
    for text in search_text:
        # print("inside for loop 1")
        with open(file_path, 'r') as file:
            # print("inside file")
            for line in file:
                if text in line:
                    # print("incrementing")
                    found+=1
    if countToFind == found:
        print('Found all')
        return True

def write_text_to_file(text, file_path='temp.txt'):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Text successfully written to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def clickArea(images, Timeout):
    callTime = time.time()
    while (callTime-time.time()) <= Timeout:
        i=0
        for image in images:
            try:
                button_location = gui.locateOnScreen(images[i])
                # Note that button shade is diff, when login details enter compared to not enter
                if button_location:
                    gui.click(button_location)
                    return
            except gui.ImageNotFoundException:
                i+=1

def goTobrowser():
    gui.click(605,745)
    gui.sleep(1)

def getSessionId():
    gui.PAUSE = 1
    gui.hotkey('ctrl', '2')
    gui.click(1080,490) # click on screen to unselect all other selections
    dragSelect(1080,490, 1040,140)
    gui.hotkey('ctrl', 'c')
    text = clip.paste()
    write_text_to_file(text)
    if checkText('temp.txt', ['shbid', 'csrftoken']) != True:
        gui.press('f12')
    gui.sleep(2)
    gui.click(1066,386) # Click on session id cookie
    gui.doubleClick(1105,640) # double click on session id to select it (select all)
    gui.hotkey('ctrl', 'c')
    sessionID = clip.paste()
    print(f"Returning Session ID: {sessionID}")
    return sessionID

def pasteSessionIdToCode(sessionID):
    gui.PAUSE = 1
    sessionID = f" '{sessionID}'" # Re-formatting session ID
    gui.hotkey('ctrl', '1') # going to tab 1 on browser
    gui.moveTo(1355,244, duration=0.5) # moving to scroll bar
    gui.scroll(5000) # scrolling to the top to paste session id
    gui.moveTo(208,349, duration=0.5)
    gui.click(210,349)
    gui.mouseDown()
    gui.dragTo(867,349, duration=0.7)
    gui.mouseUp()
    clip.copy(sessionID)
    gui.hotkey('ctrl', 'v')

def getCodeOutput():
    gui.moveTo(1355,244) # move to scroll bar
    gui.scroll(5000)
    gui.scroll(-600)
    gui.click(1260,390) # click on code area
    gui.hotkey('ctrl','a')
    gui.hotkey('ctrl','c')
    codeOutput = clip.paste()
    return codeOutput

def dataPushedCount(file_path='textfile.txt'):
    search_texts = ['Users data_pushed', 'profiles_pushed']
    for search_text in search_texts:
        try:
            print("\n" + search_text)
            matched_lines = []
            with open(file_path, 'r') as file:
                for line in file:
                    if search_text in line:
                        # Split the line and take the last element
                        last_number = line.strip().split()[-1]
                        matched_lines.append(last_number)
            if matched_lines:
                # Join the numbers with a plus sign
                print(" + ".join(matched_lines))
                # return " + ".join(matched_lines)
            else:
                print("Text not found in the file.")
                # return "Text not found in the file."
        except FileNotFoundError:
            return f"File '{file_path}' not found."

def instaLogin(igId,igPw,Timeout=None):
        gui.click(110,330)
        images = ['images\ig_user_id_box1.png','images\ig_user_id_box2.png'] # id input box imgs
        clickArea(images, waitTimeOut=Timeout) # this finds n clicks area that looks like the images given
        gui.hotkey('ctrl', 'a')
        gui.sleep(1)
        gui.write(igId) # type insta user id
        gui.sleep(1)
        gui.click(110,330)
        gui.sleep(1)
        images = ['images\ig_pw_box1.png','images\ig_pw_box2.png'] # Password box imgs
        clickArea(images, waitTimeOut=Timeout) # this function finds area that look like the images, if found, clicks it
        gui.hotkey('ctrl', 'a')
        gui.sleep(1)
        gui.write(igPw) # type insta user password
        gui.press('enter')

def getIgStatus(Timeout):
    # Checks insta status & returns (LoggedIn, LoggedOut, DismissWarning, CaptchaWarning, Loading)
    try:
        callTime = time.time()
        while (callTime-time.time()) <= Timeout:
            try:
                if gui.locateOnScreen(r'images\ig_logo.png'):
                    return 'Loading'
            except gui.ImageNotFoundException:
                if gui.locateOnScreen(r'images\login_btn.png'):
                    return 'LoggedOut'
            except gui.ImageNotFoundException:
                    return 'LoggedIn'
    except gui.ImageNotFoundException:
            return 'CouldNotGetStatus: Hint-Increase Timeout'
        
def instaLogout(Timeout=None):
    gui.hotkey('ctrl', '2')
    try:
        gui.locateOnScreen('images\ig_more2.png') # Checking for Bolded More Btn: 3 Bold lines-horizontal
    except gui.ImageNotFoundException:
        # print('Doing Except of logout')
        clickArea(['images\ig_more1.png'], Timeout=Timeout)
        gui.moveTo(680,320) # move out of area (at centre) coz holding at same position highlights alt text 
    finally:
        clickArea(['images\ig_logout_btn.png'], waitTimeOut=(Timeout+5))

def dismissWarning(Timeout=None):
    clickArea(['images\dismiss_btn.png'], waitTimeOut=Timeout)

ig_ids_pws= [
            ['fast_n_furious.fanpage','nani@lobro22$123456489'],
            ['paulwalker_speed','nanilobro22123456789'],
            ['nl.ig.work1','nanilobro22'],
            ['nl.ig.work2','nanilobro22'],
            ['thenonameguy22','nani@lobro22%123456789'],
            ['mrs_big_boss365','nani@lobro22$123456489'],
            ['jbl_unbreakable','jblbroken'],
            ['mr_meta_nl_123','nlme@2209'],
            ['nathanlobo123','2209@nopass@123'],
            ['the_coconut_tree_365','natuhere@22'],
            ['mr.xavier_everywhere','nanilobro22'],
            ['mr_nick_name_nani','qwerty123456789'],
            ['nl_notfound.404','nanilobro22.404'],
            ['911_or_bmw','bmwormercedes'],
            ['_onlyme.22_','loloretu'],
            ['fake_roaster_22.me','fakeroasteracc'],
            ['mr.natu.me','natulobo22']
            ]

def main():
    goTobrowser()
    gui.hotkey('ctrl', '2')
    # gui.hotkey('ctrl', 'shift', 'r')
    # gui.hotkey('ctrl', 'r')
    print(getIgStatus(2))
    # instaLogin(igId,igPw)
    # dismissWarning()
    # sessionID = getSessionId()
    # pasteSessionIdToCode(sessionID)
    # gui.hotkey('ctrl', 'enter')
    # codeOutput = getCodeOutput()
    # write_text_to_file(codeOutput)
    # analysis = a.analyze('temp.txt')
    # if analysis == 'ErrorXCodeCompleted':
    #     print('printed from if')
        # userCount = getScrapCount()[0]
        # profileCount = getScrapCount()[1]
        # print(f'{userCount}, {profileCount}')
        # if userCount != 'TextNotFound' and userCount != 'FileNotFound':
        #     userCount = userCount.split('+')
        #     tempVal = 0
        #     for count in userCount:
        #         tempVal+=int(count)
        #     userCount = tempVal
        # else:
        #     print('User Scrap Count Not Found')
        # if profileCount != 'TextNotFound' and profileCount != 'FileNotFound':
        #     profileCount = profileCount.split('+')
        #     tempVal = 0
        #     for count in profileCount:
        #         tempVal+=int(count)
        #     profileCount = tempVal
        # else:
        #     print('Profile Scrap Count Not Found')
        # print(f'{userCount}, {profileCount}')
        # writeToSpreadsheet(userCount, profileCount)
    # elif analysis == 'ErrorXCodeActiveORCrashed':
    # if gui.locateOnScreen('images\colab_run_btn.png'):
    #     print('Run button exist')
    # use gui image location to check if code stop running scroll to top check if run btn avaible or not then further decide0
    #     print('printed from elif')
    
    # else:
    #     print('Unknown Error Occured at Analyze')
    print("\nProgram ended")

if __name__ == "__main__":
    main()

    import winsound
    frequency = 1000
    duration = 1500
    winsound.Beep(frequency, duration)
    pass