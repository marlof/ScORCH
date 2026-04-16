# ScORCH Changelog

Full version history extracted from the `scorch` script header.
Current version: **3.1.17** (Codename: Fafnir)

---

## 3.x

| Version | Date   | Author | Notes |
|---------|--------|--------|-------|
| 3.1.17  | 260106 | marc   | #201 - Improved plugin loading security checks |
| 3.1.16  | 251214 | marc   | #198 - Improved screen width handling |
| 3.1.15  | 240615 | marc   | #196 - Improved Dispatcher Functions. Changed ++ increments |
| 3.1.14  | 240610 | marc   | Refactor fn_GetRequest |
| 3.1.13  | 240608 | marc   | #197 - Added view plugin feature, improved help and info feature options |
| 3.1.12  | 240326 | marc   | #193 - Update to fn_MV for take ownership tasks |
| 3.1.11  | 240129 | marc   | #186 See archived jobs |
| 3.1.10  | 240116 | marc   | #190 Handle duplicated main vars that are not list. #191 COLUMNS default updated. Switched more mv to fn_Mv |
| 3.1.9   | 240108 | marc   | #189 export COLUMNS to showJobs.py. #188 Strip non printable characters |
| 3.1.8   | 231228 | marc   | #185 Fixed jobstate differences |
| 3.1.7   | 231223 | marc   | #182 Adding Documentation Feature. Small typo fix. Fixed fn_Audit when job state unknown |
| 3.1.6   | 231223 | marc   | Improvement to CheckLatest function |
| 3.1.5   | 231222 | marc   | #184 Adding str_Group option as preferences |
| 3.1.4   | 231205 | marc   | #183 Fixed globbing issue for bash ShowJobs2 |
| 3.1.3   | 231019 | marc   | #181 Adding Manual comment options |
| 3.1.2   | 231017 | marc   | Improvement for permission issue jobs |
| 3.1.1   | 231017 | marc   | Improvement for permission issue jobs |
| 3.1.0   | 231006 | marc   | #180 Fixed dispatcher |
| 3.0.9   | 231005 | marc   | Improvement for corrupt jobs |
| 3.0.8   | 231002 | marc   | #179 Hardened python calls. Added TERM default for docker version |
| 3.0.7   | 230312 | marc   | #178 Code Cleanup |
| 3.0.6   | 230130 | marc   | #177 Fix tar find local and install directory. #173 Added noglob |
| 3.0.5   | 230121 | marc   | #175 Add help documentation |

---

## 2.x

