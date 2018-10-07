#!/usr/bin/python
############################################################################################################
# This program will find Job files in multiple state directories and turn them into a human readable format
#
# Created by Marc Loftus 28/10/2017
#
#
############################################################################################################
# History
# 1.0       Marc Loftus     21/06/2017      Basic file ls handling
# 1.1       Marc Loftus     28/10/2017      dir lists turned into dictionary types for ease of searching
# 1.2       Marc Loftus     28/10/2017      Sorting NEW oldest first, COMPLATED oldest last
# 1.3       Marc Loftus     30/10/2017      Starting convert of scorch(bash) to scorch(python)
# 1.4       Marc Loftus     27/11/2017      C|hnaged to self contained ShowJobs function
# 1.5       Marc Loftus     08/02/2018      Adjustment for args [2] to [1] for output file
#      -v int_Column1Width=${int_Column1Width} \
#      -v int_Column2Width=${int_Column2Width} \
#      -v int_Column3Width=${int_Column3Width} \
#      -v int_Column4Width=${int_Column4Width} \
#      -v int_Column5Width=${int_Column5Width} \
#      -v int_Column6Width=${int_Column6Width} \
# 1.6       Marc Loftus     17/04/2018      Adjustment to OS paths
# 1.7       Marc Loftus     02/05/2018      Colour class added and failed jobs highlighted
# 1.8       Marc Loftus     21/05/2018      Now uses int_MaxShown prefs (or 35 default)
# 1.8.1                                     changed wording
# 1.9       Marc Loftus     05/06/2018      Added rows for auto scaling
# 1.10      Marc Loftus     12/06/2018      Adding Pause and Rules flags
# 1.11      Marc Loftus     15/06/2018      Adding elasped time
# 1.12      Marc Loftus     04/10/2018      Fixed issues with showline stealing CR
############################################################################################################
str_ProgramVersion = '1.11'

import os, getpass, getopt, sys
import time        # Used for ls sorting in time order
import datetime    # Used for elapsed running time
import glob
import tempfile    # Used to have an output file
import re

from os import listdir, access
from os.path import isfile, join, islink, getmtime


class colours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

dir_Run=os.getcwd()
# Default maxnum
maxnum = 35
b_More = False
int_More = 0

# Set up variables
#if os.name == "nt":
    # Windows
#    print("Not yet onfigured for windows")
#    dir_Base  = "C:\\Users\\Marc\\Google Drive\\WebMarcIT\\scorch\\ScORCH\\"
#    dir_Job   = dir_Base + "\\jobs\\"
#    dir_Log   = dir_Base + "\\var\\log\\"
#    cmd_Clear = "os.system('cls')"
#    exit()
#else:
    # Everything else
dir_Base=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dir_Job   = dir_Base + "/jobs/"
dir_Log   = dir_Base + "/var/log/"
str_Pause = "pause"
str_Rule  = "rules"
cmd_Clear = "os.system('clear')"
chr_PauseFlag = ""
chr_RuleFlag = ""
str_Time = ""

int_Count             = 1
str_ProgramName       = __file__
int_PID               = os.getpid()
int_Rows, int_Columns = os.popen('stty size', 'r').read().split()
list_Dir              = []

def fn_ShowLine(cha_LineChar,str_LineTitle):
    ''' Shows a row of characters that fill the width of the screen Takes 2 parameters, char , title
        This can actually show a row of strings but they my not fill the whole depending on string width '''
    parity=(len(cha_LineChar))
    print( "%s"% cha_LineChar * (3/parity) + str_LineTitle + cha_LineChar * ((int(int_Columns)/parity) - (len(str_LineTitle)/parity) - (3/parity) - 1 ) )

