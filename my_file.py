import requests, json, sys, time, os


def IssueDescription(plan,url):
    approvalbody = '''
    -----
    ##Terraform Approval and Cancel Instructions
    **Valid Approve Comments are _"Approved"_, _"Approve"_, _"approved"_, _"approve"_ to Continue the Terraform Destroy Apply**
    **Valid Dis-Approve or Cancel Comments are _"Denied"_, _"Deny"_, _"denied"_, _"deny"_ to Cancel the Terraform Destroy Apply**
    '''
    Github_RUN_Url = f"Github Run Url -- {url}"

    IssueDescription = f"{plan}-{approvalbody}-{Github_RUN_Url}"
    return IssueDescription





Github_PAT = sys.argv[1] #{sys.argv[1]}
owner = "BrazilAmazon"
repo = "terraform_poc"
assignees = {"Abdulk777"}
temp_assignees = ["Abdulk777"]
def headers(token):
    headers = {
        "accept" : "application/vnd.github+json",
        "Authorization" : f"Bearer {token}",
        "X-GitHub-Api-Version" : "2022-11-28",
    }
    return headers

Description = IssueDescription(plan=sys.argv[2],url=sys.argv[3])
def CreateIssue():

    CreateIssueForApproval = f"https://api.github.com/repos/{owner}/{repo}/issues"
    body = {"title":f"Terraform Approval Run ID:{sys.argv[4]}","body":f"{Description}.","assignees":["Abdulk777"],"labels":["Terraform Approval"]}
    CreateIssue = requests.post(CreateIssueForApproval,headers=headers(token=Github_PAT), data=json.dumps(body))

    return CreateIssue

IssueNumner = CreateIssue()

def UpdateIssue():

    UpdateIssueState = f"https://api.github.com/repos/{owner}/{repo}/issues/{IssueNumner.json()['number']}"
    body = {"title":f"Terraform Approval Run ID:{sys.argv[4]}","body":f"{Description}.","assignees":["Abdulk777"], "state":"closed" ,"labels":["Terraform Approval"]}
    UpdateIssue_State = requests.patch(UpdateIssueState,headers=headers(token=Github_PAT), data=json.dumps(body))

    return UpdateIssue_State


TerraformApplyContinue = 0
Approvers_list = set()
while 1:
    GetIssueForApproval = f"https://api.github.com/repos/{owner}/{repo}/issues/{IssueNumner.json()['number']}/comments"
    GetIssue = requests.get(GetIssueForApproval,headers=headers(token=Github_PAT))
    #print(GetIssue.json())
    if len(GetIssue.json()) <=0:
        print(f"Waiting For Approval -- Check With {temp_assignees}", flush=True)
    elif len(GetIssue.json()) >=1:
        objs = len(GetIssue.json())
        print(f"Waiting For Approval -- Check With {temp_assignees}", flush=True)
        commentbody = GetIssue.json()[objs-1]['body']
        user = GetIssue.json()[objs-1]['user']['login']
        if str(commentbody).lower() == "approved" or str(commentbody).lower() == "approve" and user in assignees:
            TerraformApplyContinue = 1
            Approvers_list.add(user)
            print(f"Issue Comment -- {GetIssue.json()[objs-1]['body']}--{Approvers_list}", flush=True)
            try:
              temp_assignees.remove(f"{user}")
            except:
                pass
            if assignees == Approvers_list:
                if IssueNumner.json()['state'] == "open":
                    UpdateIssue()
                break
        elif str(commentbody).lower() == "denied" or str(commentbody).lower() == "deny" and user in assignees:
            TerraformApplyContinue = 2
            if IssueNumner.json()['state'] == "open":
                UpdateIssue()
            break
    time.sleep(3)

name = 'TerraformApplyContinue'
value = TerraformApplyContinue
with open(os.environ['GITHUB_OUTPUT'], 'a') as TAC:
    print(f'{name}={value}', file=TAC)


