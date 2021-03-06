[![GitHub license](https://img.shields.io/github/license/marlof/ScORCH)](https://github.com/marlof/ScORCH/blob/master/LICENSE) [![GitHub issues](https://img.shields.io/github/issues/marlof/ScORCH)](https://github.com/marlof/ScORCH/issues)

ScORCH Suite
============

Simplicity is a great virtue but it requires hard work to achieve it and education to appreciate it. - Edsger W. Dijkstra


# DevOps Software Orchestration

This will install the latest version (released or otherwise) into the current directory:

`wget http://www.autoscorch.com/downloads/install && chmod a+x install && ./install`

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
                      
                      
