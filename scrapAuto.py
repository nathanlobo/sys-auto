import pyautogui as gui
import pyperclip as clip
import PIL
import time, os, random
from myModule import getScrapCount, writeToSpreadsheet

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

def clickArea(images,Timeout):
    callTime = time.time()
    try:
        Timeout = int(Timeout)
    except ValueError:
        Timeout = 0.1
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

def formatTime(timeTaken):
    h = int(timeTaken // 3600)
    m = int((timeTaken % 3600) // 60)
    s = int(timeTaken % 60)
    return h,m,s

def goTobrowser():
    gui.click(605,745)
    gui.sleep(1)

def goToIg():
    gui.hotkey('ctrl','2')

def goToColab():
    gui.hotkey('ctrl','1')

def getSessionId():
    global inspectOpened
    gui.PAUSE = 1
    gui.hotkey('ctrl', '2')
    gui.press('f12')
    inspectOpened = True
    gui.sleep(5)
    gui.click(1066,400) # Click on session id cookie
    gui.doubleClick(1105,640) # double click on session id to select it (select all)
    gui.hotkey('ctrl', 'c')
    sessionID = clip.paste()
    print(f"Returning Session ID: {sessionID}")
    # gui.press('f12')
    return sessionID

def pasteSessionIdToCode(sessionID):
    try:
        sessionID = f"\t\tsession_id = '{sessionID}'\n" # Re-formatting session ID
        gui.hotkey('ctrl', '1') # going to tab 1 on browser
        while True:
            try:
                gui.click(gui.locateOnScreen('images\session_id.png'),clicks=3,interval=.1)
                break
            except gui.ImageNotFoundException:
                gui.moveTo(1355,228)
                gui.scroll(500)
    except gui.ImageNotFoundException:
        raise gui.ImageNotFoundException
    finally:
        clip.copy(sessionID)
        gui.hotkey('ctrl', 'v')

def getCodeOutput():
    gui.moveTo(1355,244) # move to scroll bar # new: moveto run btn and try scrolling
    gui.scroll(10000) # scroll up
    while True:
    # for _ in range(10):
        try:
            x, y = gui.center(gui.locateOnScreen('images\colab_outp_option_btn.png'))#if slow use confidence=0.8
            # random used below to not be caught as Bot at captcha 
            gui.click(x + (random.uniform(30,150)), y + (random.uniform(-8,6)))
            # gui.sleep(random.uniform(0.1,1.0))# not to be detected as Bot
            gui.hotkey('ctrl','a')
            gui.hotkey('ctrl','c')
            codeOutput = clip.paste()
            return codeOutput
        except gui.ImageNotFoundException:
            gui.scroll(-500) # scroll down
            gui.sleep(1)
    

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
    gui.PAUSE = 0.2
    gui.hotkey('ctrl','2')
    gui.click(110,330)
    images = ['images\ig_user_id_box1.png','images\ig_user_id_box2.png'] # id input box imgs
    clickArea(images, Timeout=Timeout) # this finds n clicks area that looks like the images given
    gui.hotkey('ctrl', 'a')
    gui.write(igId) # type insta user id
    gui.click(110,330)
    images = ['images\ig_pw_box1.png','images\ig_pw_box2.png'] # Password box imgs
    clickArea(images, Timeout=Timeout) # this function finds area that look like the images, if found, clicks it
    gui.hotkey('ctrl', 'a')
    gui.write(igPw) # type insta user password
    gui.press('enter')

def getIgStatus(Timeout=0.1):
    # Checks insta status & returns (LoggedIn, LoggedOut, DismissWarning, CaptchaWarning, Loading)
    gui.hotkey('ctrl','2')
    callTime = time.time()
    statuses = [
                [r'images\ig_logo.png', 'Loading'],
                [r'images\login_btn.png', 'LoggedOut'],
                [r'images\insta_word.png', 'LoggedIn'],
                [r'images\ig_b&w_logo.png', 'LoggedIn'],
                [r'images\suspect_auto_warn.png', 'DismissWarning'],
                [r'images\suspect.png', 'DismissWarning']
                ]
    while (callTime-time.time()) <= Timeout:
        for status in statuses:
            try:
                if gui.locateOnScreen(status[0],confidence=0.8):# use region=(81,123, 135, 50)
                    return status[1]
            except gui.ImageNotFoundException:
                pass
    raise gui.ImageNotFoundException

def getBrowserStatus(Timeout=0.1):
    # Checks browser status & returns (Refreshing, NotRefreshing)
    callTime = time.time()
    statuses = [
                [r'images\no_net.png', 'NoNetwork'],
                [r'images\refresh_btn.png', 'NotRefreshing'],
                [r'images\stop_refresh_btn.png', 'Refreshing']
                ]
    while (callTime-time.time()) <= Timeout:
        for status in statuses:
            try:
                if gui.locateOnScreen(status[0], confidence=0.8):
                    return status[1]
            except gui.ImageNotFoundException:
                pass
    raise gui.ImageNotFoundException

def getColabStatus(Timeout):
    try:
        callTime = time.time()
        while (callTime-time.time()) <= Timeout:
            try:
                if gui.locateOnScreen(r'images\colab_run_btn.png'):
                    return 'CodeNotRunning'
            except gui.ImageNotFoundException:
                if gui.locateOnScreen(r'images\colab_red_run_btn.png'):
                    return 'CodeCrashed'
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
        clickArea(['images\ig_logout_btn.png'], Timeout=(Timeout+5))

def dismissWarning(Timeout=1):
    clickArea(['images\dismiss_btn.png'], Timeout=Timeout)
    gui.sleep(1)

def captchaWarning():
    clickArea(['images\ig_captcha_verify.png'])
    gui.sleep(random.randint(3,7))
    clickArea([r'images\next.png'])
    gui.sleep(1)

def chk_all_ig_acc():
    print('inside chk accs function')
    global ig_ids_pws
    # if getIgStatus(1) == 'LoggedIn':
    #     print('ig acc already logged in')
    #     instaLogout(10)
    #     while(getBrowserStatus()=='Refreshing')or(getIgStatus()=='Loading')or(getIgStatus()=='LoggedIn'):
    #         print('waiting')
    #         gui.sleep(0.1)
    for id_pw in ig_ids_pws:
        print(id_pw)
        id = id_pw[0]
        pw = id_pw[1]
        print(f'ID: {id} Pw: {pw}')
        instaLogin(id, pw, 5)
        print('logged in')
        waitFor('LoggedIn') # Verify if LoggedIn
        print('done waiting')
        if getIgStatus() == 'DismissWarning':
            print('dismissing warning')
            dismissWarning()
        instaLogout(10)
        waitFor('LoggedOut')

def chknTackleWarnings():
    igStatus = getIgStatus(5)
    if igStatus == 'DismissWarning':
        dismissWarning()
    # if igStatus == 'CaptchaWarning':
    #     captchaWarning()
    # if igStatus == 'OTP-Verify':
    #     pass

def waitFor(status,Timeout=120):
    if status == 'LoggedIn':
        status = 'LoggedOut'
    elif status == 'LoggedOut':
        status = 'LoggedIn'
    igStatus = getIgStatus()
    callTime = time.time()
    while(getBrowserStatus()=='Refreshing')or((igStatus)=='Loading')or(igStatus==status):
        igStatus = getIgStatus()
        print('waiting')
        gui.sleep(0.5)
        if (time.time())-callTime > Timeout:
            gui.hotkey('ctrl','r')

def beepAlarm(count=1, interval=1, nonStop=False):
    for _ in range(count):
        import winsound
        frequency = 1000
        duration = 1500
        winsound.Beep(frequency, duration)
        time.sleep(interval)

def rptScrapAcc(id,pw):
    while True:
        print(f'ID: {id} Pw: {pw}')
        instaLogin(id, pw, 5)
        waitFor('LoggedIn') # Verify if LoggedIn
        print('logged in')
        if getIgStatus() == 'DismissWarning':
            print('dismissing warning')
            dismissWarning()
        # instaLogout(10)
        # waitFor('LoggedOut')

ig_ids_pws = [
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
    # os.startfile(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
    for id_pw in ig_ids_pws:
        id = id_pw[0]
        pw = id_pw[1]
        instaLogin(id,pw)
        waitFor('LoggedIn')
        chknTackleWarnings()
        waitFor('LoggedIn')
        session_id = getSessionId()
        pasteSessionIdToCode(session_id)
        gui.hotkey('ctrl','enter')
        i=0
        while getColabStatus() == 'CodeRunning':
            if i<=3:
                delay = 10
                i+=1
            else:
                delay = 150
            gui.sleep(delay)
            goToIg()
            gui.hotkey('ctrl','r')
            waitFor('LoggedIn',Timeout=5)
            chknTackleWarnings()
            goToColab()
        if getColabStatus()=='CodeCrashed': #Check for red btn
            beepAlarm(nonStop=True)
        if getColabStatus()=='CodeCompleted':
            # **** getColabOutput FUNCTION NOT YET Created**** 
            colabCodeOutput = getColabOutput()
            write_text_to_file(colabCodeOutput)
            total_userdata = getScrapCount()
            total_profiles = getScrapCount()
    print("\nProgram ended")

# inspectOpened = False

if __name__ == "__main__":
    goTobrowser()
    start = time.time()
    # main() # main not ready to run
    # chk_all_ig_acc()
    print(getCodeOutput())
    end = time.time()
    print(f'\nTime Taken by main: {end - start}\n')
    beepAlarm(1)
    pass