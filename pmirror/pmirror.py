#!/usr/bin/python3
# vim: set expandtab shiftwidth=3 tabstop=3 autoindent: 
# PMirror

from gpapi.googleplay import GooglePlayAPI
import configparser
import sys
import os
import getopt


def usage(length):
    if length == "short":
        print("usage: pmirror [-d|--download -m|--mail ]|[-s|--search]|[-l|--login]")
    else:
        print("Usage:")
        print("pmirror.py -l -m <mail> -p <password> [-c <save_file>] [-t <timezone] [-l <locale>]")
        print("pmirror.py -d [-c <save_file>] PACKAGE_NAME1 PACKAGE_NAME2 ...")
        print("pmirror.py -s [-c <save_file>] QUERY")


def loginWithToken(gsfId, authSubToken, locale, timezone):
    server = GooglePlayAPI(locale, timezone)
    server.login(None, None, gsfId, authSubToken)
    return server


# this one only gets the tokens
def loginWithMail(mail, password, locale, timezone):
    server = GooglePlayAPI(locale, timezone)
    server.login(mail, password)
    gsfId = server.gsfId
    authSubToken = server.authSubToken
    return gsfId, authSubToken


def writeCacheFile(mail, password, locale, timezone, gsfId, authSubToken, cacheFile):
    tokenCache = configparser.ConfigParser()
    tokenCache['DEFAULT'] = {'mail': mail,
                             'password': password,
                             'locale': locale,
                             'timezone': timezone,
                             'authSubToken': authSubToken,
                             'gsfId': gsfId}
    with open(cacheFile, 'w') as configFile:
        tokenCache.write(configFile)


def readCacheFile(cacheFile):
    tokenCache = configparser.ConfigParser()
    tokenCache.read(cacheFile)
    try:
        gsfId = tokenCache['DEFAULT']['gsfId']
        authSubToken = tokenCache['DEFAULT']['authSubToken']
        timezone = tokenCache['DEFAULT']['timezone']
        locale = tokenCache['DEFAULT']['locale']
    except configparser.Error:
        raise configparser.Error

    return int(gsfId), authSubToken, timezone, locale


def downloadApp(appName, directory, server):
    details = server.details(appName)
    filename = details.get('filename')
    docid = details.get('docid')
    if details is None:
        print('Package ', appName, ' does not exist on the server')
        return
    if filename is None:
        filename = details.get('docid') + '.apk'
    data_gen = server.download(docid, details['details']['appDetails']['versionCode']).get('file').get('data')
    with open( filename , 'wb') as apk_file:
        for chunk in data_gen:
            apk_file.write(chunk)


def main():

    # defaults for the args
    mail = 'mail@mail.com'
    password = 'password'
    cacheFile = '.cache.ini'
    locale = 'en_US'
    timezone = 'UTC'
    mode = ''

    # get which mode we are working on
    try:
        opts,args = getopt.getopt(sys.argv[1:], "d:l:s:h:", ["download", "login", "search", "help"])
    except BaseException:
        usage("short")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage("long")
            sys.exit(0)
        if opt in ("-l", "--login"):
            mode = 0
        if opt in ("-d", "--download"):
            mode = 1
        if opt in ("-s", "--search"):
            mode = 2

    # login mode
    if mode == 0:
        try:
            opts, args = getopt.getopt( sys.argv[2:], "p:m:c:t:l:", ["password=", "mail=", "cache=", "timezone=", "locale="] )
        except getopt.GetoptError:
            usage("short")
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-p", "--password"):
                password = arg
            elif opt in ("-m", "--mail"):
                mail = arg
            elif opt in ("-c", "--cache"):
                cacheFile = arg
            elif opt in ("-t", "--timezone"):
                timezone = arg
            elif opt in ("-z", "--locale"):
                locale = arg
        if mail == '':
            print("Missing mail")
            sys.exit(1)
        if password == '':
            print("Missing password")
            sys.exit(1)

        # build api
        gsfId, authSubToken = loginWithMail(mail, password, locale, timezone)
        # save token
        try:
            writeCacheFile(mail, password, locale, timezone, gsfId, authSubToken, cacheFile)
        except:
            print("Error while trying to save cacheFile, nothing done.")
            sys.exit(3)


    # download mode
    if mode == 1:
        directory = "."
        appNames = sys.argv[2:]
        gsfId, authSubToken, timezone, locale = readCacheFile(cacheFile)
        server = loginWithToken(gsfId, authSubToken, locale, timezone)
        for app in appNames:
            print("downloading app " + app)
            downloadApp(app, directory, server)

    # search mode
    if mode == 2:
        searchQuery = ' '.join(sys.argv[2:])
        gsfId, authSubToken, timezone, locale = readCacheFile(cacheFile)
        server = loginWithToken(gsfId, authSubToken, locale, timezone)
        print (searchQuery)
        resultRaw = server.search(searchQuery)
        for result in resultRaw:
            if 'docid' in result:
                print("doc: {}".format(result['docid']))
            cluster = result['child'][1];
            print("\tcluster: {}".format(cluster['docid']))
            for child in cluster['child']:
                print("\t\tapp: {}".format(child['docid']))


if __name__ == "__main__":
    main()
