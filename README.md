[![GitHub license](https://img.shields.io/github/license/marlof/ScORCH)](https://github.com/marlof/ScORCH/blob/master/LICENSE) [![GitHub issues](https://img.shields.io/github/issues/marlof/ScORCH)](https://github.com/marlof/ScORCH/issues) [![CI](https://github.com/marlof/ScORCH/actions/workflows/ci.yml/badge.svg?branch=dev)](https://github.com/marlof/ScORCH/actions/workflows/ci.yml)

ScOrch Suite
============

Simplicity is a great virtue but it requires hard work to achieve it and education to appreciate it. - Edsger W. Dijkstra


# DevOps Software Orchestration

This will install the latest version (released or otherwise) into the current directory:

`wget https://s3.eu-west-2.amazonaws.com/autoscorchdownload.com/install && chmod a+x install && ./install`

Once you have installed ScOrch, try the following:

Press the "n" & Enter to create a new job. ScOrch will refresh all the available plugins, display them to the screen and then drop into an input area.

        INSTALL:        AZURECLI        OK
        INSTALL:            JAVA        OK
        INSTALL:           NEXUS        OK
        INSTALL:       TERRAFORM        OK
          LOCAL:  LOCAL-SAFEDEMO        OK
          LOCAL:         LONGRUN        OK
          LOCAL:        SAFEDEMO        OK
          LOCAL:         VAGRANT        OK
             PI:          PI-VPN        OK
             PI:          VECTOR        OK
           TEST:            TEST        OK

     help <plugin>    at any time for additional parameters
     info <plugin>    for further information

     Please enter the request below.
     To complete the request is use a fullstop on a newline:
     (To quit type CANCEL)

  
Copy and paste the following template (include the full stop on a new line to teminate the input stream)
    
    Action : DRINK-TEA
    Size   : Mug
    Milk   : 1
    .
    
A new job will now be created in ScOrch. Enter the number of the job and feel free to explore the context menu options

    ---Job-Details---------------------------------------------------------------------------------------------------------
     str_Owner=scorch
     State at selection : new
    Job_ID-280_280.DRINK-TEA.1_DRINK-TEA_NA_

    -rwxrwxrwx 1 scorch scorch 8514 Feb 20 21:38 /home/scorch/jobs/active/Job_ID-280_280.DRINK-TEA.1_DRINK-TEA_NA_
    -rwxrwxrwx 1 scorch scorch 39 Feb 20 21:38 /home/scorch/var//log//Job_ID-280_280.DRINK-TEA.1_DRINK-TEA_NA_.log


    ---Template------------------------------------------------------------------------------------------------------------
    Action : DRINK-TEA
    Size   : Mug
    Milk   : 1

    ---Log-Summary---------------------------------------------------------------------------------------------------------
    220220-213820 Created by:scorch Tasks[8]

    -----------------------------------------------------------------------------------------------------------------------

     Amend rules | Copy | View | Edit | Log | tail | Queue | Tasks | Delete | Filter | eXit :

Tasks is a good place to start to understand what the job consists of.

Repeatable

Brilliant in it's simplicity

# Directory Structure

ScORCH does not require building, but does have a unique directory structure

```
scorch/
+--bin/                     Some useful shell scripts
+--etc/                     Config files users and motd
+--functions/               Collections of ScORCH functions
+--jobs/                    Jobs and job status information
   +--active/               Job files
   +--archived/             symlinks of deleted jobs
   +--completed/            symlinks of completed jobs
   +--deleted/              symlinks of deleted jobs
   +--failed/               symlinks of jobs that have failed
   +--fixing/               symlinks of failed jobs that have been acknowledged
   +--manual/               symlinks of jobs waiting for manual intervention
   +--new/                  symlinks of new jobs
   +--pending/              symlinks of jobs waiting for other actions
   +--queued/               symlinks of queued jobs waiting for the dispatcher
   +--running/              symlinks of running jobs
   +--starting/             symlinks of jobs waiting for the owners session
+--plugins/                 ScORCH plugin
   +--DEMO/
   +--LOCAL/
   +--CUSTOM/               Directory for plugins local to a customer
+--projects/                Obrar projects (and sym link ScORCH plugins)
   +--common/
      +--(bin)/
      +--etc
      +--functions/
   +--demo/
   +--customname/
+--python/                  Where show jobs is held in speedier python
+--tmp/                     Holding area for Action buildup
+--var/                     Logs and locks and obrar stats
```

Standard Features

* Add Jobs
* Plugins Engine
* State Engine
* Notification / Communication Engine
                      
Enterprise features

* Authentication / Security  Module
* Alternative Paths
* Audit Module
* Report Module
* Admin tasks Module
                      
                      
