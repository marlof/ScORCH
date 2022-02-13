# obrar
Scripted Deployment framework

obrar[1.0]

NAME
        obrar - deployment runbook automation framework

SYNOPSIS
        obrar [ [-h] | [-l [str]] [-v] ] ] <TAG> [ <TAG arguments> ]

DESCRIPTION
        This script passes arguments to a set of predefined functions to ensure
        a repeatable, auditable, consistent run of functions

OPTIONS

        -h, --help              Show this help and version

        -l, --list [str]        List Tags or list tags matching string

        -t, --timings [str]     Show previous timing for functions in tags

        -v, --verbose           Verbose output


        -install                Create initial directory structure


        <TAG> <args>            The TAG to call. Anything after the TAG
                                will be treated as an argument to the tag

EXAMPLES

        obrar -v DEMO

        Will show verbose output from obrar and run functions/
        defined in the obrar.def file by the DEMO tag

        obrar DEMO -v

        Will run functions defined in the obrar.def file and
        pass the -v flag as an argument to the DEMO tag

        obrar -l

        List all TAG definitions from all obrar.def files

        obrar -l DEM

        List all TAG definitions from all obrar.def files that
        contain the matching string 'DEM' either in tag name, variables or
        function list

