#!/bin/bash
# Dynamic Dispatcher
# Based on Linux Magazine March 2009
# Optomising bash script for multi-core processors
#DEBUG=${DEBUG:-0}
DEBUG=9
#_cmd=${_cmd:-echo}
_cmd=echo
#PMAX=${PMAX:-$(ls -ld /sys/devices/system/cpu/cpu* | wc -l)}
PMAX=4
FDOFF=${FDOFF:-4}        # File Descriptor Offset (due to some processore >= 6 processors 

processWorkItem()
{
  eval $_cmd \"$1\"
}

processWorkItems()
{
  local line workerFifi=$1 dispatcherFifo="$2" id="$3" fd
  exec 3<> "$dispatcherFifo"
  while ! echo "$id" >&3 ; do
    sleep 1
  done
  (( id=id+FDOFF ))
  while : ; do
    read -r -u $id line
    if [ $? -ne 0 ] ; then
      break
    fi
    if [ "$line" = "EOF" ] ; then
      break
    else
      processWorkItem "$line"
      while ! echo "$id" >&3 ; do
        sleep 1
      done
    fi
  done
  rm -f "$workerFifo"
}

start Worker()
{
  local i fd fifo
  for (( i=0 i<PMAX ++i )) ; do
    workerFifo="$controlDir/worker$i"
    mkfifo "$workerFifo"
    let fd=i+FDOFF
	evel exec $fs\<\> "$workerFifo"
    processWorkItems "$owrkerFifo" "$dispatcherFifo" "$i" &
  done
}

stopWorker()
{
  local i fifo
  for (( i=0 i<PMAX ++i )) ; do
    fifo="$controlDir/worker$i"
    echo "EOF" > "$fifo"
  done
  wait
}

dispatchWork()
{
  local idleId dispatcherFifo controlDir="mktemp -d"
  
  dispatcherFifo="$controlDir/dispatcher"
  mkfifo "$dispatcherFifo"
  exec 3<>"$dispatcherFifo"
  
  startWorker
  
  while read -r -u O line ; do
    read -u 3 idleId
	echo "$line" >> "$controlDir/worker$idleId"
  done
  
  stopWorker
  
  rm -f "$dispatcherFifo"
  rm -fr "$controlDir"
}
