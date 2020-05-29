#!/usr/bin/python3
############################################################################################################
# This program will find Job files in multiple state directories and turn them into a human readable format
#
# Created by Marc Loftus 28/10/2017
#
# ${dir_Python}/showJobs.py -n $int_MaxShown -o ${file_Cache} -f "${str_Filter}" $*
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
# 1.13      Marc Loftus     23/10/2018      #73 Adding filter option
# 1.14      Marc Loftus     26/01/2019      #94 Variable Column Width
#                                           #95 Empty log file protection
# 1.15      Marc Loftus     11/07/2019      #112 Highlight own jobs
# 1.16      Marc Loftus     29/10/2019      #122 Nulling out non-ascii characters
# 1.17      Marc Loftus     20/02/2020      Python 3
############################################################################################################
str_ProgramVersion = '1.17'

import os, getpass, getopt, sys
import time        # Used for ls sorting in time order
import datetime    # Used for elapsed running time
import glob
import tempfile    # Used to have an output file
import re
import mmap        # Used to find LAST occurance of TASK:START: even in large log files

from os import listdir, access
from os.path import isfile, join, islink, getmtime

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

dir_Run=os.getcwd()
# Default maxnum
maxnum = 35
b_More = False
int_More = 0


class colours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

# class File(file):
#     """ Helper class for file reading """
#     def __init__(self,*args, **kwargs):
#         super(File,self).__init__(*args, **kwargs)
#         self.BLOCKSIZE = 4096

#     def head(self, lines_2find=1):
#         self.seek(0)
#         return [super(File, self).next() for x in xrange(lines_2find)]

#     def tail(self, lines_2find=1):
#         self.seek(0,2)
#         bytes_in_file = self.tell()
#         lines_found, total_bytes_scanned = 0, 0
#         while (lines_2find +1 > lines_found and
#             bytes_in_file > total_bytes_scanned):
#           byte_block = min(
#             self.BLOCKSIZE,
#             bytes_in_file - total_bytes_scanned)
#           self.seek( -(byte_block + total_bytes_scanned), 2)
#           total_bytes_scanned += byte_block
#           lines_found += self.read(self.BLOCKSIZE).count('\n')
#         self.seek(-total_bytes_scanned,2)
#         line_list = list(self.readlines())
#         return line_list[-lines_2find:]


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


def fn_ShowLine(cha_LineChar,str_LineTitle):
    ''' Shows a row of characters that fill the width of the screen Takes 2 parameters, char , title
        This can actually show a row of strings but they my not fill the whole depending on string width '''
    parity=(len(cha_LineChar))
    #print(str_LineTitle.center(int(int_Columns),cha_LineChar))
    int_remaining = int(int(int_Columns)/parity) - int(3/parity) 
    print("%s"% cha_LineChar * int(3/parity) + str_LineTitle.ljust(int_remaining, cha_LineChar))
    #print( "%s"% cha_LineChar * int(3/parity) + str_LineTitle + cha_LineChar * ((int(int_Columns)/parity) - (len(str_LineTitle)/parity) - int(3/parity) - 1 ) )

def fn_ColumnMax(arr_Files,int_Column):
    int_ColumnMax=0
    for str_File in arr_Files:
        str_JobSplit = str_File.split("_")
        int_TmpMax=len(str_JobSplit[int_Column])
        if  int_TmpMax >= int_ColumnMax:
            int_ColumnMax = int_TmpMax
    return int_ColumnMax + 1

def fn_ColumnMax2(dir_Job,arr_str_Dirs,int_Column):
    print(os.path.join(dir_Job))
    #arr_str_DirList2 = glob.glob(os.path.join(dir_Job)+'*/Job*'+jobfilter+'*')   #   Create an "ls $jobdir/Job*"
    #for str_File in arr_str_DirList2:
    #    print str_File
    #    int_ColumnMax=0
    #for root, dirs, files in os.walk(dir_Job):
    #    print root
        #print dirs
        #print files
    #for str_File in arr_Files:
    #    str_JobSplit = str_File.split("_")
    #    int_TmpMax=len(str_JobSplit[int_Column])
    #    if  int_TmpMax >= int_ColumnMax:
    #        int_ColumnMax = int_TmpMax
    return 1

