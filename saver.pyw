from datetime import *
import pyautogui
while(True):
        if(pyautogui.locateCenterOnScreen("C:\\Users\\specdrum\\Documents\\python\\sb.png")):
                pyautogui.locateCenterOnScreen("C:\\Users\\specdrum\\Documents\\python\\sfn.png");
                pyautogui.click(pyautogui.locateCenterOnScreen("C:\\Users\\specdrum\\Documents\\python\\sfn.png"));
                pyautogui.typewrite(str(datetime.now()).replace(":","").replace(" ","-"));
                pyautogui.click(pyautogui.locateCenterOnScreen("C:\\Users\\specdrum\\Documents\\python\\sb.png"));
                pyautogui.hotkey('ctrl','shift','s')
                pyautogui.typewrite(str(datetime.now()).replace(":","").replace(" ","-"));
                pyautogui.press('enter')
        if(pyautogui.locateCenterOnScreen("C:\\Users\\specdrum\\Documents\\python\\splice.png")):
                pyautogui.click(pyautogui.locateCenterOnScreen("C:\\Users\\specdrum\\Documents\\python\\splice.png"));
