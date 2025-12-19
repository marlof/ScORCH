#!/bin/bash

file_Request=/tmp/getvar.tmp
echo "x : 1" > "${file_Request}"
echo "y : 1 2 3" >> "${file_Request}"

GetVar()
{
  # Exception to the naming convention is GetVar. This is used in plugins by users
  #
  # This function is used to set global variables with value pairs from templates
  # =============================================================================
  #
  # Given    KEYNAME : VALUE
  # In a template, 
  # 
  # -label  "<key name>"          specifies the key name search string
  # -name   "<variable name>"  the global variable to assign the VALUE to
  # -c                         Enforce case in the label pattern
  # -default "<value>"         Set a default is no value passed
  # -list                      Expect a list of values into an array by space or comma
  #
  # awk 20070501 does not allow ignorecase so dont worry if it doesnt work
  # Examples
  #
  # GetVar -pattern "data label" -name DATA_LABEL -d "None"
  local str_Pattern=
  local str_Name=
  local str_Value=
  local str_Default=
  local b_IgnoreCase=1
  local b_List=
  local b_Upper=
  local b_Lower=
 
  if [ $# -ne 0 ] ; then
    while [ $# -gt 0 ] ; do
      case "${1}" in
        -pattern ) shift ; str_Pattern="${1}" ;;
        -name    ) shift ; str_Name="${1}"    ;;
        -default ) shift ; str_Default="${1}" ;;
        -c       )         b_IgnoreCase=0     ;;
        -list    )         b_List=1           ;;
        -upper   )         b_Upper=1          ;;
        -lower   )         b_Lower=1          ;;
      esac
      shift
    done
  fi

  ## Awk is a pain if the items are in a list so handle lists separately
  ## ===================================================================
  if [ "${b_List}" ] ; then
    ## Lists can be passed as a space, comma or ampersand separated list 
    ## i.e. KEYWORD : ENV1, ENV2 ENV3 & ENV4
    str_Value="$(${cmd_AWK} 'BEGIN {
       FS=":"
       IGNORECASE='"$b_IgnoreCase"' }
       $1 ~ /^ *'"$str_Pattern"'/ {print $2}'       "${file_Request}" | sed -e 's/[,&]/ /g' )"
  else
    ## If the item is not a list, get rid of any spaces and tabs with gsub
    ## ===================================================================
    str_Value="$(${cmd_AWK} 'BEGIN {
       FS=":"
       IGNORECASE='"$b_IgnoreCase"' }
       $1 ~ /^ *'"$str_Pattern"'/ {gsub (/[ \t]+/, "");
         $2=$2;
         print $2}'       "${file_Request}" )" 
  fi

  ## If a value hasnt been found or is empty, use the default if one is set
  ## ======================================================================
  [[ "${str_Value}" ]] || str_Value=${str_Default}
  [[ "${b_Upper}"   ]] && str_Value=${str_Value^^}
  [[ "${b_Lower}"   ]] && str_Value=${str_Value,,}
        # tmp=${1:1}               # Strip off leading '/' . . .
         # str_Name=${tmp%%:*}     # Extract name.
         # str_Value=${tmp##*:}         # Extract value.
         # eval $str_Name=${str_Value}

  echo "here ${str_Name}=\"${str_Value}\""
  #eval "${str_Name}=\"${str_Value}\""
}
