import time

import requests, json, sys

Github_PAT = sys.argv[1] #{sys.argv[1]}
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

TerraformDestroyPlan = """

Terraform will perform the following actions:

  # module.rg.azurerm_resource_group.rg will be destroyed
  - resource "azurerm_resource_group" "rg" {
      - id         = "/subscriptions/e86d46ed-ce74-4b9f-a823-5e715aaaaf44/resourceGroups/trraformpoc3" -> null
      - location   = "eastasia" -> null
      - name       = "trraformpoc3" -> null
      - tags       = {} -> null
        # (1 unchanged attribute hidden)
    }

  # module.rg.azurerm_service_plan.example will be destroyed
  - resource "azurerm_service_plan" "example" {
      - id                           = "/subscriptions/e86d46ed-ce74-4b9f-a823-5e715aaaaf44/resourceGroups/trraformpoc3/providers/Microsoft.Web/serverFarms/traamio09sd8nsknmvvnn5" -> null
      - kind                         = "app" -> null
      - location                     = "eastasia" -> null
      - maximum_elastic_worker_count = 1 -> null
      - name                         = "traamio09sd8nsknmvvnn5" -> null
      - os_type                      = "Windows" -> null
      - per_site_scaling_enabled     = false -> null
      - reserved                     = false -> null
      - resource_group_name          = "trraformpoc3" -> null
      - sku_name                     = "S1" -> null
      - tags                         = {} -> null
      - worker_count                 = 1 -> null
      - zone_balancing_enabled       = false -> null
        # (1 unchanged attribute hidden)
    }

Plan: 0 to add, 0 to change, 2 to destroy.

Changes to Outputs:
  - appid = "/subscriptions/e86d46ed-ce74-4b9f-a823-5e715aaaaf44/resourceGroups/trraformpoc3/providers/Microsoft.Web/serverFarms/traamio09sd8nsknmvvnn5" -> null


"""

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
        #print(f"Waiting For Approval -- Check With {assignees}")
        continue
    elif len(GetIssue.json()) >=1:
        objs = len(GetIssue.json())
        #print(f"Waiting For Approval -- Check With {assignees}")
        #print(f"Issue Comment -- {GetIssue.json()[objs-1]['body']}")
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
    time.sleep(2)

print(TerraformApplyContinue)
