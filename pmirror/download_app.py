#!/usr/bin/python3

from gpapi.googleplay import GooglePlayAPI
import configparser
import sys
import os

def main():

   # get args
   sys.argv.pop(0)
   appNames = sys.argv

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

   for app in appNames:
      try:
         details = server.details(app)
         docid = details.get('docId')
         filename = details.get('filename')
         if filename is None:
            filename = details.get('docId') + '.apk'
         if details is None:
            print('Package ', docid, ' does not exist')
            continue
      except:
         print("Error while trying to get details for", app)
      else:
         print(docid, ' , ', filename, details['versionCode'])
         data_gen = server.download(docid, details['versionCode'])
         data_gen = data_gen.get('file').get('data')
         filepath = filename
         with open(filepath, 'wb') as apk_file:
            for chunk in data_gen:
               apk_file.write(chunk)


if __name__ == "__main__":
   main()
