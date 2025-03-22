from atlassian import Jira
import pandas as pd

#project = "TSP"
project = "CE1009054"

jira = Jira(
    url='',
    username='',
    password='',
    cloud=True)
issue_cols = ['key','created','issuetype','status','priority']
jql_request = f'project = {project}'
JQL_response = jira.jql(jql_request,
                  fields = issue_cols[1:],
                  limit=500)


JQL_response = jira.jql(jql_request,
                  limit=500)

issues = {}
for issue in JQL_response["issues"]:
    issueTypeName = issue["fields"]['issuetype']["name"]
    if issueTypeName not in issues.keys():
        issues[issueTypeName] = []
    issues[issueTypeName].append(issue)
    

#issues = issues
#issueType = 'Story'

def get_isssue_status_count(issues, issueType):
    d={}

    for issue in issues[issueType]:
        k = issue['fields']['status']['name']
        if k not in d:  
            d[k] = 0
        d[k] += 1

    return d

def get_issues_status_priority_count(issues, issueType):
    result = {}
    for isssue in issues[issueType]:
        status = isssue['fields']['status']['name']
    
        priority = issue['fields']['priority']['name']
    
        if status not in result:
            result[status] = {}
            
        if priority not in result[status]:
            result[status][priority] = 0
            
        result[status][priority] += 1
      

    return result











'''
issues['Story'][0]['fields']['priority']['name']="Low"
issues['Story'][10]['fields']['priority']['name']="High"
issues['Story'][6]['fields']['priority']['name']="Low"
issues['Story'][15]['fields']['priority']['name']="Low"
issues['Story'][2]['fields']['priority']['name']="High"

for issue in issues['Story']:
    print("Status:",issue['fields']['status']['name'], "Priority:",issue['fields']['priority']['name'] )



status_counts = {}

for issue in JQL_response["issues"]:
    status = issue['fields']['status']['name']
    
    #print(status)
    if status not in status_counts:
        status_counts[status] = 0
    status_counts[status] += 1

    #print(status_counts)

for status, count in status_counts.items():
    print(f'{status}: {count}')


issue_df =  pd.DataFrame(columns= issue_cols)
for issue in issues['issues']:
    issue_list = [issue['key'],issue['fields']['created'],issue['fields']['issuetype']['name'],issue['fields']['status']["name"],issue['fields']['priority']["name"]]
    dict_from_list = {k:v for k,v in zip(issue_cols,issue_list)}
    df_for_list = pd.DataFrame(dict_from_list,index=[0])
    issue_df = pd.concat([issue_df,df_for_list],ignore_index=True)

issue_dict = [{'value': v, 'name': k} for k, v in issue_df['issuetype'].value_counts().to_dict().items()]
print(issue_dict)
'''


# issue_type = list(set(issue_df['issuetype']))

# issue_dict = {}
# status_dict = {}
# print(issue_type)
# for issue in issue_type:
#     issue_dict[issue] = issue_df.loc[issue_df['issuetype'] == issue]
#     print("Dataframe")
#     print(issue_dict[issue]['status'].value_counts().to_dict())
#     status_dict[issue] = [{'value': v, 'name': k} for k, v in issue_dict[issue]['status'].value_counts().to_dict().items()]

# print("Defect_pieChart project_df : ",issue_df)

