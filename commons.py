#list of all common functions

from atlassian import Jira


def jira_login(JiraDetails):
    jira = Jira(
        url=JiraDetails['url'],
        username=JiraDetails['email'],
        password=JiraDetails['token'],
        cloud=True)
    return jira
    
def generate_JQL(project,query):
    JQL = f'project = {project}'
    if query:
        JQL = JQL+" AND "+query
    print("\n\n JQL : ",JQL)
    return JQL 
    
    

def check_jira_cloud_token(jiraDetails):
    return True


def get_JIRA_Projects(jiraDetails):
    try:
        print("get_JIRA_Projects jiraDetails : ",jiraDetails)
        jira = Jira(url=jiraDetails["url"],
                    username=jiraDetails["email"],
                    password=jiraDetails["token"],
                    cloud=True)
        list_projects = jira.get_all_projects()
        projects = []
        for project in list_projects:
            projects.append({"key"  :project["key"],
                             "name" :project["name"]})
        return projects
    except Exception as e:
        print("Error occured at get_JIRA_Projects : ",e)


def get_issue_types_with_icon(issue_types):
    types_list = []
    for issuetype in issue_types:
        types_list.append({"name": issuetype['name'], "icon" : issuetype['iconUrl']})
    return types_list

def get_project_details(jira, project_key):
    project = jira.get_project(project_key, expand=None)
    users = jira.get_all_assignable_users_for_project(project_key, start=0, limit=1000)
    try:
        return {"name":project['name'],
                "key": project['key'],
                "desc": project['description'],
                "issueTypes": get_issue_types_with_icon(project['issueTypes']) ,
                "total_users" : len(users),
                "project_icon" : project['avatarUrls']['48x48']
                }
    except Exception as e:
        print("Error occured at get_project_details : ",e)