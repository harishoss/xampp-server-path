#! usr/bin/env python3
from os import path,chmod
from sys import argv
from re import match
from stat import S_IWUSR, S_IREAD
import subprocess

# httpd.conf path 
HTTPD_CONF = '/opt/lampp/etc/httpd.conf'

def get_httpd_content(file_path):
    ''' 
    takes file path as input and returns 
    file content in list format.
    '''
    if not path.isfile(file_path):
        exit("File is not found.")
    httpd_file = open(file_path, 'r')
    return httpd_file.readlines()

def is_matched(string):
    '''
    accepts a string.
    returns true if the string matches to our 
    regex pattern 'DocumentRoot ".+"'
    if not, false is returned.
    '''
    if match('^DocumentRoot ".*"$',string):
        return True
    else:
        return False

def replace_path(fileContent, replace_string):
    '''
    accepts file's content in list format and 
    replace string.
    returns nothing.
    modify the given list-items if the expected string 
    found in any list-items.
    '''
    for lineCount, line in enumerate(fileContent):
        if is_matched(line):
            if fileContent[lineCount+1] == '<Directory "{}">\n'.format(line.split('"')[1]):
                fileContent[lineCount] = 'DocumentRoot "{}"\n'.format(replace_string)
                fileContent[lineCount+1] = '<Directory "{}">\n'.format(replace_string)
                return
            else:
                exit("httpd.conf file is correcpted  - Could't found line starts with Directory")
    exit("httpd.conf file is correcpted  - Could't found line starts with DocumentRoot")   

def save_to_file(fileContent):
    '''
    accepts a list of items and 
    saves to httpd.conf file
    (No appending, completely repalces 
    the file)
    '''
    with open(HTTPD_CONF, 'w') as file:
        file.writelines(fileContent)
def process_argv():
    if(len(argv) == 1):
        exit("No Necessary Arguments found. Provide a 'path/to/replace' or '--current' as arguments.")
    if argv[1] == '--current':
        return path.dirname(path.realpath(__file__))
    else:
        if path.isdir(argv[1]):
            return argv[1]
        else:
            exit("Given Path is not a directory or can't be accesable")

if __name__ == "__main__":
    path_to_replace = process_argv()
    fileContent = get_httpd_content(HTTPD_CONF)
    replace_path(fileContent, path_to_replace)
    save_to_file(fileContent)
