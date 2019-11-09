#!/usr/bin/python3

from gpapi.googleplay import GooglePlayAPI
import configparser
import sys
import getopt

def main():
   
   mail = ''
   password = ''
   cacheFile = '.cache.ini'
   locale = 'en_US'
   timezone = 'UTC'
   helpString = "login.py -m <mail> -p <password> [-c <save_file>] [-t <timezone] [-l <locale>]"
   # get options 
   try:
      opts, args = getopt.getopt(sys.argv[1:],"p:m:c:t:l:h",["password=","mail=","cache=","timezone=","locale=","help"])
   except getopt.GetoptError:
      print(helpString)
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-h", "--help"):
         print(helpString)
         sys.exit()
      elif opt in ("-p", "--password"):
         password = arg
      elif opt in ("-m", "--mail"):
         mail = arg
      elif opt in ("-c", "--"):
         cacheFile = arg
      elif opt in ("-t", "--"):
         timezone = arg
      elif opt in ("-l", "--"):
         locale = arg
   if mail == '':
      print("Missing mail")
      sys.exit(1)
   if password == '':
      print("Missing password")
      sys.exit(1)
  
   # login to GP server
   server = GooglePlayAPI(locale="en_US", timezone="UTC")
   server.login(mail,password)
   gsfId = server.gsfId
   authSubToken = server.authSubToken

   # save data in cacheFile
   tokenCache = configparser.ConfigParser()
   tokenCache['DEFAULT'] = { 'mail': mail,
                             'password': password,
                             'locale': locale,
                             'timezone': timezone,
                             'authSubToken': authSubToken,
                             'gsfId': gsfId }
   with open(cacheFile, 'w') as configFile:
      tokenCache.write(configFile)

if __name__ == "__main__":
   main()
