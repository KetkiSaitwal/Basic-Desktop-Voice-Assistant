# Description: tHis is a virtual assistant program that gives date,currenttime, responds back with random greeting and returns information
import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import wikipedia
import random

#Ignore any warning msgs
warnings.filterwarnings('ignore')

#record audio and return audio as string
def recordAudio():

    #Record the audio
    r = sr.Recognizer()#creating a recognizer object

    #Open the microphone and start recording
    with sr.Microphone() as source:
        print("Listening")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    #USe google's speech recognition
    data = '' 
    try:
        data = r.recognize_google(audio)
        print("You said: " +data)
    except sr.UnknownValueError: #check for unknown error
        print("Google Speech recognition could not understand the audio")
    except sr.RequestError as e:
        print("Request results from Google SPeech Recognition service error" +e)
    return data

#recordAudio()

#A function to get the virtual assistant response
def assistantResponse(text):
    print(text)
    
    #Convert the text to speech
    myobj  = gTTS(text = text, lang='en', slow = False) #text =text passed as param to this funct

     #Save the converted audio to a file
    myobj.save('assistant_response.mp3')

     #play the converted file
    os.system('start assistant_response.mp3')

#text = 'This is a test'
#assistantResponse(text)

#A function for wake words for phrase
def wakeWord(text):
    WAKE_WORDS = ['hey computer','okay computer','hi computer'] #A list of wake words

    text = text.lower() #Coverting the text to all lower case words

    #Check if users command/text contains a wake word/phrase
    for phrase in WAKE_WORDS:
        if phrase in text:
            #print("T")
            return True
            
    
    #IF the wake words isn't found in the text from the loop, spo it returns false
    #print("F")
    return False
    

#text = "hey"
#wakeWord(text)

#A funtion to get the current date
def getDate():

    now = datetime.datetime.now()
    myDate = datetime.datetime.today()
    weekday = calendar.day_name[myDate.weekday()] #e.g. Monday
    monthNum = now.month
    dayNum = now.day

    #A list of months
    monthNames = ['January','February','March',
    'April','May','June','July','August',
    'September','October','November','December']

    #List of ordinal numbers
    ordinalNumbers = ['1st','2nd','3rd','4th','5th','6th','7th','8th','9th','10th',
    '11th','12th','13th','14th','15th','16th','17th','18th','19th','20th',
    '21st','22nd','23rd','24th','25th','26th','27th','28th','29th','30th']

    return 'Today is '+weekday+ ' '+monthNames[monthNum -1]+' the '+ ordinalNumbers[dayNum-1]+'.'

#print(getDate())

#a function to return a random response
def greeting(text):

    #greeting input
    greetingInput = ['hi','hey','hello','ola','wassup']

    #greeting responses
    greetingResponse = ['howdy!','whatsgood?','hello!','hey there!']

    #if the user's input is greeting, then return a randomly chosen response
    for word in text.split():
        if word.lower() in greetingInput:
            return random.choice(greetingResponse) + '. '
    
    #if no greetings are detected, return an empty string.
    return ''


#function to get a person's first and last name from text
def getPerson(text):

    wordList = text.split() #Splitting the text into a list of words

    for i in range(0, len(wordList)):
        if i+3 <= len(wordList) -1 and wordList[i].lower() =='who' and wordList[i+1].lower() == 'is':
            return wordList[i+2]+' '+wordList[i+3]
            #try to make the code more robust

while True:

    #Record the audio
    text = recordAudio()
    response = '' #var used to append all the rsponses and convert them to audio 

    #checking for wake words/phrase
    if (wakeWord(text)== True):

        #Check for greetings by the user
        response = response + greeting(text)

        #check to see if user said anything about the date
        if('date' in text):
            get_Date = getDate()
            response = response + ' '+get_Date

        #check to see if user said anything about time
        if('time' in text):
            now = datetime.datetime.now()
            meridian = ''
            if  now.hour >=12:
                meridian = 'p.m' 
                hour = now.hour - 12
            else:
                meridian = 'a.m'
                hour = now.hour
            
            #convert minute into proper string
            if now.minute <10:
                minute = '0'+str(now.minute)
            else:
                minute = str(now.minute)
            response = response + ' ' + 'It is'+ str(hour) +':'  +minute  +''+meridian+'. ' 

        #check if user said who is
        if('who is' in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person, sentences =2)
            response = response +' '+wiki

#assistant responding back using audio and text
        assistantResponse(response)

        #print("You said the word!")