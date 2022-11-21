import sys
import itertools
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

from pygerrit2 import GerritRestAPI
from requests.auth import HTTPBasicAuth

class RTKGerrit:
    def __init__(self, account=None, password=None, url="https://mm2sd.rtkbf.com/gerrit/"):
        self.auth = HTTPBasicAuth(account, password)
        self.rest = GerritRestAPI(url=url, auth=self.auth, verify=False)
        self.headers = {'Content-Type': 'application/json'}

        self.groupRelationship = dict()
        self.groupMembers = dict()

        self.gerritGroups = dict()

        self.stdout = sys.stdout
        self.stderr = sys.stderr

        self.allAccess = dict()

    def fetch(self, method="GET", url=None):
        assert url != None, "[RTK Gerrit][Error] fetch: API url is required"
        
        if method == "GET":
            return self.rest.get(url, headers=self.headers)
        else:
            print(f"[RTK Gerrit][Error] fetch: Method {method} haven't support yet")
        

    def getGroups(self):
        groups = self.fetch( method="GET", url=f"groups/" )
        
        for group in groups.keys():
            subgroups = self.fetch(  method="GET", url=f"groups/{groups[group]['id']}/groups" )

            self.groupRelationship[group.strip()] = {
                "id": groups[group]['id'],
                "subgroups": {}
            }
            if len(subgroups) > 0:
                for subgroup in subgroups:
                    self.groupRelationship[group]["subgroups"][subgroup['name'].strip()] = {
                        "id": subgroup["id"]
                    }
    
    def getMembers(self, output="member.log"):

        f = open(output, "w+")
        sys.stdout = f

        for group in self.groupRelationship.keys():
            print(group)
            
            members = self.fetch(  method="GET", url=f"groups/{self.groupRelationship[group]['id']}/members/?recursive" )
            if len(members) == 0:
                print(f"[Error] Empty group {group}")
            for member in members:
                print(f"\t{member['name']} <{member['email']}>")

        f.close()
        sys.stdout = self.stdout

    # ToDo
    # Analyze the access of each project
    def getInheritsAccess(self, origin_project, project):
        access = self.fetch( url=f"projects/{project.replace('/', '%2F')}/access" )

        if "inherits_from" not in access.keys():
            self.allAccess[origin_project].append(access["local"])
        else:
            inheritesProject = access["inherits_from"]["name"]
            self.allAccess[origin_project].append(access["local"] )
            self.getInheritsAccess(origin_project, inheritesProject)

    def getAccess(self):
        # projects = self.fetch( url=f"projects/" )
        projects = {"realtek/jarvis": "" }
        
        for project in projects.keys():
            self.allAccess[project] = []

            access = self.fetch( url=f"projects/{project.replace('/', '%2F')}/access" )
            
            if "inherits_from" not in access.keys():
                self.allAccess[project].append(access["local"])
            else:
                inheritesProject = access["inherits_from"]["name"]
                
                self.allAccess[project].append(access["local"])
                self.getInheritsAccess(project, inheritesProject)
                
        print(self.allAccess)
    
    def flattenGroup(self, count, groupName):
        prefix = ['\t' for i in range(count)]
        print(f"{''.join(prefix)}{groupName}")
        
        if groupName.startswith("user/") or len(self.groupRelationship[groupName]["subgroups"].keys()) == 0:
            return    
        else:
            for subgroup in self.groupRelationship[groupName]["subgroups"].keys():            
                if subgroup == groupName:
                    print(f"[Error] Infinity recursive {subgroup}")
                if subgroup != groupName:
                    self.flattenGroup(count+1, subgroup)

    def getGroupRelationship(self, output="relationship.log"):
        
        f = open(output, "w+")
        sys.stdout = f

        for key in self.groupRelationship.keys():
            self.flattenGroup(0, key)
        
        f.close()
        sys.stdout = self.stdout

if __name__ == '__main__':
    rtkGerrit = RTKGerrit(account="yang.yuming", password="w/Tql7LbY3dQujCAe3eQGQxL16I1EZTZqCx5YoeYRw")
    # rtkGerrit.getGroups()
    # rtkGerrit.getGroupRelationship(output="relationship.log")
    # rtkGerrit.getMembers()
    rtkGerrit.getAccess()