| Version | Date   | Author | Notes |
|---------|--------|--------|-------|
| 2.13.4  | 220719 | marc   | Not all envs have Python |
| 2.13.3  | 220627 | marc   | Fixed setup URLs after autoscorch migration |
| 2.13.2  | 211201 | marc   | #168 Added disabled plugin count |
| 2.13.1  | 211124 | marc   | #165 Confirm update. #167 cancel tee issue |
| 2.13    | 211117 | marc   | #164 LogWhy update |
| 2.12    | 210830 | marc   | Shellcheck updates |
| 2.11    | 210820 | marc   | Updates to typeset |
| 2.10    | 210503 | marc   | Shellcheck for created jobs |
| 2.9.18  | 210426 | marc   | Adding Trim function to clean variables |
| 2.9.17  | 210325 | marc   | #161 Fixed StartGroup Copy issue |
| 2.9.16  | 210324 | marc   | Fixed resume from unknown task state |
| 2.9.15  | 210318 | marc   | #154 Added flock check block. Improved GetVar. Added schedule keypair |
| 2.9.14  | 210318 | marc   | #158 Adding ability to use \<num>\<task> like 1t |
| 2.9.13  | 210122 | marc   | tput fails in some systems. Added installation owner |
| 2.9.12  | 201208 | marc   | "cancel" a task fixed |
| 2.9.11  | 201107 | marc   | "T" task not registered |
| 2.9.10  | 201107 | marc   | Fafnir - #149 Copy Template feature |
| 2.9.9   | 201103 | marc   | Fix "(C)hange Rules triggers (c)ancel" |
| 2.9.8   | 200725 | marc   | Allow sort of plugins |
| 2.9.7   | 200622 | marc   | Changed python call |
| 2.9.6   | 200613 | marc   | #145 Remove gawk requirement |
| 2.9.5   | 200528 | marc   | chmod fix |
| 2.9.4   | 200404 | marc   | #143 curl failure causes scorch to exit fix |
| 2.9.3   | 200324 | marc   | #12 info option |
| 2.9.2   | 200323 | marc   | fn_Call |
| 2.9.1   | 200321 | marc   | Python3 for showJobs |
| 2.9.0   | 200302 | marc   | Hangup to kill improvements |
| 2.8.9   | 200116 | marc   | #136 Fixed fail from exit tasks |
| 2.8.8   | 200109 | marc   | #137 Fix failing exits from plugins |
| 2.8.7   | 191220 | marc   | shellcheck lintifying |
| 2.8.6   | 191213 | marc   | Adding Path updates for customer |
| 2.8.5   | 191203 | marc   | Improved rules |
| 2.8.4   | 191128 | marc   | #12 Some estimated run time work |
| 2.8.3   | 191127 | marc   | #133 Fix abrupt exit with no users file |
| 2.8.2   |        | marc   | #132 Allow access to "log" from task list |
| 2.8.1   |        | marc   | #124 Adding /dev/shm alternative for other OS. #126 SetPrefs not required when non-interactive. #127 Adding strict mode. #129 Adding timeout feature |
| 2.8     |        | marc   | #121 Started shared drive / multi host work |
| 2.7.6   |        | marc   | #108 deleted jobs deactivated (removed execute) |
| 2.7.5   |        | marc   | Stop current user being added to /etc/users (install script) |
| 2.7.4   |        | marc   | Checks include python |
| 2.7.3   |        | marc   | #118 Fixed str_Group check when in prefs |
| 2.7.2   |        | marc   | #117 Fixed double run issue when using -s from background job |
| 2.7.1   |        | marc   | #115 Run jobs with newgrp is str_Group set |
| 2.7     |        | marc   | #109 Killed jobs report last running task |
| 2.6.7   |        | marc   | #111 COLUMNS update + others |
| 2.6.6   |        | marc   | Kafka/Docker/Ubuntu demo plugins |
| 2.6.5   |        | marc   | #106 -u - more work on undefined arrays |
| 2.6.4   |        | marc   | #105 -e mode turned to requestable until resolved |
| 2.6.3   |        | marc   | #105 Super Strict Mode |
| 2.6.2   |        | marc   | #104 StartTime issue fixed |
| 2.6.1   |        | marc   | #99 bash -n added |
| 2.6     |        | marc   | #93 Group updates. #95 Dynamic column sizing in python |
| 2.5.1   |        | marc   | Patch after testing on live |
| 2.5     | 190107 | marc   | #90 str_Group additional fixes |
| 2.4     | 190104 | marc   | #92 Allow plugins to fail the creation of a job |
| 2.3     |        | marc   | dir_Orig fixed |
| 2.2     | 181207 | marc   | #88 Local install version improved |
| 2.1     | 181206 | marc   | #87 Add Error and Message tasks + fix to subgroup output |
| 2.00    | 181124 | marc   | #46 Install plugins from plugin library. #86 Added LogWhy to Cancel function |

---

## 1.x (Codename: Amarok)

