#!/usr/bin/python3
# vim: set expandtab:shiftwidth=3:tabstop=3:autoindent: 
# PMIrror

from gpapi.googleplay import GooglePlayAPI
import configparser
import sys
import os
import getopt

def usage(short):
   if short == True
      print("usage: pmirror [-d|--download -m|--mail ]|[-s|--search]|[-l|--login]")
   print("
   print("pmirror.py -m <mail> -p <password> [-c <save_file>] [-t <timezone] [-l <locale>]")



def loginWithToken(gsfId,authSubtoken,locale,timezone):
   server = GooglePlayAPI(locale,timezone)
   server.login(None, None, gsfId, authSubToken)

# this one gets the tokens, too
def loginWithMail(mail,password,locale,timezone):
   server = GooglePlayAPI(locale,timezone)
   server.login(mail,password)
   gsfId = server.gsfId
   authSubToken = server.authSubToken
   return gsfId,authSubToken
   
def saveCacheFile(mail,password,locale,timezone,gsfId,authSubToken,cacheFile):
   tokenCache = configparser.ConfigParser()
   tokenCache['DEFAULT'] = { 'mail': mail,
                             'password': password,
                             'locale': locale,
                             'timezone': timezone,
                             'authSubToken': authSubToken,
                             'gsfId': gsfId }
   with open(cacheFile, 'w') as configFile:
      tokenCache.write(configFile)



def main():
   
   mail = ''
   password = ''
   cacheFile = '.cache.ini'
   locale = 'en_US'
   timezone = 'UTC'
    = "pmirror.py -m <mail> -p <password> [-c <save_file>] [-t <timezone] [-l <locale>]"
   
   # get which mode we are working on
   try:
      opts, args = getopt.getopt(sys.argv[1],"d:l:s:h",["download","login","search","help"])
   except getopt.GetoptError:
      print(helpString)
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-h", "--help"):
         print(helpString)
         sys.exit()
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

if __name__ == "__main__":
   main()