def fn_ShowJobs(str_State,temp,maxnum):
    '''ShowLine2 takes a state argument which is turned into a directory location
       and the files in the directory are broken up into columns'''
    arr_str_DirList  = (listdir(join(dir_Job,str_State)))                   #   Create an "ls" list for the directory
    arr_str_DirList2 = glob.glob(os.path.join(dir_Job,str_State)+'/Job*')   #   Create an "ls $jobdir/Job*"
    global b_More
    global int_More
    global int_Count
    if arr_str_DirList2:                                                    #   If there is anything in the directory

        fn_ShowLine("-",str_State.upper())
        

        if os.name == "nt":
            dir_State = dir_Job + str_State + '\\'
        else:
            dir_State = dir_Job + str_State + '/'

        #print ("debug - testing dir", dir_State)
        os.chdir(dir_State)                                                     # Change to the job/state directory
        arr_Files = list(os.listdir('.'))
        #print ("debug - files1 :', files,'\n')
        arr_Files.sort(key=lambda x: os.path.getmtime(x))
        if str_State == "completed":
            arr_Files=list(reversed(arr_Files))
        if str_State == "failed":
          ansi_colour=colours.FAIL
        else:
          ansi_colour=colours.RESET

        # int_Column1Width=3     # Job num
        # int_Column2Width=8     # Job ID
        # int_Column3Width=20    # Longest Action
        # int_Column4Width=10    # Longest Envrionment
        # int_Column5Width=23    # Longest Release 
        # int_Column6Width=      # Width left for the log
        int_Width=int(int_Columns) - 3 - 8   - 10 - 20  - 8  - 20 

        for str_File in arr_Files:
            if os.access ( dir_Job + "active/" + str_File + "." + str_Pause, os.R_OK):
                chr_PauseFlag = "P"
            else:
                chr_PauseFlag = " "
            if os.access ( dir_Job + "active/" + str_File + "." + str_Rule, os.R_OK):
                chr_RuleFlag = "R"
            else:
                chr_RuleFlag = " "

            ''' Max Display '''
            if int_Count <= maxnum:
                #print("ok", int_Count, maxnum)
                ''' Class handling '''

                temp.write('arr_States['+str(int_Count)+']='+str_State+'\n')
                temp.write('arr_Jobs['+str(int_Count)+']='+str_File+'\n')

                str_JobSplit = str_File.split("_")
                file_JobLog  = dir_Log + str_File + ".log"

                # Collect the last line of the log file
                if os.access (file_JobLog, os.R_OK):

                    ptr_JobLogFile = open(file_JobLog,"r")

                    str_JobLogFile = ptr_JobLogFile.readlines()
                    ptr_JobLogFile.close()
                    str_LastLine   = str_JobLogFile[-1].rstrip('\n')

                else:
                    str_LastLine   = "Error: Cannot read file"

                if re.search("WIP", str_LastLine):
                  ansi_colour=colours.RESET
                if str_State == "running":
                    
                  # look in log file for AUDIT:START:[1.*] - yes starting with a one - it'll be a long time till is starts 2 (18 May 2033 03:33:20 in fact)
                  with open(file_JobLog) as origin:
                    for line in origin:
                       if not "AUDIT:START:1" in line:
                          continue
                       try:
                          str_StartTime = int(line.split(':')[2])
                       except IndexError:
                          print


                  str_CurrentTime=int(time.time())
                  str_Time=str_CurrentTime - str_StartTime
                  str_Time=str(datetime.timedelta(seconds=str_Time))
                  print (ansi_colour + "%3d%s%s%+10s|%+20s|%+8s|%+20s|%+s|%s%s"% (int_Count,chr_PauseFlag,chr_RuleFlag,str_JobSplit[1],str_JobSplit[3],str_JobSplit[4],str_JobSplit[5], str_Time, str_LastLine, colours.RESET))
                else:
                  print (ansi_colour + "%3d%s%s%+10s|%+20s|%+8s|%+20s|%s%s"% (int_Count,chr_PauseFlag,chr_RuleFlag,str_JobSplit[1],str_JobSplit[3],str_JobSplit[4],str_JobSplit[5], str_LastLine[:int_Width], colours.RESET))
                int_Count = int_Count + 1
            else:
                b_More = True
                int_More = int_More + 1



def main(argv):
    outputfile = os.devnull
    args = sys.argv[1:]
    global int_More
    while len(args):
        if args[0] == '-o':
            outputfile = args[1]
            args = args[2:]
        elif args[0] == '-v':
            option = args[1]
            args = args[1:]
        elif args[0] == '-n':
            maxnum = int(args[1])
            args = args[2:]
        else:
            list_Dir.append(args[0])
            args = args[1:] # shift

    filename = outputfile
    temp = open(filename, 'w+b')

    if maxnum == 999:
        rows, columns = os.popen('stty size', 'r').read().split()
        maxnum = int(rows) - 10

    for eachDir in list_Dir:
        fn_ShowJobs(eachDir,temp,maxnum)

    if b_More is True:
        print("+++ ["+str(int_More)+" more]")

    temp.write('int_Count='+str(int_Count)+'\n')

    name= 'varname'
    value= 'something'

    temp.close()


if __name__ == "__main__":
   main(sys.argv[1:])