def fn_ShowJobs(str_State,temp,maxnum):
    '''ShowLine2 takes a state argument which is turned into a directory location
       and the files in the directory are broken up into columns'''
    arr_str_DirList2 = glob.glob(os.path.join(dir_Job,str_State)+'/Job*'+jobfilter+'*')   #   Create an "ls $jobdir/Job*"
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
        chr_Owner=" "
        int_Magic=7    # including pipes and spaces
        int_JobNumWidth=3     # 1 Job num
        int_JobIDWidth=fn_ColumnMax(arr_Files,2)    # 2 Job ID
        int_ActionWidth=fn_ColumnMax(arr_Files,3)     # 3 Longest Action
        int_EnvWidth=fn_ColumnMax(arr_Files,4)     # 4 Longest Envrionment
        int_ReleaseWidth=fn_ColumnMax(arr_Files,5)      # 5 Longest Release 
        int_LogWidth=99      # 6 Width left for the log
        #int_Width=int(int_Columns) - 3 - 8   - 10 - 20  - 8  - 20
        int_Width=int(int_Columns) - int_Magic - int_JobNumWidth - int_JobIDWidth - int_ActionWidth - int_EnvWidth - int_ReleaseWidth

        for str_File in arr_Files:
            chr_Owner = " "
            for line in open(str_File, 'r'):
              if re.search("str_Owner=" + getpass.getuser() + "$", line):
                chr_Owner = ">"
                break

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
                #with open(temp, 'w+a') as temp: 
                temp.write('arr_States['+str(int_Count)+']='+str_State+'\n')
                temp.write('arr_Jobs['+str(int_Count)+']='+str_File+'\n')

                str_JobSplit = str_File.split("_")
                file_JobLog  = dir_Log + str_File + ".log"

                # Collect the last line of the log file
                if os.access (file_JobLog, os.R_OK):

                    ptr_JobLogFile = open(file_JobLog,"r")

                    str_JobLogFile = ptr_JobLogFile.readlines()
                    ptr_JobLogFile.close()
                    try:
                        str_LastLine   = re.sub(r'[^\x0e-\x7e]',r'\\', str_JobLogFile[-1].rstrip('\n'))
                    except IndexError:
                        str_LastLine   = "Warning: Empty file"

                else:
                    str_LastLine   = "Error: Cannot read file. Check permissions for read access."

                if re.search("WIP", str_LastLine):
                  ansi_colour=colours.RESET
                if str_State == "running":
                  #str_StartTime = int(time.time())
                    
                  # look in log file for AUDIT:START:[1.*] - yes starting with a one - it'll be a long time till is starts 2 (18 May 2033 03:33:20 in fact)
                  str_StartTime=GetStartTime(file_JobLog)
                  str_TaskTime=GetRunningTime(file_JobLog)

                  str_CurrentTime=int(time.time())
                  str_Time=str_CurrentTime - str_StartTime
                  str_Time=str(datetime.timedelta(seconds=str_Time))
                  str_Task=str_CurrentTime - str_TaskTime
                  str_Task=str(datetime.timedelta(seconds=str_Task)) 
                  #print str_Task  
                  # if TIMEOUT set
                  #   if str_Task greter then TIMEOUT
                  #     set ansi_colour=coulrs.WARNING                
                  print (ansi_colour + "%s%3d%s%s%+*s|%+*s|%+*s|%+*s|%+s|%s%s"% (chr_Owner, int_Count,
                    chr_PauseFlag,chr_RuleFlag,
                    int_JobIDWidth,str_JobSplit[1],
                    int_ActionWidth,str_JobSplit[3],
                    int_EnvWidth,str_JobSplit[4],
                    int_ReleaseWidth,str_JobSplit[5], 
                    str_Time, 
                    str_LastLine[:int_Width-10], colours.RESET))
                #  with File(file_JobLog) as f:
                #    for line in f.head(12):
                #      print line.replace('\n','')
                #    print f.tail(1)
                else:
                    if re.search(jobfilter,str_File):
                        print (ansi_colour + "%s%3d%s%s%*s|%+*s|%+*s|%+*s|%s%s"% (chr_Owner,int_Count,
                            chr_PauseFlag,chr_RuleFlag,
                            int_JobIDWidth,str_JobSplit[1],
                            int_ActionWidth,str_JobSplit[3],
                            int_EnvWidth,str_JobSplit[4],
                            int_ReleaseWidth,str_JobSplit[5], 
                            str_LastLine[:int_Width], colours.RESET))

                int_Count = int_Count + 1
            else:
                b_More = True
                int_More = int_More + 1

