from atlassian import Jira
from datetime import datetime
import pandas as pd
from collections import Counter


def get_issue_length(issues):
    issues_types = issues.keys()
    data = []
    for itype in issues_types:
        data.append({'value' : len(issues[itype]),
                     'name'  : itype})
    return data
    

def get_issues_trends(issues):
    data = []
    for key in issues:
        date_dict = Counter([issue['fields']['created'].split('T')[0] for issue in issues[key]])
        data.append({"name":key,
                     "type": "line",
                     "color" : get_colour(key),
                     "data":[[key, value] for key,value in date_dict.items()]})
    return data

def get_issue_status_count(issues):
    data = Counter([issue['fields']['status']['name'] for issue in issues])
    data = [{'value': v, 'name': k} for k,v in data.items()]
    return data

def get_colour(issueType):
    issueType = issueType.lower()
    colour = {
    'task'   : 'blue',
    'defect' : 'orange',
    'story'  : 'green',
    'epic'   : 'red'}
    if issueType in colour:
        return colour[issueType]
    else:
        return ""

