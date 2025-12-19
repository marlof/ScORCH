#!/bin/bash

PROGNAME=${1:-}
if [[ -f ../${PROGNAME} ]] ; then
  # Check that $PROGNAME has a help function
  TEST="NAME"
  RESULT=$(../$PROGNAME -h && echo NOTNULL || echo "ERROR")
  printf "1:"
  [[ "${TEST}" =~ ${RESULT:1:4} ]] && echo "PASS" || echo "FAIL:${TEST:1:4}!=${RESULT:1:4}"



  # Check that -l works
  cat > txtdb << EOF
#DEF COLA COLB COLC
A B C
1 2 3
EOF
  TEST=" -COLA -COLB -COLC"
  RESULT="$(../$PROGNAME -l)"
  printf "2:"
  [[ "${TEST}" == "${RESULT}" ]] && echo "PASS" || echo "FAIL"
  rm txtdb 


  # Check that -f works
  cat > myfile << EOF
#DEF COL1 COL2 COL3
A B C
1 2 3
EOF
  TEST=" -COL1 -COL2 -COL3"
  RESULT="$(../$PROGNAME -f myfile -l)"
  printf "3:"
  [[ "${TEST}" == "${RESULT}" ]] && echo "PASS" || echo "FAIL"
  TEST="A B C"
  RESULT="$(../$PROGNAME -f myfile A)" 
  printf "4:"
  [[ "${TEST}" == "${RESULT}" ]] && echo "PASS" || echo "FAIL"
  rm myfile


  # Check the field seperator works
  cat > fieldfs << EOF
#DEF COL1 COL2 COL3
#FS=:
A:B:C
1:2:3
EOF
  TEST="B"
  RESULT="$(../$PROGNAME -f fieldfs -l && ../$PROGNAME -f fieldfs -COL2 A)"
  printf "5:"
  [[ "${TEST}" == "${RESULT}" ]] && echo "PASS" || echo "FAIL"
  rm fieldfs
fi