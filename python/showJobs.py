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
############################################################################################################
str_ProgramVersion = '1.4dev'

import os, getpass, getopt, sys
import time
import glob
import tempfile

from os import listdir, access
from os.path import isfile, join, islink, getmtime


#import ctypes
dir_Run=os.getcwd()
#typeset           dir_Orig="$(pwd)/${dir_Run}"
#typeset     fn_FullLogDate="date +${str_ProgramName}:%y%m%d-%H%M%S"
#typeset         fn_LogDate="date +%y%m%d-%H%M%S"

# Set up variables
if os.name == "nt":
    # Windows
    print("Not yet onfigured for windows")
    dir_Base  = "C:\\Users\\Marc\\Google Drive\\WebMarcIT\\scorch\\ScORCH\\"
    dir_Job   = dir_Base + "\\jobs\\"
    dir_Log   = dir_Base + "\\var\\log\\"
    cmd_Clear = "os.system('cls')"
    exit()
else:
    # Everything else
    dir_Base=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dir_Job   = dir_Base + "/jobs/"
    dir_Log   = dir_Base + "/var/log/"
    cmd_Clear = "os.system('clear')" 

int_Count             = 1
str_ProgramName       = __file__
int_PID               = os.getpid()
int_Rows, int_Columns = os.popen('stty size', 'r').read().split()
list_Dir              = []
#print(int_Rows, int_Columns)
#print open(__file__).read()

#print ("Eid [%s]"  % (getpass.getuser()))
#print ("pwd: [%s]" % (os.getcwd()))





def fn_ShowLine(cha_LineChar,str_LineTitle):
    ''' Shows a row of characters that fill the width of the screen Takes 2 parameters, char , title
        This can actually show a row of strings but they my not fill the whole depending on string width '''
    parity=(len(cha_LineChar))
    print(cha_LineChar * (3/parity) + str_LineTitle + cha_LineChar * ((int(int_Columns)/parity) - (len(str_LineTitle)/parity) - (3/parity)))

#fp = tempfile.TemporaryFile()
#    fp.write(b'Hello world!')

def fn_ShowJobs(str_State,temp):
    '''ShowLine2 takes a state argument which is turned into a directory location
       and the files in the directory are broken up into columns'''
    arr_str_DirList  = (listdir(join(dir_Job,str_State)))                   #   Create an "ls" list for the directory
    arr_str_DirList2 = glob.glob(os.path.join(dir_Job,str_State)+'/Job*')   #   Create an "ls $jobdir/Job*" 
    if arr_str_DirList2:                                                    #   If there is anything in the directory 

        #print ("debug:\n" , dic_str_DirList[str_State], "\n")
        fn_ShowLine("-",str_State.upper())
        # print( "-- " + str_State.upper() + " ---------------------------------------------------------------------------" )           #   mark the state
        global int_Count

        if os.name == "nt":
            dir_State = dir_Job + str_State + '\\'
        else:
            dir_State = dir_Job + str_State + '/'

        #print ("debug - testing dir", dir_State)
        os.chdir(dir_State)                                                     # Change to the job/state directory
        arr_Files = list(os.listdir('.'))                                       
        #print ("debug - files1 :', files,'\n')
        arr_Files.sort(key=lambda x: os.path.getmtime(x))

        for str_File in arr_Files:

            ''' Class handling '''

            temp.write('arr_States['+str(int_Count)+']='+str_State+'\n')
            temp.write('arr_Jobs['+str(int_Count)+']='+str_File+'\n')

            str_JobSplit = str_File.split("_")
            file_JobLog  = dir_Log + str_File + ".log"

            if os.access (file_JobLog, os.R_OK):

#               for line in open(str_File,"r"):
#                  if "str_Owner=" in line:
#                     print line

                ptr_JobLogFile = open(file_JobLog,"r")

                str_JobLogFile = ptr_JobLogFile.readlines()
                ptr_JobLogFile.close()
                str_LastLine   = str_JobLogFile[-1].rstrip('\n')

            else:
                str_LastLine   = "Error: Cannot read file"

            #print ("%3d%+10s|%+20s|%+8s|%+20s|%s"% (int_Count,str_JobSplit[1],str_JobSplit[3],str_JobSplit[4],str_JobSplit[5], str_JobLogFile[-1].rstrip('\n')))
            print ("%3d%+10s|%+20s|%+8s|%+20s|%s"% (int_Count,str_JobSplit[1],str_JobSplit[3],str_JobSplit[4],str_JobSplit[5], str_LastLine))
            int_Count = int_Count + 1
            #print(x.name,x.states)


def main(argv):
    #print('Number of arguments:', len(sys.argv), 'arguments.')
    #print('Program name:',os.path.basename(__file__))
    #print('Argument List:', str(sys.argv))
    #inputfile = ''
    outputfile = 'os.devnull'
#    try:
#        opts, args = getopt.getopt(argv,"hi:o:v:",["ifile=","ofile="])
#    except getopt.GetoptError:
#        print(__file__ , '-o <outputfile> <state> <state>*')
#        sys.exit(2)
#    for opt, arg in opts:
#        if opt == '-h':
#            print(__file__ , ' -i <inputfile> -o <outputfile>')
#            sys.exit()
#        elif opt in ("-o", "--ofile"):
#            outputfile = arg
#        elif opt in ("-v"):
#            print(arg)
#        else:
#            print(opt)
#            fn_ShowJobs(arg)

#    print("===========================")
    outputfile = os.devnull
    args = sys.argv[1:]
    while len(args):
        if args[0] == '-o':
            outputfile = args[1]
            args = args[2:]
        elif args[0] == '-v':
            option = args[1]
            args = args[1:]
        else:
            list_Dir.append(args[0])
            #fn_ShowJobs(args[0])
            args = args[1:] # shift

    #filename = '/tmp/%s.txt' % os.getpid()
    filename = outputfile
    temp = open(filename, 'w+b')
    
    #print("Array ListDir",list_Dir)
    for eachDir in list_Dir:
        #print(eachDir)
        fn_ShowJobs(eachDir,temp)
    temp.write('int_Count='+str(int_Count)+'\n')

    #print('Output file is "', outputfile)

    #print(tempfile.gettempdir())
    #temp.seek(0)
    #print(temp.read())
    #print("\n\n")

 


    name= 'varname'
    value= 'something'

    temp.close()


if __name__ == "__main__":
   main(sys.argv[1:])


#setattr(self, name, value) #equivalent to: self.varname= 'something'

#print(self.varname)
#will print 'something'
'''      system("echo arr_States["linenum"]="state" >> "file_Cache)
      system("echo arr_Jobs["linenum"]=$(basename "$0") >> "file_Cache)

      linenum++
    }
    END {
      system("echo int_Count="linenum" >> "file_Cache )
    }'
    ##. ${file_Cache}
#       cat "${file_Cache}"
    [[ -r "${file_Cache}" ]] && . "${file_Cache}" && rm "${file_Cache}"


  file_Cache=$(mktemp "${dir_Tmp}"/cache.$$.XXXXX)
  echo "#$$" > "${file_Cache}"

  >>> fp = tempfile.TemporaryFile()
>>> fp.write(echo arr_States[]=state)

import tempfile

    '''


