import pyautogui
import keyboard  # For detecting key presses
import time

# Function to handle clicking on a link, writing file path, and pressing Enter
def handle_link(link):
    # Simulate waiting for Alt key press (using a different method for demonstration)
    keyboard.wait('delete')

    # Select the address bar and clear it (Ctrl + L, Ctrl + A, Delete)
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')

    # Type the link URL and press Enter
    pyautogui.write(link)
    pyautogui.press('enter')

    # Optional: Add a delay to allow the page to load before moving on
    time.sleep(5)  # Adjust as needed

# Start listening for Enter key presses (optional)
keyboard.wait('enter')

# List of links to handle (replace with your actual links)
links = [
    "https://www.amazon.se/sspa/click?ie=UTF8&spc=MTo1MjgxOTk3MTE3MTc2OTU1OjE3MjEzMTk2NTI6c3BfYXRmX2Jyb3dzZTozMDAxNzMwNzc0NjgwMzI6OjA6Og&url=%2FSmartphone-Mobiltelefon-1440x3200P-H%25C3%25B6guppl%25C3%25B6st-L%25C3%25A5ngvarigt%2Fdp%2FB0B6G9T4QF%2Fref%3Dsr_1_1_sspa%3Fdib%3DeyJ2IjoiMSJ9.49j_jjPKYjrD7-t8Arhwy4hzOSRNouFqya1NcaEbudXhaSoBWr8NbPnWdTEcAbd8wb_1cS2GTLlZ6gV0wlX27RnCjb8L1xro9h-31UnwF2HsVA9q7xITot1wVVJ9Ns9S5vwgZKbKtB3R5PweBwS6BYrNbLXaZRkAAEn8qmIK9af54uJ_MrdRRxEpYYmkmtbn-i0ch8DGQwwvVkljkylCk1PUfkAPXkC-UTp2vnTQaZqkMsgN7Xx_76ml79rkS2NORc_-d37dhp4l5u3r60FaVTKgn1Qt48UJPPwCahDXcps.JAqR5g5vNwkSWNIzCy8gGNQBMSR8WvzdZRIFuSzZ96M%26dib_tag%3Dse%26qid%3D1721319652%26s%3Delectronics%26sr%3D1-1-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGZfYnJvd3Nl%26psc%3D1",
    "https://www.amazon.se/sspa/click?ie=UTF8&spc=MTo1MjgxOTk3MTE3MTc2OTU1OjE3MjEzMTk2NTI6c3BfYXRmX2Jyb3dzZTozMDAxNTE3Mjk0NTE4MzI6OjA6Og&url=%2FMobiltelefon-Seniorer-L%25C3%25A4ttanv%25C3%25A4nd-SOS-knapp-16800mAh%2Fdp%2FB0BCKZ1RTD%2Fref%3Dsr_1_2_sspa%3Fdib%3DeyJ2IjoiMSJ9.49j_jjPKYjrD7-t8Arhwy4hzOSRNouFqya1NcaEbudXhaSoBWr8NbPnWdTEcAbd8wb_1cS2GTLlZ6gV0wlX27RnCjb8L1xro9h-31UnwF2HsVA9q7xITot1wVVJ9Ns9S5vwgZKbKtB3R5PweBwS6BYrNbLXaZRkAAEn8qmIK9af54uJ_MrdRRxEpYYmkmtbn-i0ch8DGQwwvVkljkylCk1PUfkAPXkC-UTp2vnTQaZqkMsgN7Xx_76ml79rkS2NORc_-d37dhp4l5u3r60FaVTKgn1Qt48UJPPwCahDXcps.JAqR5g5vNwkSWNIzCy8gGNQBMSR8WvzdZRIFuSzZ96M%26dib_tag%3Dse%26qid%3D1721319652%26s%3Delectronics%26sr%3D1-2-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGZfYnJvd3Nl%26psc%3D1"
    # Add more links as needed
]

for link in links:
    handle_link(link)
