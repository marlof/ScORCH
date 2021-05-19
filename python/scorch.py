#!/usr/bin/python3
import logging

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

warncount = 0
define Warn(msg):
  logging.warning(msg)
  warncount = warncount++

Debug    = logging.debug
Message  = logging.info
#Warning  = logging.warning
Error    = logging.error
Critical = logging.critical
Debug('Hello')
Warning('This is a warning')
Warn('This is also a warn warning')
