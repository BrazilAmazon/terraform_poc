import requests, json, sys, time, os

Github_PAT = sys.argv[1]  #{sys.argv[1]}
owner = "BrazilAmazon"
repo = "terraform_poc"
assignees = ["Abdulk777"]

def headers(token):
    headers = {
        "accept" : "application/vnd.github+json",
        "Authorization" : f"Bearer {token}",
        "X-GitHub-Api-Version" : "2022-11-28",
    }
    return headers

TerraformDestroyPlan = sys.argv[2]
def CreateIssue():

    CreateIssueForApproval = f"https://api.github.com/repos/{owner}/{repo}/issues"
    body = {"title":"Found a bug","body":f"{TerraformDestroyPlan}.","assignees":["Abdulk777"],"labels":["Terraform Approval"]}
    CreateIssue = requests.post(CreateIssueForApproval,headers=headers(token=Github_PAT), data=json.dumps(body))

    return CreateIssue

IssueNumner = CreateIssue()

def UpdateIssue():

    UpdateIssueState = f"https://api.github.com/repos/{owner}/{repo}/issues/{IssueNumner.json()['number']}"
    body = {"title":"Found a bug","body":f"{TerraformDestroyPlan}.","assignees":["Abdulk777"], "state":"closed" ,"labels":["Terraform Approval"]}
    UpdateIssue_State = requests.patch(UpdateIssueState,headers=headers(token=Github_PAT), data=json.dumps(body))

    return UpdateIssue_State


TerraformApplyContinue = 0

while 1:
    GetIssueForApproval = f"https://api.github.com/repos/{owner}/{repo}/issues/{IssueNumner.json()['number']}/comments"
    GetIssue = requests.get(GetIssueForApproval,headers=headers(token=Github_PAT))
    #print(GetIssue.json())
    if len(GetIssue.json()) <=0:
        print(f"Waiting For Approval -- Check With {assignees}", flush=True)
    elif len(GetIssue.json()) >=1:
        objs = len(GetIssue.json())
        print(f"Waiting For Approval -- Check With {assignees}", flush=True)
        print(f"Issue Comment -- {GetIssue.json()[objs-1]['body']}", flush=True)
        commentbody = GetIssue.json()[objs-1]['body']
        if str(commentbody).lower() == "approved" or str(commentbody).lower() == "approve":
            TerraformApplyContinue = 1
            if IssueNumner.json()['state'] == "open":
                UpdateIssue()
            break
        elif str(commentbody).lower() == "denied" or str(commentbody).lower() == "deny":
            TerraformApplyContinue = 2
            if IssueNumner.json()['state'] == "open":
                UpdateIssue()
            break
    time.sleep(5)

name = 'TerraformApplyContinue'
value = TerraformApplyContinue
with open(os.environ['GITHUB_OUTPUT'], 'a') as TAC:
    print(f'{name}={value}', file=TAC)

