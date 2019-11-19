#!/usr/bin/python3
# vim: set expandtab shiftwidth=3 tabstop=3 autoindent: 
# PMIrror

from gpapi.googleplay import GooglePlayAPI
import configparser
import sys
import os
import getopt

def usage(length):
   if length == "short"
      print("usage: pmirror [-d|--download -m|--mail ]|[-s|--search]|[-l|--login]")
   else
      print("Usage:")
      print("pmirror.py -l -m <mail> -p <password> [-c <save_file>] [-t <timezone] [-l <locale>]")
      print("pmirror.py -d [-c <save_file>] PACKAGE_NAME1 PACKAGE_NAME2 ...")
      print("pmirror.py -s [-c <save_file>] QUERY")

def loginWithToken(gsfId,authSubtoken,locale,timezone):
   server = GooglePlayAPI(locale,timezone)
   server.login(None, None, gsfId, authSubToken)
   return server

# this one only gets the tokens
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

def readCacheFile(cacheFile):
   tokenCache = configparser.ConfigParser()
   tokenCache = read(cacheFile)
   try:
      gsfId = 
      authSubToken = 
      timezone =
      locale = 
   return gsfId,authSubToken,timezone,locale

def downloadApp(gsfId,authSubToken,appName,directory,server)
   details = server.details(appName)
   filename = details.get('filename')
   if filename is None:
      filename = details.get('docId') + '.apk'
   if details is None:
      print('Package ', docid, ' does not exist on the server')
      raise 

def main():
  
   # defaults for the args
   mail = ''
   password = ''
   cacheFile = '.cache.ini'
   locale = 'en_US'
   timezone = 'UTC'
   mode = ''
   
   # get which mode we are working on
   try:
      opts, args = getopt.getopt(sys.argv[1],"d:l:s:h",["download","login","search","help"])
   except getopt.GetoptError:
      usage("short")
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-h", "--help"):
         usage("long")
         sys.exit(0)
      if opt in ("-l", "--login");
         mode = 1 
      if opt in ("-d", "--download");
         mode = 2 
      if opt in ("-s", "--search");
         mode = 3 
   
   # login mode 
   if mode == 1
      try:
         opts, args = getopt.getopt(sys.argv[2:],"p:m:c:t:l:",["password=","mail=","cache=","timezone=","locale="])
      except getopt.GetoptError:
         usage("short")
         sys.exit(2)
      for opt, arg in opts:
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

      # get token
      gsfId, authSubToken = loginWithMail(mail,password,locale,timezone)
      # save token
      try:
         saveCacheFile(mail,password,locale,timezone,gsfId,authSubToken,cacheFile):
      except:
         print("Error while trying to save cacheFile, nothing done.")
         sys.exit(3)


   # download mode
   if mode == 1
      try:
         opts, args = getopt.getopt(sys.argv[2:],"c:",["cache="])
      except getopt.GetoptError:
         usage("short")
         sys.exit(2)
      for opt, arg in opts:
         if opt in ("-c", "--"):
            cacheFile = arg
      readCacheFile(cacheFile)



if __name__ == "__main__":
   main()
