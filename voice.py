from ctypes import resize
from email import message
from urllib import request
import pyttsx3
import datetime
import speech_recognition as sr
import smtplib
#from info import sendermail, epwd # mail yollama
from email.message import EmailMessage
import pyautogui
import webbrowser as wb
from time import sleep
import wikipedia
import pywhatkit
import requests
import clipboard
import os
import pyjokes
import time as tt
import string
import random
import psutil
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup


engine = pyttsx3.init()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()    

def getvoices(voice):
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    newVoiceRate = 120
    #print(voices[0].id)
    if voice == 1:
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', newVoiceRate)        
        speak('Hello, I am Emily')

    if voice == 2:
        engine.setProperty('voice', voices[1].id)  
        engine.setProperty('rate', newVoiceRate)  
        speak('Hello, I am Bumblebee')

def timeStr():
    Time = datetime.datetime.now().strftime('%I:%M') 
    timeStr = "The current time is: "+ Time
    return timeStr

def dateStr():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    today = datetime.datetime.now()    
    return (f'The current date is: {date} {month} {year}')

def greetingStr():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        return('Good morning!')
    elif hour >= 12 and hour < 18:
        return('Good afternoon!')
    elif hour >=18 and hour < 24:
        return('Good evenning!')
    else:
        return('Good night!')

def wishme():
    speak('Velcome back user.')
    time()
    date()
    speak('Assistant at your service, please tell me how can I help you?')

def takeCommandMIC():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print('Recognizning...')
        query = r.recognize_google(audio, language="en-US")
        print(query)
    except Exception as e: 
        print(e)
        speak('Can you say it again please?')
        return ""
    return query

def sendEmail(receiver, subject, content):
    server = smtplib.SMTP('smtp.gmail.com', 587) 
    server.starttls() # tls: transport layer security
    server.login(sendermail, epwd)
    email = EmailMessage()
    email['From'] = sendermail
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(content)
    server.send_message(email)
    server.close()

def sendwhatsappmsg(phone_no, message):
    Message = message
    wb.open('https://web.whatsapp.com/send?phone=' + phone_no + '&text=' + Message)
    sleep(10)
    pyautogui.press('enter')

def searchgoogle():
    speak('What sould ı search for?')
    search = takeCommandMIC().replace(' ','+')
    wb.open('https://www.google.com/search?q=' + search)

def weatherStr(cityName):
  
    url = f'https://www.google.com/search?q={cityName}+weather&hl=en'        
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content,'html.parser')
    table = soup.find_all('div',{'class':'nawv0d'})
    # Today
    liste = []

    city_name = table[0].find('div',{'id':'wob_loc'}).text
    temperature_c = table[0].find('span',{'class':'wob_t TVtOme'}).text
    temperature_f = table[0].find('span',{'id':'wob_ttm'}).text
    celsius = table[0].find('span',{'aria-label':'°Celsius'}).text
    fahrenheit = table[0].find('span',{'aria-label':'°Fahrenheit'}).text
    weather_event = table[0].find('span',{'id':'wob_dc'}).text

    forOneDay = ""+ city_name +" | "+ temperature_c +" "+ celsius +" | "+ temperature_f +" "+ fahrenheit +" | "+ weather_event
    speak(forOneDay)
    for i in range (1, 4):
        week = table[0].find('div',{'data-wob-di':i}) 
        day_name = week.find("div", {"class":"QrNVmd Z1VzSb"})["aria-label"]
        day_weather = week.find("img", {"class":"uW5pk"})["alt"]
        day_temp = week.find("span", {"class":"wob_t"}).text
        
        forthreeDay =  ""+ day_name +" | "+ day_weather +" | "+ day_temp 
        
        liste.append(forthreeDay)
        
    forWeather = "Today\n<br>"+forOneDay +"\n\n<br><br>Three Days<br>\n"+ liste[0] +"\n<br>"+ liste[1] + "\n<br>" +liste[2]

    return forWeather

def imdb():
    url = "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm"

    try:
        response = requests.get(url).content
        soup = BeautifulSoup(response, "html.parser")

        list = soup.find("tbody", {"class":"lister-list"}).find_all("tr", limit = 5)

        liste = []
        text = ""
        
        for info in list:
            title = info.find("td", {"class":"titleColumn"}).find("a").text
            year = info.find("td", {"class":"titleColumn"}).find("span").text
            
            text = title + year

            liste.append(text)

        random.shuffle(liste)

        result_1 = (f"You can watch {liste[0]}")
        result_2 = (f"and you can check out these movies:<br><br>{liste[1]}<br>{liste[2]}<br>{liste[3]}<br>{liste[4]}")

        speak(result_1)

    except Exception as ex:
        print(ex)
        print("please try again")

    return result_1 +"<br>"+ result_2

