import subprocess
import sys
import schedule
import time
from datetime import datetime
from pynput.keyboard import Key, Controller
import os
import pyautogui

running = True
cont = 0
now = datetime.now()
now = now.strftime("%d-%m-%Y--%H-%M-%S")
# Author: Anth0nyPereira

def tracert(ip, fileName):
    global now
    f = open(fileName, "w")
    proc = subprocess.Popen("tracert " + str(ip), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = proc.stdout.read()
    output = output.decode("utf-8")
    f.write(output)
    f.close()
    
def openTracertFile(fileName):
    ips = []
    f = open(fileName, "r")
    for line in f:
        if not line.split():
            continue
        array = line.split()
        lastElement = array[len(array)-1]
        removingChars = [ "[", "]", "*" ]
        for char in removingChars:
            if char in lastElement:
                lastElement = lastElement.replace(char, "")
        if lastElement != "" and "out" not in lastElement and "complete" not in lastElement and "hop" not in lastElement:
            ips.append(lastElement)
    f.close()
    return ips

def getIpLocation(fileName, lst):
    f = open(fileName, "w")
    for ip in lst:
        proc = subprocess.Popen('curl ipinfo.io/' + str(ip), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = proc.stdout.read()
        output = output.decode("utf-8")
        f.write(output)
    f.close()
    
    
def turnOnVPN(password):
    keyboard = Controller()
    time.sleep(2)
    pyautogui.click(x=1707, y=1048)
    pyautogui.click(x=1707, y=1048)
    time.sleep(2)
    keyboard.type(password)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(5)


def turnOffVPN():
    keyboard = Controller()
    time.sleep(2)
    pyautogui.click(x=1707, y=1048)
    pyautogui.click(x=1707, y=1048)
    time.sleep(2)
    pyautogui.click(x=435, y=590)
    time.sleep(2)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(5)

    '''
    pyautogui.click(x=1601, y=1055)
    time.sleep(1)
    pyautogui.moveTo(1516, 981)
    time.sleep(1)
    pyautogui.click(button='right')
    time.sleep(1)
    pyautogui.click(x=1675, y=963)
    time.sleep(1)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    '''
    
def program():
    global running
    global cont
    global now
    
    if cont == 5:
        running = False
        schedule.cancel_job
    site = sys.argv[1]
    fileName = "tracert-" + site + "-" + now + ".txt"
    
    tracert(site, fileName)
    ipsList = openTracertFile(fileName)
    resultsFileName = "results-" + fileName 
    getIpLocation(resultsFileName, ipsList)
    time.sleep(5)
    
    #VPN
    passArgument = sys.argv[2]
    turnOnVPN(passArgument)
    time.sleep(3)
    
    fileNameVPN = "tracert-VPN-" + site + "-" + now + ".txt"
    tracert(site, fileNameVPN)
    ipsVPNList = openTracertFile(fileNameVPN)
    resultsVPNFileName = "results-" + fileNameVPN
    getIpLocation(resultsVPNFileName, ipsVPNList)
    turnOffVPN();
    cont += 1
    

def main():
    program()
    #schedule.every().day.at("11:30").do(program)
    #schedule.every().hour.do(program)

    #while running:
        #schedule.run_pending()
     #   time.sleep(1)
    
if __name__ == "__main__":
    main() 
