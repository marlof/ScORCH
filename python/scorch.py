#!/usr/bin/python3
'''
scorch py development only

Optional arguments:
-h , --help       show this message and exit


== Examples ==

x y z

== History ==

<github>


'''
import logging
import time

LOG_FORMAT = "%(asctime)s %(levelname)-8s - %(message)s"
logging.basicConfig(filename = "/tmp/lumberjack.log",
                     format = LOG_FORMAT,
                     level = logging.DEBUG )

                     #format = LOG_FORMAT,
                     #filemode = "w")

#logger = logging.getlogger()

# Test messages
#logging.debug('This is a DEBUG message')
#logging.info('Well thats just INFO')
#logging.warning('Careful now. Thats a WARNING')
#logging.error('I told you to be careful - Youve ERRORed')
#logging.critical('XXX XXX XXX CRITICAL XXX XXX XXX')

global warncount
warncount = 0
def warn(msg):
  logging.warning(msg)
  #warncount += 1

def yesno(prompt):
  '''returns True if answer is y or Y'''
  answer = input(prompt + " (Y/N): ")
  return answer.strip().lower() == "y"

Debug = logging.debug
Message = logging.info
Warning  = logging.warning
Error = logging.error
Critical = logging.critical
Debug('Hello')
Warning('This is a warning')
warn('This is also a warn warning')
if yesno('Did this work?'):
  print("It's a yes from me")
else:
  print("That's a shame")

job_status = 'unknown'
wait_time = 20
while True:
  logging.info('Job status: {}'.format(job_status))
  if job_status == 'complete' : break
  time.sleep(wait_time)