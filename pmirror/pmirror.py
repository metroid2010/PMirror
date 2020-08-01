#!/usr/bin/python3
# vim: set expandtab shiftwidth=3 tabstop=3 autoindent: 
# PMIrror

from gpapi.googleplay import GooglePlayAPI
import configparser
import argparse
import sys
import os
import getopt

class ConfigFile():
   def __init__(self, filename):
      self._filename = filename
      self._config = configparser.ConfigParser()
      self._set_defaults()
   def load_config(self,filename):
      if os.path.isfile(filename):
         self._config.read(open(filename, 'r'))
   def save(self):
      with open(self._filename, 'w') as f:
         self._config.write(f)
   def _set_defaults(self):
      self._config.add_section('PMIRROR')
      self._config['PMIRROR']['mail'] = ""
      self._config['PMIRROR']['locale'] = "en_US"
      self._config['PMIRROR']['password'] = ""
      self._config['PMIRROR']['timezone'] = "UTC"
      self._config['PMIRROR']['gsfId'] = ""
      self._config['PMIRROR']['authSubToken'] = ""
   def get_mail(self): return self._config['PMIRROR']['mail']
   def set_mail(self, mail): self._config['PMIRROR']['mail'] = mail
   def get_password(self): return self._config['PMIRROR']['password']
   def set_password(self, password): self._config['PMIRROR']['password'] = password
   def get_locale(self): return self._config['PMIRROR']['locale']
   def set_locale(self, locale): self._config['PMIRROR']['locale'] = locale
   def get_timezone(self): return self._config['PMIRROR']['timezone']
   def set_timezone(self, locale): self._config['PMIRROR']['timezone'] = timezone
   def get_gsfId(self): return self._config['PMIRROR']['gsfId']
   def set_gsfId(self, gsfId): self._config['PMIRROR']['gsfId'] = gsfId
   def get_authSubToken(self): return self._config['PMIRROR']['authSubToken']
   def set_authSubToken(self, authSubToken): self._config['PMIRROR']['authSubToken'] = authSubToken

class ServerAPI():
   def __init__(self, ConfigFile):
      self._config = ConfigFile
      self._server = GooglePlayAPI(self._config.get_locale(), self._config.get_timezone())
   def login_with_token(self):
      self._server.login(None, None, self._config.get_gsfId(), self._config.get_authSubToken())
   def get_token(self):
      self._server.login(self._config.get_mail(), self._config.get_password())
      self._config.set_gsfId = self._server.gsfId
      self._config.set_authSubToken = self._server.authSubToken
   def download_app(self, appName):
      details = self._server.details(appName)
      docId = details.get('docId')
      filename = details.get('filename')
      if filename is None:
         filename = details.get('docId') + '.apk'
      if details is None:
         print('Package ', docid, ' does not exist on the server')
      else:
         print(docid, ' , ', filename, ' , ', details['versionCode'])
         data_gen = self._server.download(docid, details['versionCode'])
         data_gen = data_gen.get('file').get('data')
         filepath = filename
         with open(filepath, 'wb') as apk_file:
            for chunk in data_gen:
               apk_file.write(chunk)

def usage():
   print("Usage:")
   print("pmirror.py -l -m <mail> -p <password> [-c <save_file>] [-t <timezone] [-l <locale>]")
   print("pmirror.py -d [-c <save_file>] PACKAGE_NAME1 PACKAGE_NAME2 ...")
   print("pmirror.py -s [-c <save_file>] QUERY")

def parse_args():
   parser = argparse.ArgumentParser(description='PMirror: search and download PlayStore apps')
   parser.add_argument('-d', '--download', action='store_true',
                        help='Download mode')
   parser.add_argument('-s', '--search', action='store_true',
                        help='Search mode')
   parser.add_argument('-l', '--login', action='store_true',
                        help='Login mode')
   parser.add_argument('-c', '--config-file', metavar='FILENAME',
                        help='Config file', default='pmirror.config')

   return parser.parse_args()


#def main():

   ## get token
   #gsfId, authSubToken = loginWithMail(mail,password,locale,timezone)
   ## save token
   #try:
   #   saveCacheFile(mail,password,locale,timezone,gsfId,authSubToken,cacheFile):
   #except:
   #   print("Error while trying to save cacheFile, nothing done.")
   #   sys.exit(3)


   ## download mode
   #if mode == 1
   #   try:
   #      opts, args = getopt.getopt(sys.argv[2:],"c:",["cache="])
   #   except getopt.GetoptError:
   #      usage("short")
   #      sys.exit(2)
   #   for opt, arg in opts:
   #      if opt in ("-c", "--"):
   #         cacheFile = arg
   #   readCacheFile(cacheFile)



#if __name__ == "__main__":
#   main()
