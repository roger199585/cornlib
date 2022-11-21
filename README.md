# cornlib

Python module library for analyze datas from JIRA and Gerrit in RTK

## Feature
* RTKJira
    * This calss ecapsulation the JIRA Restful API
    * This feature is develop to create JIRA by script, so tha that we can report the test issue onto JIRA automatically.

* RTKGerrit
    * This class encapsulation the Gerrit Restful API
    * This feature is develop to statistic the infomation on Gerrit

## Usage
### RTKJira
* Authentication
```
from cornlib import RTKJira

jira_account = "your account"
jira_pwd = "you password" # In RTK we only support basic authentication

rtkjira = RTKJira.RTKJira(account=jira_account, password=jira_pwd)
```

### RTKGerrit
* Authentication
```
from cornlib import RTKGerrit

gerrit_account = "your account"
gerrit_pwd = "you password" # You can user the token that generated in setting page

rtkGerrit = RTKGerrit.RTKGerrit(account=gerrit_account, password=gerrit_pwd)
```