def GetStartTime(filename):
    MAX_READ=range(10)
    x = int(time.time())
    with open(filename) as origin:
      for line, _ in zip(origin,MAX_READ):
        if "AUDIT:START:1" in line:
          try:
            x = int(line.split(':')[2])
          except:
            x = int(time.time())
          break 
    return x

def GetRunningTime(filename):
    x = int(time.time())
    for line in reversed(open(filename).readlines()):
      if "TASK:START" in line:
        try:
          x = int(line.split(':')[2])
        except:
          x = GetStartTime(filename) #int(time.time())
        break
    return x


    # Do the operations here when you find the line


# Reverse readlines from logfile until string found
#def reverse_readline(filename, buf_size=8192):
#    """A generator that returns the lines of a file in reverse order"""
#    with open(filename) as fh:
#        segment = None
#        offset = 0
#        fh.seek(0, os.SEEK_END)
#        file_size = remaining_size = fh.tell()
#        while remaining_size > 0:
#            offset = min(file_size, offset + buf_size)
#            fh.seek(file_size - offset)
#            buffer = fh.read(min(remaining_size, buf_size))
#            remaining_size -= buf_size
#            lines = buffer.split('\n')
#            # The first line of the buffer is probably not a complete line so
#            # we'll save it and append it to the last line of the next buffer
#            # we read
#            if segment is not None:
#                # If the previous chunk starts right from the beginning of line
#                # do not concat the segment to the last line of new chunk.
#                # Instead, yield the segment first 
#                if buffer[-1] != '\n':
#                    lines[-1] += segment
#                else:
#                    yield segment
#            segment = lines[0]
#            for index in range(len(lines) - 1, 0, -1):
#                if lines[index]:
#                    yield lines[index]
#        # Don't yield None if the file was empty
#        if segment is not None:
#            yield segment

#def readlines_reverse(filename):
#    with open(filename) as qfile:
#        qfile.seek(0, os.SEEK_END)
#        position = qfile.tell()
#        line = ''
#        while position >= 0:
#            qfile.seek(position)
#            next_char = qfile.read(1)
#            if next_char == "\n":
#                yield line[::-1]
#                line = ''
#            else:
#                line += next_char
#            position -= 1
#        yield line[::-1]
#

#if __name__ == '__main__':
#    for qline in readlines_reverse(raw_input()):
#        print qline

def main(argv):
    outputfile = os.devnull
    maxnum = 999
    global jobfilter
    jobfilter = ""
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
        elif args[0] == '-f':
            jobfilter = args[1]
            args = args[2:] 
        else:
            list_Dir.append(args[0])
            args = args[1:] # shift

    temp = open(outputfile, 'w+')

    if maxnum == 999:
        rows, columns = os.popen('stty size', 'r').read().split()
        maxnum = int(rows) - 10

    # Work for better spanning columns
    #arr_str_DirList  = (listdir(dir_Job))                   #   Create an "ls" list for the directory
    #arr_str_DirList = ("completed","failed","fixing","manual","new","pending","queued","running","starting","superseded")
    #print arr_str_DirList
    #print(fn_ColumnMax2(dir_Job,arr_str_DirList,1))

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