def news():
    url = 'https://breakingnewsenglish.com/'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content,'html.parser')
    title = soup.find_all('h3')
    date = soup.find_all('div', {'class':'smallfont'})
    content = soup.find_all('div', {'class':'content'})

    t =[]
    l =[]

    for i in range(3,12):
        news_title = (title[i].text)
        news_link = title[i].contents[0].get('href')     

        t.append(news_title)
        l.append(news_link)
        

    d = []
    c = []

    for i in range(9):
        news_date = (date[i].text)
        news_content = (content[i].text)

        
        d.append(news_date.replace('"Easier"',"").replace('-','').replace('"Harder"',""))
        c.append(news_content)



    return('NEWS\n<br>'+ t[0] + '\n<br>' + d[0] + '\n<br>' + c[0] + '\n<br>' + 
    t[1] + '\n<br>' + d[1] + '\n<br>' + c[1])

def texttospeech():
    text = clipboard.paste()
    print(text)
    return str(text)

def covid():
    url='https://www.haberler.com/koronavirus/'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content,'html.parser')

    table = soup.find_all('tr',{'class':'turkey'})
    table2 = soup.find_all('tr',{'class':'other'})

    a=[]
    for i in range(1,9):
        a.append(table[0].contents[i].text)

    speak("Country: " + a[0] + "\nNew Cases: " + a[2] + "\nNew Deaths: " + a[4] + '\n')

    result1 = ('Detailed Data About ' + a[0] + "\n<rb>Total Cases: " + a[1] + "\n<rb>Total Deaths: " + a[3] +  "\n<br>Total Recovered: " + a[5] + "\n<rb>Active Cases: " + a[6] +'\n<br>')

    b=[]
    for i in range(1,9):
        b.append(table2[0].contents[i].text)

    result2 = ('\n' + 'Detailed Data About ' + b[0] + "\n<br>Total Cases: " + b[1] +  "\n<br>Total Deaths: " + b[3] + "\n<rb>Total Recovered: " + b[5] )

    return result1+"<br>"+result2
    
def screenshot():
    name_img = tt.time()
    name_img = f'D:\\sesli_asistan_2.dönem_proje\\asistan_deneme_5\\{name_img}.png'
    img = pyautogui.screenshot(name_img)
    img.show()

def screenshotStr():
    name_img = tt.time()
    name_img_two = f'D:\\sesli_asistan_2.dönem_proje\\sesli_asistan\\{name_img}.png'
    img = pyautogui.screenshot(name_img_two)
    name_img_three = str(name_img)
    return name_img_three

def passwordgen():
    s1 = string.ascii_uppercase
    s2 = string.ascii_lowercase
    s3 = string.digits
    s4 = string.punctuation

    passlen = 12

    s = []
    s.extend(list(s1))
    s.extend(list(s2))
    s.extend(list(s3))
    s.extend(list(s4))

    random.shuffle(s)
    newpass = (''.join(s[0:passlen]))
    print(newpass)
    return newpass

def flipcoin():
    speak('Okay, flipping a coin.')
    coin = ['heads', 'tails']    
    toss = []
    toss.extend(coin)
    random.shuffle(toss)
    toss = (''.join(toss[0]))
    result = "I flipped the coin and you got " + toss
    return result

def roll():
    speak('Okay, rolling a die for you.')
    die = ['1', '2', '3', '4', '5', '6']
    roll = []
    roll.extend(die)
    random.shuffle(roll)
    roll = ("".join(roll[0]))
    result = "I rolled a die and you got " + roll
    return result

def cpuStr():
    usage = str(psutil.cpu_percent())
    usage_result = ('CPU is at ' + usage+ ' %<br><br>')
    battery = psutil.sensors_battery().percent
    batery_result = ('Battery is at '+ str(battery))
    return usage_result+""+batery_result+" %"

def location(): 
    url = 'https://www.google.com/search?q=where+%C4%B1+am&oq=where+%C4%B1+am '   
     
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content,'html.parser')
    table = soup.find_all('div',{'class':'vk_c XCwAFc'})

    loc = table[0].find('div', {'class':'desktop-title-content'}).text
    locd = table[0].find('span', {'class':'desktop-title-subcontent'}).text

    return ("You are in now: " + loc + ' | ' + locd)

def euro():    
    url = 'https://www.google.com/search?q=euro&hl=en'      
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content,'html.parser')
    table = soup.find_all('div',{'class':'nRbRnb'})

    miktar = table[0].find('span',{'class':'DFlfde SwHCTb'}).text
    currency  = table[0].find('span',{'class':'MWvIVe'}).text
    beyanname = table[0].find('div',{'class':'hqAUc'}).text

    return ("1 Euro: " + miktar + ' ' + currency + ' ' + beyanname)

def dolar():
    url = 'https://www.google.com/search?q=dolar&hl=en'         
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content,'html.parser')
    table = soup.find_all('div',{'class':'nRbRnb'})

    miktar = table[0].find('span',{'class':'DFlfde SwHCTb'}).text
    currency  = table[0].find('span',{'class':'MWvIVe'}).text
    beyanname = table[0].find('div',{'class':'hqAUc'}).text

    return ("1 ABD Dolar: " + miktar + ' ' + currency + ' ' + beyanname)