| Version | Date   | Author | Notes |
|---------|--------|--------|-------|
| 1.60    | 181121 | marc   | #83 Dispatcher exits if jobs directory missing |
| 1.59    | 181120 | marc   | #82 Update for ps bash under windows bug |
| 1.58    | 181119 | marc   | #81 Adding Mandatory GetVar feature |
| 1.57    | 181114 | marc   | #80 Try tasks that fail are not shown in task output |
| 1.56    | 181107 | marc   | #79 Manual state defined |
| 1.55    | 181028 | marc   | Formatting improvement |
| 1.54    | 181027 | marc   | #78 Scorch Group testing |
| 1.53    | 181022 | marc   | #72 Manual message when in sub-group. #73 Filter added to job name. Quiet grep for check owner. Tee option changed back. #74 Resume from Manual state. #75 coloured disk space fixed |
| 1.52    | 181021 | marc   | #66 Plugin manager added. Codename Amarok. #69 #70 fixed |
| 1.51    | 181004 | marc   | #60 showline improved output for CR. #59 Improved for first install. #62 Bug fix. #63 Try fix. #64 "d" context missing. #65 admin job numbering fixed. #68 motd file |
| 1.50    | 181001 | marc   | #59 Improvement to memory shm link |
| 1.49    | 180922 | marc   | Improvement to #51 |
| 1.48    | 180912 | marc   | Jenkins build test. #51 IsAlreadyRunning function. #55 #56 #57 #58 fixes |
| 1.47    | 180906 | marc   | Added associative array check. #48 #49 #50 improvements |
| 1.46    | 180905 | marc   | #47 Sort "skip" steps in new mode |
| 1.45    | 180904 | marc   | #45 Associative array to track TASK status |
| 1.44    | 180821 | marc   | Improvement to DF output. #43 Group Manual steps Completed |
| 1.43    |        | marc   | #42 Removed debug code. tmp dir changes. /dev/shm link. #44 #38 improvements |
| 1.42    |        | marc   | Removed formatting space. #40 Confirmation function. #41 Alternative location for auto install files |
| 1.41    |        | marc   | #34 Included task and tail quick mode fix |
| 1.40    |        | marc   | #37 Add maintenance mode |
| 1.39    |        | marc   | #39 Add scorch definition to CSV file |
| 1.38    |        | marc   | Improved versions feature for correct MD5 |
| 1.37    |        | marc   | #23 curl install |
| 1.36    |        | marc   | #36 Improved for multi dispatcher |
| 1.35    |        | marc   | #23 Added new version features |
| 1.34    |        | marc   | #24 abort jobs. #34 b_Quick fix. #35 Refresh improvement |
| 1.33    |        | marc   | read quick for experts and slow for novice |
| 1.32    |        | marc   | Resume after pause fixed #31. Pause and Rules flags shown #32 |
| 1.31    |        | marc   | cache file no longer shared |
| 1.30    |        | marc   | shell read command now reads in raw (-e) |
| 1.29    |        | marc   | _(no notes)_ |
| 1.28.1  |        | marc   | Minor format fix |
| 1.28    | 180518 | marc   | Working with CentOS |
| 1.27    | 180516 | marc   | github#29 Resume from Tasks. github#30 Manual Tasks |
| 1.26    | 180511 | marc   | Resumed Group Jobs shows number of failures |
| 1.25    | 180509 | marc   | Resume group tasks |
| 1.24    | 180503 | marc   | Publish functions updated to include Python |
| 1.23    | 180502 | marc   | Completed list is showjobs.py reversed |
| 1.22.1  | 180424 | marc   | Issue #28 resolved |
| 1.22    | 180424 |        | Task display updates |
| 1.21dev | 180207 | marc   | Fixing TASK for none running jobs. Adding plugin manager. dos2unix on showJobs.py. Wait group improvements |
| 1.20    | 171204 | marc   | Trial python for showJobs |
| 1.19    | 171018 | marc   | Added lower and upper options for GetVar. Working on breakTask |
| 1.18    | 171015 | marc   | Formatting program and output. Improved %age call for disk space. Added timer to running jobs |
| 1.17    | 170922 | marc   | Added update notification to Context Menu |
| 1.16    | 160713 | marc   | Fixed job owner reporting. Old active jobs recovered from archive |
| 1.15    | 160211 | marc   | Protected header comment lines. GAWK and NAWK checks. Improved owner check. JobID changed |
| 1.14    | 160126 | marc   | Indicate Job Owner. pauseTask added. breakTask added |
| 1.13    | 160114 | marc   | Added preferences for SHOWMAX and REFRESH |
| 1.12    | 151223 | marc   | Added fix in progress. Cleaned up some code |
| 1.11    | 151127 | marc   | Fixed issue with LOCK filename. github#20 Tail feature added. github#13 Added tryTask option |
| 1.10    | 150817 | marc   | Removed System as a key-pair. Updated comments. Added upper flag to GetVar. Toggle pause flag |
| 1.9     | 150805 | marc   | Check for outstanding jobs on exit |
| 1.8     | 150805 | marc   | Improvement to manager layout with dynamic column width |
| 1.7     |        | marc   | #15 log update. #16 multi job update. Shell check updates. Trap updates. Enterprise feature multi-parent rule enabled |
| 1.6     |        | marc   | Audit handling. Failed job audit tracking. Enterprise Feature (Developer:Debug) |
| 1.5     |        | marc   | Jobs now use symbolic links |
| 1.4     |        | marc   | Further improvements to task list |
| 1.3     |        | marc   | Improved task list, began lock manager and task manager |
| 1.2     |        | marc   | Improved fn_ShowJobs2, pause feature |
| 1.1     |        | marc   | Reversed and improved fn_RunJobs |
| 1.0     |        | marc   | First running demo |
