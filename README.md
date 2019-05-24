ScORCH Suite
============

Announcing 2.6


DevOps Software Orchestration

This will install the latest version (released or otherwise) into the current directory:

`wget http://www.autoscorch.com/downloads/install && chmod a+x install && ./install`

Repeatable

Brilliant in it's simplicity

Standard Features

                      Add Jobs
                      
                      Plugins Engine
                      
                      State Engine
                      
                      Notification / Communication Engine
                      
Enterprise features

                      Authentication / Security  Module

                      Alternative Paths
                      
                      Audit Module
                      
                      Report Module
                      
                      Admin tasks Module
                      
                      
TM Challenge
============

Overview
========

Please find attached my submission.

# tMan.py 		python source code for Thought Machine Service Manager
# README.md 	this file


Develoment approach
===================
# step 1 make it work
# step 2 make it right
# step 3 make it fast

Due to the time constraint and having external factors influencing my
time I will be lucky to get through step 1 and make it work.

	Actual time spent *14 hours*

Outcome 1 and 3 have been completed.
Outcome 2 and 4 - out of time.


Running
=======

I have been running my script from a bash command line. It can be run with -d for debug which
also shows the simulation tests

		./tMan.py

					 IP|             Service|                 CPU|              Memory|              Status|
		--------------------------------------------------------------------------------------------------------------
			  10.58.1.1|      StorageService|                 33%|                 56%|             Heathly|
			 10.58.1.10|         RoleService|                 25%|                  3%|             Heathly|
			10.58.1.100|         RoleService|                 78%|                 31%|            Degraded|
			10.58.1.101|         RoleService|                 63%|                 19%|             Heathly|
			10.58.1.102|         RoleService|                 56%|                 34%|             Heathly|
			10.58.1.103|           MLService|                 64%|                 72%|             Heathly|
			10.58.1.104|       TicketService|                 51%|                 54%|             Heathly|
			10.58.1.105|         RoleService|                 99%|                 49%|           Unhealthy|
			10.58.1.106|           MLService|                 39%|                 17%|             Heathly|
			10.58.1.107|         AuthService|                 23%|                 45%|             Heathly|
			10.58.1.108|          GeoService|                  2%|                 76%|            Degraded|
			10.58.1.109|         AuthService|                 35%|                 75%|            Degraded|
			 10.58.1.11|           MLService|                 22%|                  3%|             Heathly|
			10.58.1.110|         TimeService|                 11%|                 86%|           Unhealthy|
			10.58.1.111|       TicketService|                 22%|                100%|           Unhealthy|

You may notice an addition Status of "Degraded". This is a service which has values that have broken 
a warning threshold which can be set at variables.

		# Healthy/unhealthy thresholds
		int_AmberCPU          = 75              # Please change this to suit your needs
		int_AmberMemory       = 75              # Please change this to suit your needs
		int_RedCPU            = 85              # Please change this to suit your needs
		int_RedMemory         = 85              # Please change this to suit your needs
		int_ServiceCountLimit = 2               # Customisable number of services to alert on unheathly services

Troubleshooting
===============

If you see error like these, they are coming from *requests*. It may be that you have not started the cpx or it is on a different port
		requests.exceptions.ConnectionError: HTTPConnectionPool(host='localhost', port=8889): Max retries exceeded with url: /servers (Caused by NewConnectionError('<requests.packages.urllib3.connection.HTTPConnection object at 0x7f7682426c88>: Failed to establish a new connection: [Errno 111] Connection refused',))

A try: was attempted but need to look at it in further development.


Development Environment
=======================

Developed using BASH 4.3.46.1 for Windows 10 and Python 3.5.2
Using sublime as text editor

I began with some demo data and didnt use the cpx script until version 1.1
then I struggling to get the output of the http request into a dictionary named
after the IP so moved on for a bit and came back to that.


Challenges
==========

My primary scripting language is BASH - only switching to python if
I need to speed part of it up so I havent used very often.

With that in mind, please excuse me if some of the contructs are not
"python" class/method enough (yet).

Using more python will be an area for growth for me, but I hope I have 
demonstrated some level of knowledge even though I did not complete the
task or have time to refactor.


Considerations
==============

Try to make the functions as generic as possible to allow more re-use and adatability
Some services may return a different number of key pairs
Some services may use upper/lowercase differences in key names - just be aware if hashing and use k.upper() of k.lower()
Some services may stop using % signs and may simply switch to numeric so use str.replace()
Create a hash of services to do counts (or use count from keys would be quicker)
Dont limit the columns just to those shown - allow additional columns and thresholds, ordering and filters
  e.g - the service may choose to also report a version which can be used for feature control.


Future Improvements
===================

Extand to be python 2 or 3 agnostic
Check for service down, long delays, http success/error codes 2xx success messages, 4xx clients errors, 5xx server errors
Validate that the server is an IP or valid hostname (dont limit it to IP's )
Allow config driven customisable threshold per service i.e AuthService may be ok to have higher memory usage
Some effort has already been invested in the creation of specific functions in order to allow return on investment if/when changes are required
Run it as a container
More then one service may come from the same IP (different ports/shared services) so beware that a hash may overwrite
Create/use other peoples library functions that have already some of the actions. 



















                      
