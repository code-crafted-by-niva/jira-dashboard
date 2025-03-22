from flask import Flask, render_template, redirect, url_for, request, Blueprint
import db
import commons
from flask_login import login_required

dashboard_blueprint = Blueprint('dashboard_blueprint', __name__)


@dashboard_blueprint.route('/dashboard',methods=['GET'])
@login_required
def dashboard_home():
    page = {"title"   : "Dashboard",
            "icon"    : "fas fa-fw fa-chart-area",
            "heading" : "JIRA Dashboard",
            "desc"    : "Create your own JIRA Dashboard"}
    return render_template('/pages/dashboard.html',page=page)




@dashboard_blueprint.route('/dashboard/dailystatus',methods=['GET','POST'])
def dashboard_dailystatus():
    #mock
    page = {"title"   : "Daily Status Dashboard",
            "icon"    : "fas fa-fw fa-chart-area",
            "heading" : "Daily Status Dashboard",
            "desc"    : "Provides Daily Status Report Analysis on Task, Defects & Execution"}
    email = "priyadharshinivi@maveric-systems.com"
    project = 'TSP'
    issues = ""
    #code to check jira 
    jiraDetails = db.get_jira_details(email)
    user_projects = commons.get_JIRA_Projects(jiraDetails)
    
    if request.method == 'GET':
        query = ""
        project = ""
        jira_request = ""
        return render_template('dashboards/dailyStatus.html',
                           page = page,
                           user_projects = user_projects,
                           jiraDetails=jiraDetails)
        
    if request.method == 'POST':
        project = request.form.get('project')
        query = request.form.get('query')
        maxResults = request.form.get('maxResults')
        print("form details ",project,query,maxResults)
        jira = commons.jira_login(jiraDetails)
        jira_request = commons.generate_JQL(project,query)
        #JQL
        JQL_response = jira.jql(jira_request,
                                limit=maxResults)
        print("jira_request",jira_request)
        issues = {}
        for issue in JQL_response["issues"]:
            issueTypeName = issue["fields"]['issuetype']["name"]
            if issueTypeName not in issues.keys():
                issues[issueTypeName] = []
            issues[issueTypeName].append(issue)
    return render_template('dashboards/dailyStatus.html',
                           page = page,
                           user_projects = user_projects,
                           jiraDetails=jiraDetails,
                           jira_request = jira_request,
                           total_issues = len(JQL_response['issues']),
                           issues = issues,
                           projectDetails = commons.get_project_details(jira, project) )






'''
@dashboard_blueprint.route('/dashboard/dailystatus',methods=['GET','POST'])
def dashboard_dailystatus():
    #mock
    page = {"title"   : "Daily Status Dashboard",
            "icon"    : "fas fa-fw fa-chart-area",
            "heading" : "Dialy Status Dashboard",
            "desc"    : "Provides Daily Status Report Analysis on Task, Defects & Execution"}
    email = "priyadharshinivi@maveric-systems.com"
    project = 'TSP'
    #code to check jira 
    jiraDetails = db.get_jiraDetails(email)
    user_projects = commons.get_JIRA_Projects(jiraDetails)
    
    if request.method == 'GET':
        query = ""
        project = 'TSP'
    if request.method == 'POST':
        project = request.form['project']
        query = request.form['query']
    return render_template('dashboards/dailyStatus.html',
                           page = page,
                           user_projects = user_projects,
                           jiraDetails=jiraDetails,
                           query = query)
'''
