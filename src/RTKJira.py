import os
from jira import JIRA

class JIRABase:
    mAccount = ""
    mPASSWORD = ""
    mURL = ""
    mJIRA = None
    mAttachmentPath = ""
    mAttachmentName = ""

    def __init__(self):
        pass

    def __del__(self):
        self.Disconnect()

    def Connect(self):
        self.Disconnect()
        options_jira = {
            'server': self.mURL
        }
        self.mJIRA = JIRA(options_jira,basic_auth=(self.mAccount, self.mPASSWORD))

    def Reconnect(self):
        self.Disconnect()
        self.Connect()

    def Disconnect(self):
        if self.mJIRA != None:
            self.mJIRA.close()
            self.mJIRA = None

    def SetAccount(self, account, password):
        self.mAccount = account
        self.mPASSWORD = password

    def SetURL(self, url):
        self.mURL = url

    def SetAttachmentInfo(self, path, name):
        self.mAttachmentPath = path
        self.mAttachmentName = name

class RTKJIRA(JIRABase):
    mProjectName = ''
    mLABEL_KEY_ISSUE = ''
    mLABEL_1 = ''

    def __init__(self, account, passwd):
        super().__init__()
        super().SetAccount(account,passwd)
        super().SetURL("https://jira.realtek.com")
        super().Connect()
        self.mProjectName = ''

    def __del__(self):
        super().Disconnect()
        super().__del__()

    def SetProjectName(self, projectname):
        self.mProjectName = projectname

    def SetProjectLabels(self, key, arg1):
        self.mLABEL_KEY_ISSUE = key
        self.mLABEL_1 = arg1

    def Add_Watcher(self, task_issue, watcher ):
        self.mJIRA.add_watcher(task_issue,watcher)

    def Find_Jira_Id(self,task_issue_key):
        return self.mJIRA.issue(task_issue_key)

    def Link_Task_With_Issues(self, task_key, issue_key):
        self.mJIRA.create_issue_link(type='blocks',inwardIssue=issue_key,outwardIssue=task_key)

    def Create_BUG(self, jira_type, summary, desc, issuetype, comp, pri, freq, assign, epic_link, labels1, labels2, labels3, labels4, env, customerid):
        labels = []
        labels.append(labels1.replace(" ", "_"))
        labels.append(labels2.replace(" ", "_"))
        labels.append(labels3.replace(" ", "_"))
        labels.append(labels4.replace(" ", "_"))
        new_issue = None

        if desc == None:
            desc = "No Description"

        if jira_type == "Task":
            issue_dict= {
                'project': {'key': self.mProjectName},
                'summary': summary,
                'description': desc,
                'components':[{'name': comp}],
                'issuetype': {'name': issuetype},
                'priority': {'name': pri},
                'customfield_12400': {'value': freq},
                'assignee':{'name': assign},
                'labels':labels,
                'environment':env,
                'customfield_10405': epic_link,
            }
        else:
            issue_dict= {
                'project': {'key': self.mProjectName},
                'summary': summary,
                'description': desc,
                'components':[{'name': comp}],
                'issuetype': {'name': issuetype},
                'priority': {'name': pri},
                'customfield_12400': {'value': freq},
                'assignee':{'name': "-1"},
                'labels':labels,
                'environment':env,
                # 'customfield_12100': '',
            }

        new_issue = self.mJIRA.create_issue(fields=issue_dict)

        return new_issue

    def Upload_Attachment(self,issue,filelocation):
        if not os.path.isfile(filelocation):
            print(f"[RTK JIRA][Error] Upload attachment: File not Exist {filelocation}" )

        attach = self.mJIRA.add_attachment(issue=issue, attachment=filelocation)

        if attach.size == 0:
            print("[RTK JIRA][Error] Upload attachment: Upload not complete")
