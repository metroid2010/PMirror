#!/usr/bin/python3

from gpapi.googleplay import GooglePlayAPI
import configparser
import sys

def main():

   # get args
   sys.argv.pop(0)
   searchQuery = ' '.join(sys.argv)

   # read token cache
   tokenCache = configparser.ConfigParser()
   tokenCache.read('.cache.ini')
   try:
      gsfId = int(tokenCache['DEFAULT']['gsfId']) # does not get saved as int, but as str!
      authSubToken = tokenCache['DEFAULT']['authSubToken']
      timezone = tokenCache['DEFAULT']['timezone']
      locale = tokenCache['DEFAULT']['locale']
   except configparser.NoSectionError:
      print("Missing login data. Please, check your cache file, or run login.py")
      sys.exit(1)
   except configparser.ParsingError:
      print("The cache file could not be read correctly. Please, check it, or run login.py")
      sys.exit(1)
   except configparser.Error as e:
      print("Error ", e, " while reading cache file")
      sys.exit(1)


   server = GooglePlayAPI(locale, timezone)
   
   # log in with saved credentials
   try:
      server.login(None, None, gsfId, authSubToken)
   except:
      print("Error while trying to login to GP servers")
      sys.exit(2)

   resultRaw = server.search(searchQuery, 20)

   for app in resultRaw:
       docid = app.get('docId')
       print(docid)

if __name__ == "__main__":
   main()
