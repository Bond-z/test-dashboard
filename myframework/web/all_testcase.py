import xml.etree.ElementTree as ET
import datetime
import time
import pandas
import os
from dotenv import load_dotenv
import glob
import requests
import re
import yaml



input_text = """

---

-
    Testcase ID: SCC-AZURE-ACCOUNT-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: GET
    Use case: Get all Azure accounts
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: "{{baseUrl}}/account?cloud-provider=azure"
    Body: N/A
    Response: All accounts for Azure
    Result:
    Remark: Run this after you create these test accounts
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-ACCOUNT-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: GET
    Use case: Get Azure account(s) matching with prefix
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=azure&prefix=dela
    Body: N/A
    Response: Get list of Azure accounts matched with prefix
    Result:
    Remark: Run this after you create these test accounts
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-ACCOUNT-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: GET
    Use case: Get a single Azure account matching with prefix
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=azure&prefix=delabsc01
    Body: N/A
    Response: Get exact Azure account in response
    Result:
    Remark: Run this after you create these test accounts
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-ACCOUNT-4
    Postman: Y
    Servicenow: Y
    Customer UI: Y
    Automation: Y
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: POST
    Use case: Account Creation with testing validations first (identical owners)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=azure
    Body: |
        {
          "account-data": {
            "project-name": "Cloud Accounts",
            "account-owners": [
              "mirza.grbic@allianz.de",
              "mirza.grbic@allianz.de"
            ],
            "customer-environment": "test",
            "account-tag": "delabsc01",
            "cloud-region": "germanywestcentral",
            "crp-aks-cluster": false
          }
        }
    Response: |
          {
            "code": 400,
            "message": "Errors: Owners must be unique, Account already exists."
          }
    Result:
    Remark: If the scenario works then for other account types and services it should as well (we can skip such tests)
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-ACCOUNT-5
    Postman: Y
    Servicenow: Y
    Customer UI: Y
    Automation: Y
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: POST
    Use case: Account Creation with testing validations first (only one use provided)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=azure
    Body: |
        {
          "account-data": {
            "project-name": "Cloud Accounts",
            "account-owners": [
              "mirza.grbic@allianz.de"
            ],
            "customer-environment": "test",
            "account-tag": "delabsc01",
            "cloud-region": "germanywestcentral",
            "crp-aks-cluster": false
          }
        }
    Response: |
          {
            "code": 500,
            "message": [
              {
                "message": "['mirza.grbic@allianz.de'] is too short",
                "schema": {
                  "title": "Account Owners",
                  "$schema": "http://json-schema.org/draft-04/schema#",
                  "description": "Type of the cloud account",
                  "type": "array",
                  "items": {
                    "type": "string",
                    "format": "email",
                    "pattern": "^[a-zA-Z0-9]+[a-zA-Z0-9_.-]+[a-zA-Z0-9]@[a-zA-Z0-9]+[a-zA-Z0-9-]+(.[a-zA-Z0-9][a-zA-Z0-9-]+){1,}$"
                  },
                  "min-items": 2,
                  "max-items": 2,
                  "$id": "AccountOwners"
                },
                "instance": [
                  "mirza.grbic@allianz.de"
                ]
              }
            ]
          }
    Result:
    Remark: "There is only "germanywestcentral" region in Staging (Azure test tenant).Test with this region in both Staging and Prod."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-ACCOUNT-6
    Postman: Y
    Servicenow: Y
    Customer UI: Y
    Automation: Y
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: POST
    Use case: Account Creation with non-existing project in vRA
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=azure
    Body: |
          {
            "account-data": {
              "project-name": "ABCD",
              "customer-environment": "test",
              "account-tag": "delabsc01",
              "account-owners": [
                "kiro.mihajlovski@allianz.de",
                "mirza.grbic@allianz.de"
              ],
              "cloud-region": "germanywestcentral",
              "crp-aks-cluster": false
            }
          }
    Response: |
          {
            "code": 404,
            "message": "There is no such project(ABCD)."
          }
    Result:
    Remark: "There is only "germanywestcentral" region in Staging (Azure test tenant).Test with this region in both Staging and Prod."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-ACCOUNT-7
    Postman: Y
    Servicenow: Y
    Customer UI: Y
    Automation: Y
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: POST
    Use case: Account Creation with CRP AKS cluster
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=azure
    Body: |
        {
          "account-data": {
            "project-name": "Cloud Accounts",
            "customer-environment": "test",
            "account-tag": "delabsc01",
            "account-owners": [
              "kiro.mihajlovski@allianz.de",
              "mirza.grbic@allianz.de"
            ],
            "cloud-region": "germanywestcentral",
            "crp-aks-cluster": true
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: "There is only "germanywestcentral" region in Staging (Azure test tenant).Test with this region in both Staging and Prod."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-ACCOUNT-8
    Postman: Y
    Servicenow: Y
    Customer UI: Y
    Automation: Y
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: POST
    Use case: Account Creation with existing values
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=azure
    Body: |
      {
        "account-data": {
          "project-name": "Cloud Accounts",
          "customer-environment": "test",
          "account-tag": "delabsc01",
          "account-owners": [
            "kiro.mihajlovski@allianz.de",
            "mirza.grbic@allianz.de"
          ],
          "cloud-region": "germanywestcentral",
          "crp-aks-cluster": false
        }
      }
    Response: |
      {
        "code": 400,
        "message": "Errors: Account already exists."
      }
    Result:
    Remark: "Reuse any payload you've tested.There is only "germanywestcentral" region in Staging (Azure test tenant).Test with this region in both Staging and Prod."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-ACCOUNT-9
    Postman: Y
    Servicenow: Y
    Customer UI: Y
    Automation: Y
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: POST
    Use case: Account Creation with project longer than 50 chars and without CRP AKS
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=azure
    Body: |
        {
          "account-data": {
            "project-name": "A.TEC_GLOB_Smart Cloud Connected Project: SCC API Test",
            "customer-environment": "test",
            "account-tag": "delabsc02",
            "account-owners": [
              "kiro.mihajlovski@allianz.de",
              "mirza.grbic@allianz.de"
            ],
            "cloud-region": "germanywestcentral",
            "crp-aks-cluster": false
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: "There is only "germanywestcentral" region in Staging (Azure test tenant).Test with this region in both Staging and Prod."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-ACCOUNT-10
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: POST
    Use case: Account Creation without sending any notificaiton on Success
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=azure
    Body: |
        {
          "account-data": {
            "project-name": "Cloud Accounts",
            "customer-environment": "test",
            "account-tag": "delabsc03",
            "account-owners": [
              "kiro.mihajlovski@allianz.de",
              "mirza.grbic@allianz.de"
            ],
            "cloud-region": "germanywestcentral",
            "crp-aks-cluster": false
          },
          "config": {
            "send-mails": false
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: "No notification email is sent.There is only "germanywestcentral" region in Staging (Azure test tenant).Test with this region in both Staging and Prod."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-ACCOUNT-11
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: POST
    Use case: "Account Creation without sending any notificaiton on SuccessGlobal CONFIG_FLAG_SEND_EMAIL flag"
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=azure
    Body: |
        {
          "account-data": {
            "project-name": "Cloud Accounts",
            "customer-environment": "test",
            "account-tag": "delabsc04",
            "account-owners": [
              "kiro.mihajlovski@allianz.de",
              "mirza.grbic@allianz.de"
            ],
            "cloud-region": "germanywestcentral",
            "crp-aks-cluster": false
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "No notification email is sent when CONFIG_FLAG_SEND_EMAIL flag in AppConfig is set to False (default).
      This global flag ignores send-emails flag in account creation payload (see above).
      There is only "germanywestcentral" region in Staging (Azure test tenant).Test with this region in both Staging and Prod."
    JIRA: https://jmp.allianz.net/browse/AWSS-11113
    GHE: https://github.developer.allianz.io/CloudTribe/scc-api/pull/847
-
    Testcase ID: SCC-AZURE-ACCOUNT-12
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: ACCOUNT
    Method: GET
    Use case: Verify search should not be found if the account is not exiting
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=azure&prefix=delaabc001
    Body: N/A
    Response:
      {
        "account-id": []
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-ACCOUNT-13
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: ACCOUNT
    Method: GET
    Use case: Get AZURE accounts Name
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=azure&prefix=delaabc001
    Body: N/A
    Response:
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-ACCOUNT-14
    Postman: Y
    Servicenow: Y
    Customer UI: Y
    Automation: Y
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: POST
    Use case: "Account Creation with CIDR sizes + CRP AKS Cluster. This corresponds with Customer UI / SNOW forms (Advanced = No)."
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=azure
    Body: |
        {
          "account-data": {
            "project-name": "Cloud Accounts",
            "customer-environment": "test",
            "account-tag": "delascc01",
            "account-owners": [
              "kiro.mihajlovski@allianz.de",
              "mirza.grbic@allianz.de"
            ],
            "cloud-region": "germanywestcentral",
            "crp-aks-cluster": true
          },
          "cloud-network": {
            "cloud-network-name": "delascc01",
            "public-subnet": {
              "naming-pattern": "public",
              "sizes": [
                28
              ]
            },
            "private-subnet": {
              "naming-pattern": "private",
              "sizes": [
                28
              ]
            },
            "routable-subnet": {
              "naming-pattern": "routable",
              "sizes": [
                28
              ]
            }
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "There is only "germanywestcentral" region in Staging (Azure test tenant).
      Test with this region in both Staging and Prod.
      Verify in VRA console that all subnets are discovered and have the following tags:
      account_name, vnet, subnet_type, resource_groupTags are applied in step in vRA state machine during integration.
      Azure does NOT support tags on subnet level."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-ACCOUNT-15
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: POST
    Use case: Account Creation with sending notification on Failure
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=azure
    Body: |
        {
          "account-data": {
            "project-name": "Cloud Accounts",
            "customer-environment": "test",
            "account-tag": "delabsc04",
            "account-owners": [
              "kiro.mihajlovski@allianz.de",
              "mirza.grbic@allianz.de"
            ],
            "cloud-region": "germanywestcentral",
            "crp-aks-cluster": false
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "This requires to manually change PIPELINE_RUN_ACCOUNT_CREATION step to FAILED status in StateTable.
      Think of how to change this for full automation.
      For internal use and configure in Postman only, customer always receive emails notification either failure or successful"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-ACCOUNT-DELETE-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: DELETE
    Use case: SCC Basic account deletion (no restore)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=azure&account-id=<delabsc01>
    Body: |
        {
          "dry-run": false
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "Checkt in Azure console the resources are deleted and subscription is in deleted_accounts mgmt group.
      Run this for every account creation use case.
      By this we will keep our environments clean."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-ACCOUNT-DELETE-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: DELETE
    Use case: SCC Account connected deletion (no restore)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=azure&account-id=<delascc01>
    Body: |
        {
          "dry-run": false
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "Checkt in Azure console the resources are deleted and subscription is in deleted_accounts mgmt group.
      Check allocated CIDRs are removed from CIDRAllocated table.Check that branch + folder in master branch are deteled in
      https://github.developer.allianz.io/CloudTribe/azure-customer-terraform-paramsRun this for every account creation use case.
      By this we will keep our environments clean."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-ACCOUNT-DELETE-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: DELETE
    Use case: Basic Account deletion DRY-RUN mode
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=azure&account-id=<delabsc01>
    Body: |
        {
          "dry-run": true
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "This mode just shows things that will be deleted when dry-run = True
      I would expect here the output of steps and what will be deleted.
      I did not find anything /status endpoint for this activity.
      It does not trigger "delete" state machine either (correct), but we have not info.
      So, at this moment, it seems to be completely useless."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-ACCOUNT-DELETE-4
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: DELETE
    Use case: Connected Account deletion DRY-RUN mode
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=azure&account-id=<delascc01>
    Body: |
        {
          "dry-run": true
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "This mode just shows things that will be deleted when dry-run = True
      I would expect here the output of steps and what will be deleted.
      I did not find anything /status endpoint for this activity.
      It does not trigger "delete" state machine either (correct), but we have not info.
      So, at this moment, it seems to be completely useless."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-NETWORK-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: NETWORK
    Method: GET
    Use case: 'Get account''s network details'
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/network?cloud-provider=azure&account-id=<delascc01>
    Body: N/A
    Response: |
            {
              "account-id": "<delascc01>",
              "cloud-networks": [
                {
                  "cloud-network-name": "vnet-t-gwc1-01",
                  "number-availability-zones": 2,
                  "routable-subnets": [],
                  "private-subnets": [],
                  "public-subnets": [
                    {
                      "naming-pattern": "sub-t-gwc1-pubint-44.138.93.144-28",
                      "sizes": "44.138.93.144/28"
                    }
                  ]
                }
              ]
            }
    Result:
    Remark: GET Azure network status endpoint is obsoleted
    JIRA: https://jmp.allianz.net/browse/FCP-17789
    GHE:
-

    Testcase ID: SCC-AZURE-NETWORK-2
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: Y
    Cloud Privder: Azure
    Endpoint: NETWORK
    Method: POST
    Use case: Add additional subnet to the existing account with existing cloud-network-name.
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/network?cloud-provider=azure&subscription-id=<delascc01>
    Body: |
        {
          "cloud-network": {
            "cloud-network-name": "delascc01",
            "private-subnet": {
              "naming-pattern": "privint",
              "sizes": [
                28
              ]
            },
            "public-subnet": {
              "naming-pattern": "pubext",
              "sizes": [
                28
              ]
            },
            "routable-subnet": {
              "naming-pattern": "pubint",
              "sizes": [
                28
              ]
            }
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "This must fail on cloud-network-name (Private DNS zone)
      validation!Allowing to trigger Jenkins pipeline will result in failure in terraform:Error:
      Virtual Network Link Name: "sharedservices_dns_link"): polling after CreateOrUpdate: Code="BadRequest"
      Message="A virtual network cannot be linked to multiple zones with overlapping namespaces.
      You tried to link virtual network with 'delascc01.gwc1-t.azure.aztec.cloud.allianz' and 'delascc01.gwc1-t.azure.aztec.cloud.allianz' zones.""
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-NETWORK-3
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: Y
    Cloud Privder: Azure
    Endpoint: NETWORK
    Method: POST
    Use case: Create SCC AZURE additional network should be successful
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/network?cloud-provider=azure&subscription-id=<delascc01>
    Body: |
        {
          "cloud-network": {
            "cloud-network-name": "delascc01a",
            "cloud-region": "germanywestcentral",
            "customer-environment": "test",
            "private-subnet": {
              "naming-pattern": "privint",
              "sizes": [
                28
              ]
            },
            "public-subnet": {
              "naming-pattern": "pubext",
              "sizes": [
                28
              ]
            },
            "routable-subnet": {
              "naming-pattern": "pubint",
              "sizes": [
                28
              ]
            }
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "Verify resource creation in one of these:
      - Jenkins pipeline (success)
      - ideal /status endpoint and PIPELINE_RUN_NETWORK_EXTENSION_CREATION (SUCCESSFUL)
      - Azure portal (console)Verify CIDR allocation records in CIDRAllocated table{{baseUrl}}/cidr/allocation?account-name=delascc01-germanywestcentral-test
      Verify vRA state machine was triggered and applied tag in networks: account_name, vnet, subnet_type, resource_groupTags are applied in step in vRA state machine during integration.
      Azure does NOT support tags on subnet level.
      status endpoint and STEP_FUNCTIONS_RUN_VRA_WORKFLOW (SUCCESSFUL)
      The account-tag should be delascc011 or delascc0111 (depends on if previous case was run).
      The resource groups should have delascc011/delascc0111 in name.
      No peering is created with sharedservices-gwc1-s (hub) in Staging.
      No peering lock is created in Staging.Peering and lock is created with sharedservices-gwc1-p (hub) in Production.No need to test BYOC again here if you already created SCC Connected with BYOC."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-NETWORK-4
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: Y
    Cloud Privder: Azure
    Endpoint: NETWORK
    Method: POST
    Use case: Add additional subnet to the existing account with unique cloud-network-name
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/network?cloud-provider=azure&subscription-id=<delascc01>
    Body: |
        {
          "cloud-network": {
            "cloud-network-name": "delascc01b",
            "private-subnet": {
              "naming-pattern": "privint",
              "sizes": [
                28
              ]
            },
            "public-subnet": {
              "naming-pattern": "pubext",
              "sizes": [
                28
              ]
            },
            "routable-subnet": {
              "naming-pattern": "pubint",
              "cidr": "44.138.93.16/28",
              "number-of-subnets": 1
            }
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "Verify resource creation in one of these:
      - Jenkins pipeline (success)
      - ideal- /status endpoint and PIPELINE_RUN_NETWORK_EXTENSION_CREATION (SUCCESSFUL)
      - Azure portal (console)Verify CIDR allocation records in CIDRAllocated table{{baseUrl}}/cidr/allocation?account-name=delascc01-germanywestcentral-test
      Verify vRA state machine was triggered and applied tag in networks: account_name, vnet, subnet_type, resource_groupTags are applied in step in vRA state machine during integration.
      Azure does NOT support tags on subnet level./status endpoint and STEP_FUNCTIONS_RUN_VRA_WORKFLOW (SUCCESSFUL)The account-tag should be delascc0111 or delascc01111 (depends on if previous case was run).
      The resource groups should have delascc0111/delascc01111 in name.No peering is created with sharedservices-gwc1-s (hub) in Staging.No peering lock is created in Staging.
      Peering and lock is created with sharedservices-gwc1-p (hub) in Production.No need to test BYOC again here if you already created SCC Connected with BYOC."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-NETWORK-5
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: Y
    Cloud Privder: Azure
    Endpoint: NETWORK
    Method: POST
    Use case: Add additional subnet to the existing account with unique cloud-network-name (Different cloud-region)
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/network?cloud-provider=azure&subscription-id=<delascc01>
    Body: |
        {
          "cloud-network": {
            "cloud-network-name": "delascc01c",
            "cloud-region": "westeurope",
            "private-subnet": {
              "naming-pattern": "privint",
              "sizes": [
                28
              ]
            },
            "public-subnet": {
              "naming-pattern": "pubext",
              "sizes": [
                28
              ]
            },
            "routable-subnet": {
              "naming-pattern": "pubint",
              "sizes": [
                28
              ]
            }
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "Verify resource creation in one of these:
      - Jenkins pipeline (success)
      - ideal- /status endpoint and PIPELINE_RUN_NETWORK_EXTENSION_CREATION (SUCCESSFUL)
      - Azure portal (console)Verify CIDR allocation records in CIDRAllocated table{{baseUrl}}/cidr/allocation?account-name=delascc01-germanywestcentral-test
      Verify vRA state machine was triggered and applied tag in networks: account_name, vnet, subnet_type, resource_groupTags are applied in step in vRA state machine during integration.
      Azure does NOT support tags on subnet level. status endpoint and STEP_FUNCTIONS_RUN_VRA_WORKFLOW (SUCCESSFUL)
      No peering is created with sharedservices-gwc1-s (hub) in Staging.
      No peering lock is created in Staging.
      Peering and lock is created with sharedservices-gwc1-p (hub) in Production.
      This scenario is only valid in Production as we have only germanywestcentral region in Staging."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-NETWORK-6
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: Y
    Cloud Privder: Azure
    Endpoint: NETWORK
    Method: POST
    Use case: "Add additional subnet to the existing account with unique cloud-network-name (dnsname) .Different customer environment."
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/network?cloud-provider=azure&subscription-id=<delascc01>
    Body: |
        {
          "cloud-network": {
            "cloud-network-name": "delascc01d",
            "customer-environment": "dev",
            "private-subnet": {
              "naming-pattern": "privint",
              "sizes": [
                28
              ]
            },
            "public-subnet": {
              "naming-pattern": "pubext",
              "sizes": [
                28
              ]
            },
            "routable-subnet": {
              "naming-pattern": "pubint",
              "sizes": [
                28
              ]
            }
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "Verify resource creation in one of these:
      - Jenkins pipeline (success)
      - ideal- /status endpoint and PIPELINE_RUN_NETWORK_EXTENSION_CREATION (SUCCESSFUL)
      - Azure portal (console)Verify CIDR allocation records in CIDRAllocated table{{baseUrl}}/cidr/allocation?account-name=delascc01-germanywestcentral-test
      Verify vRA state machine was triggered and applied tag in networks: account_name, vnet, subnet_type, resource_groupTags are applied in step in vRA state machine during integration.
      Azure does NOT support tags on subnet level. status endpoint and STEP_FUNCTIONS_RUN_VRA_WORKFLOW (SUCCESSFUL)
      No peering is created with sharedservices-gwc1-s (hub) in Staging.No peering lock is created in Staging.Peering and lock is created with sharedservices-gwc1-p (hub) in Production."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-NETWORK-7
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: Y
    Cloud Privder: Azure
    Endpoint: NETWORK
    Method: POST
    Use case: "Add additional subnet to the existing account with unique cloud-network-name (dnsname). Different resource group."
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/network?cloud-provider=azure&subscription-id=<delascc01>
    Body: |
        {
          "cloud-network": {
            "cloud-network-name": "delascc01e",
            "cloud-region": "germanywestcentral",
            "customer-environment": "test",
            "resource-group": "delascc01e",
            "private-subnet": {
              "naming-pattern": "privint",
              "sizes": [
                28
              ]
            },
            "public-subnet": {
              "naming-pattern": "pubext",
              "sizes": [
                28
              ]
            },
            "routable-subnet": {
              "naming-pattern": "pubint",
              "sizes": [
                28
              ]
            }
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "Verify resource creation in one of these:
      - Jenkins pipeline (success)
      - ideal- /status endpoint and PIPELINE_RUN_NETWORK_EXTENSION_CREATION (SUCCESSFUL)
      - Azure portal (console)Verify CIDR allocation records in CIDRAllocated table{{baseUrl}}/cidr/allocation?account-name=delascc01-germanywestcentral-test
      Verify vRA state machine was triggered and applied tag in networks: account_name, vnet, subnet_type, resource_groupTags are applied in step in vRA state machine during integration.
      Azure does NOT support tags on subnet level. status endpoint and STEP_FUNCTIONS_RUN_VRA_WORKFLOW (SUCCESSFUL)
      No peering is created with sharedservices-gwc1-s (hub) in Staging.
      No peering lock is created in Staging.Peering and lock is created with sharedservices-gwc1-p (hub) in Production."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-NETWORK-8
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: NETWORK
    Method: GET
    Use case: Verify Network Was Deleted Successful
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: "{{baseUrl}}/network?cloud-provider=azure&account-id=<delascc01>"
    Body: N/A
    Response: |
      {
        "cloud-networks": []
      }
    Result:
    Remark: GET Azure network status endpoint is obsoleted
    JIRA: https://jmp.allianz.net/browse/FCP-17789
    GHE:
-
    Testcase ID: SCC-AZURE-NETWORK-9
    Postman: Y
    Servicenow: Y
    Customer UI: Y
    Automation: N
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: POST
    Use case: "Account Creation with BYOC + without CRP AKS ClusterThis corresponds with Customer UI / SNOW forms (Advanced = Yes)."
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=azure
    Body: |
        {
          "account-data": {
            "project-name": "Cloud Accounts",
            "customer-environment": "test",
            "account-tag": "delascc02",
            "account-owners": [
              "kiro.mihajlovski@allianz.de",
              "mirza.grbic@allianz.de"
            ],
            "cloud-region": "germanywestcentral",
            "crp-aks-cluster": false
          },
          "cloud-network": {
            "cloud-network-name": "delascc02",
            "public-subnet": {
              "naming-pattern": "public",
              "sizes": [
                28
              ]
            },
            "private-subnet": {
              "naming-pattern": "private",
              "sizes": [
                28
              ]
            },
            "routable-subnet": {
              "naming-pattern": "routable",
              "cidr": "44.138.93.0/28",
              "number-of-subnets": 1
            }
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "There is only "germanywestcentral" region in Staging (Azure test tenant).
      Test with this region in both Staging and Prod.
      Verify in VRA console that all subnets are discovered and have the following tags:
      account_name, vnet, subnet_type, resource_groupTags are applied in step in vRA state machine during integration.
      Azure does NOT support tags on subnet level."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-NETWORK-DELETION-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: NETWORK
    Method: DELETE
    Use case: Delete additional network in SCC account
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/network?cloud-provider=azure&subscription-id=<delascc01>
    Body: |
      {
        "dry-run": false,
        "region": "germanywestcentral",
        "virtual-network-name": "rgp-t-gwc1-<delascc01a>-networking",
        "request-id": "424bd0bef43b43238b6b499023ddf0a2"
      }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
       Check Network Deletion state machine finished successfully.
       Check in Azure portal that resources are deleted.
       Check mainly peering on hub / spoke side if everything is removed!
       Check that artefacts are removed from Terragrunt repo.
       Check allocated CIDRs are deleted in CIDRAllocated table.
       Run this for every network extension use case.
       By this we will keep our account clean.
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-NETWORK-DELETION-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: NETWORK
    Method: DELETE
    Use case: "Delete additional network in SCC account again"
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: "{{baseUrl}}/network?cloud-provider=azure&subscription-id=<delascc01>"
    Body: |
        {
          "dry-run": false,
          "region": "germanywestcentral",
          "virtual-network-name": "rgp-t-gwc1-<delascc01a>-networking",
          "request-id": "424bd0bef43b43238b6b499023ddf0a2"
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      We want to test repeated deletions are not an issue.
      If previous deletion was not successful, we can run again to remove leftovers.
      If previous deletion was successful, calling it again with the same data should NOT be an issue.
      Check Network Deletion state machine finished successfully.
      Check in Azure portal that resources are deleted.
      Check mainly peering on hub / spoke side if everything is removed!
      Double check that artefacts are removed from Terragrunt repo.
      Double check that CIDRs are deleted in CIDRAllocated table
      Run this for every network extension use case.
      By this we will keep our account clean.
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-ACCOUNT-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: GET
    Use case: Get all AWS accounts
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=aws
    Body: N/A
    Response: All accounts for AWS
    Result:
    Remark: Run this after you create these test accounts
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-ACCOUNT-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: GET
    Use case: Get AWS account(s) matching with prefix
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=aws&prefix=delw
    Body: N/A
    Response: Get list of AWS accounts matched with prefix
    Result:
    Remark: Run this after you create these test accounts
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-ACCOUNT-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: GET
    Use case: Get a single AWS account matching with prefix
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=aws&prefix=delwbsc01
    Body: N/A
    Response: Get exact AWS account in response
    Result:
    Remark: Run this after you create these test accounts
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-ACCOUNT-4
    Postman: Y
    Servicenow: Y
    Customer UI: Y
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: POST
    Use case: Account Creation with testing validations first (identical owners)
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=aws
    Body: |
        {
          "account-data": {
            "project-name": "Test Project Boon",
            "account-owners": [
              "kiro.mihajlovski@allianz.de",
              "kiro.mihajlovski@allianz.de"
            ],
            "customer-environment": "test",
            "account-tag": "delwbsc01",
            "cloud-region": "eu-central-1"
          }
        }
    Response: |
        {
          "code": 400,
          "message": "Errors: Owners must be unique"
        }
    Result:
    Remark: |
      "Align project name to be "Cloud Accounts".
      "Test Project Boon" is used in AWS because of special permissions to move to specific OUs."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-ACCOUNT-5
    Postman: Y
    Servicenow: Y
    Customer UI: Y
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: POST
    Use case: Account Creation with testing validations first (only one use provided)
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=aws
    Body: |
        {
          "account-data": {
            "project-name": "Test Project Boon",
            "account-owners": [
              "kiro.mihajlovski@allianz.de"
            ],
            "customer-environment": "test",
            "account-tag": "delwbsc01",
            "cloud-region": "eu-central-1"
          }
        }
    Response: |
        {
          "code": 500,
          "message": [
            {
              "message": "['kiro.mihajlovski@allianz.de'] is too short",
              "schema": {
                "title": "Account Owners",
                "$schema": "http: //json-schema.org/draft-04/schema#",
                "description": "Type of the cloud account",
                "type": "array",
                "items": {
                  "type": "string",
                  "format": "email",
                  "pattern": "^[a-zA-Z0-9]+[a-zA-Z0-9_.-]+[a-zA-Z0-9]@[a-zA-Z0-9]+[a-zA-Z0-9-]+(.[a-zA-Z0-9][a-zA-Z0-9-]+){1,}$"
                },
                "min-items": 2,
                "max-items": 2,
                "$id": "AccountOwners"
              },
              "instance": [
                "kiro.mihajlovski@allianz.de"
              ]
            }
          ]
        }
    Result:
    Remark: |
      "Align project name to be "Cloud Accounts".
      "Test Project Boon" is used in AWS because of special permissions to move to specific OUs."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-ACCOUNT-6
    Postman: Y
    Servicenow: Y
    Customer UI: Y
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: POST
    Use case: Account Creation with non-existing project
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=aws
    Body: |
        {
          "account-data": {
            "project-name": "ABCD",
            "account-owners": [
              "kiro.mihajlovski@allianz.de",
              "mirza.grbic@allianz.de"
            ],
            "customer-environment": "test",
            "account-tag": "delwbsc01",
            "cloud-region": "eu-central-1"
          }
        }
    Response: |
        {
          "code": 404,
          "message": "There is no such project(ABCD)."
        }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-ACCOUNT-7
    Postman: Y
    Servicenow: Y
    Customer UI: Y
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: POST
    Use case: Account Creation
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=aws
    Body: |
        {
          "account-data": {
            "project-name": "Test Project Boon",
            "account-owners": [
              "kiro.mihajlovski@allianz.de",
              "mirza.grbic@allianz.de"
            ],
            "customer-environment": "test",
            "account-tag": "delwbsc01",
            "cloud-region": "eu-central-1"
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      Align project name to be "Cloud Accounts.
      Test Project Boon" is used in AWS because of special permissions to move to specific OUs.
      Verify RootOrg for created account (calculated dynamically):
      - EuDev for accounts in Staging
      - EuProd for accounts in EU regions in Prod
      - UsProd for accounts in US regions in Prod
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-ACCOUNT-8
    Postman: Y
    Servicenow: Y
    Customer UI: Y
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: POST
    Use case: Account Creation with existing values
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=aws
    Body: |
        {
          "account-data": {
            "project-name": "Test Project Boon",
            "account-owners": [
              "kiro.mihajlovski@allianz.de",
              "mirza.grbic@allianz.de"
            ],
            "customer-environment": "test",
            "account-tag": "delwbsc01",
            "cloud-region": "eu-central-1"
          }
        }
    Response: |
        {
          "code": 400,
          "message": "Errors: Account already exists."
        }
    Result:
    Remark: |
      "Reuse any payload you've testedAlign project name to be "Cloud Accounts".
      "Test Project Boon" is Allianz Deutschland and is used in AWS because of special permissions to move to specific OUs."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-ACCOUNT-9
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: GET
    Use case: Verify search should not be found if the account is not exiting
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=aws&prefix=delwsccabc01
    Body: N/A
    Response:
      {
        "account-id": []
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-ACCOUNT-10
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: GET
    Use case: Get AWS accounts Name
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=aws&prefix=delwsccabc01
    Body: N/A
    Response:
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-ACCOUNT-11
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: POST
    Use case: Account creation should not be allowed if the length of account name is longer than 12 characters
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated (Subscription)
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=aws
    Body: |
        {
          "account-data": {
            "project-name": "Cloud Accounts",
            "owner-debtor-number": "2000010446",
            "snow-service-id": "string",
            "snow-order-id": "string",
            "account-owners": [
              "nathakrit.punyaworasin@allianz.com",
              "extern.gavenda_jindrich@allianz.de"
            ],
            "customer-environment": "stage",
            "account-type": "string",
            "is-customer": true,
            "account-tag": "invalid-name-awsscc1234",
            "cloud-region": "eu-central-1",
            "cloud-provider": "aws",
            "crp-aks-cluster": false
          }

        }
    Response: |
      {
        "message": "Validation error: [{'message': "'invalid-name-awsscc1234' is too long"
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-ACCOUNT-12
    Postman: Y
    Servicenow: Y
    Customer UI: Y
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: POST
    Use case: "Account Creation with CIDR sizes. This corresponds with Customer UI / SNOW forms (Advanced = No)."
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=aws
    Body: |
        {
          "account-data": {
            "project-name": "Test Project Boon",
            "account-owners": [
              "mirza.grbic@allianz.de",
              "kiro.mihajlovski@allianz.de"
            ],
            "customer-environment": "test",
            "account-tag": "delwscc01"
          },
          "cloud-network": {
            "cloud-network-name": "delwscc01",
            "cloud-region": "eu-central-1",
            "number-availability-zones": 2,
            "public-subnet": {
              "naming-pattern": "public",
              "sizes": [
                28,
                28
              ]
            },
            "private-subnet": {
              "naming-pattern": "private",
              "sizes": [
                28,
                28
              ]
            },
            "routable-subnet": {
              "naming-pattern": "routable",
              "sizes": [
                28,
                28
              ]
            }
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "It needs to be tested mainly from Customer UI and SNOW forms.
      If both tests are successful, we don't need to test explicitly from Postman as UI's will generate that payload and call SCC API anyway.
      Align project name to be "Cloud Accounts".
      "Test Project Boon" is Allianz Deutschland and is used in AWS because of special permissions to move to specific OUs.
      Verify in VRA console that all subnets are discovered and have the following tags: account_name, vnet, subnet_typeTags are applied in terraform directly in network creation Codebuild pipeline.
      AWS does support tags on subnet level."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-ACCOUNT-13
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: POST
    Use case: Account Creation without sending any notificaiton on Success
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=aws
    Body: |
        {
          "account-data": {
            "project-name": "Cloud Accounts",
            "account-owners": [
              "kiro.mihajlovski@allianz.de",
              "mirza.grbic@allianz.de"
            ],
            "customer-environment": "test",
            "account-tag": "delwbsc03",
            "cloud-region": "eu-central-1"
          },
          "config": {
            "send-mails": false
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "No notification email sent. Align project name to be "Cloud Accounts".
      "Test Project Boon" is Allianz Deutschland and is used in AWS because of special permissions to move to specific OUs.
      Verify RootOrg for created account (calculated dynamically):
      - EuDev for accounts in Staging
      - EuProd for accounts in EU regions in Prod
      - UsProd for accounts in US regions in Prod"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-ACCOUNT-14
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: POST
    Use case: "Account Creation without sending any notificaiton on SuccessGlobal CONFIG_FLAG_SEND_EMAIL flag"
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=aws
    Body: |
      {
        "account-data": {
          "project-name": "Test Project Boon",
          "account-owners": [
            "kiro.mihajlovski@allianz.de",
            "mirza.grbic@allianz.de"
          ],
          "customer-environment": "test",
          "account-tag": "delwbsc04",
          "cloud-region": "eu-central-1"
        }
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark: |
      "No notification email is sent when CONFIG_FLAG_SEND_EMAIL flag in AppConfig is set to False (default).
      This global flag ignores send-emails flag in account creation payload (see above).Align project name to be "Cloud Accounts".
      "Test Project Boon" is Allianz Deutschland and is used in AWS because of special permissions to move to specific OUs.
      Verify RootOrg for created account (calculated dynamically):
      - EuDev for accounts in Staging
      - EuProd for accounts in EU regions in Prod
      - UsProd for accounts in US regions in Prod"
    JIRA: https://jmp.allianz.net/browse/AWSS-11113
    GHE: https://github.developer.allianz.io/CloudTribe/scc-api/pull/847
-
    Testcase ID: SCC-AWS-ACCOUNT-15
    Postman: Y
    Servicenow: Y
    Customer UI: Y
    Automation: N
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: POST
    Use case: Account Creation with ITMP project to test adding account to policy
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=aws
    Body: |
        {
          "account-data": {
            "project-name": "Cloud Accounts",
            "account-owners": [
              "kiro.mihajlovski@allianz.de",
              "mirza.grbic@allianz.de"
            ],
            "customer-environment": "test",
            "account-tag": "delwbsc02",
            "cloud-region": "eu-central-1"
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "In the end, triggering account creation either from ServiceNow or customerUI it will call API account creation anyway so we can ignore test in Postman.
      Cloud Accounts project is ready to be used to test this implementation.
      https://github.developer.allianz.io/CloudTribe/scc-api/blob/staging/config/prod/account_setup.yml
      https://github.developer.allianz.io/CloudTribe/scc-api/blob/staging/config/staging/account_setup.yml
      Verify RootOrg for created account (calculated dynamically):
      - EuDev for accounts in Staging
      - EuProd for accounts in EU regions in Prod
      - UsProd for accounts in US regions in Prod
      Verify it_master_platform_technical_user in central IAM account has assigned technical_user_policy_X.
      Verify technical_user_policy_X has delwbsc02-t-<projecthas>-infraadmin-assumerole."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-ACCOUNT-DELETE-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: DELETE
    Use case: Account deletion (no restore)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=aws&account-id=<delwbsc01>
    Body: |
        {
          "dry-run": false
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "Checkt in AWS console the resources are deleted and accounts is in deleted_accounts OU.
      Run this for every account creation use case.
      By this we will keep our environments clean."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-ACCOUNT-DELETE-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: DELETE
    Use case: Account Connected deletion (no restore)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=aws&account-id=<delwscc01>
    Body: |
        {
          "dry-run": false
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "Checkt in AWS console the resources are deleted and accounts is in deleted_accounts OU.
      Check allocated CIDRs are deleted in CIDRAllocated table.
      Run this for every account creation use case.By this we will keep our environments clean."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-ACCOUNT-DELETE-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: DELETE
    Use case: Account deletion DRY-RUN mode
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=aws&account-id=<delwbsc01>
    Body: |
        {
          "dry-run": true
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "This mode just shows things that will be deleted when dry-run = True
      I would expect here the output of steps and what will be deleted.
      I did not find anything /status endpoint for this activity.
      It does not trigger "delete" state machine either (correct), but we have not info.So, at this moment, it seems to be completely useless."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-ACCOUNT-DELETE-4
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: DELETE
    Use case: Account deletion DRY-RUN mode
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/account?cloud-provider=aws&account-id=<delwscc01>
    Body: |
        {
          "dry-run": true
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "This mode just shows things that will be deleted when dry-run = True
      I would expect here the output of steps and what will be deleted.
      I did not find anything /status endpoint for this activity.
      It does not trigger "delete" state machine either (correct), but we have not info.
      So, at this moment, it seems to be completely useless."
    JIRA:
    GHE:
-
    Testcase ID:  SCC-AWS-NETWORK-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: GET
    Use case: 'Get account''s network details'
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/network?cloud-provider=aws&account-id=<delwscc01>
    Body: N/A
    Response: |
        {
          "account-id": "<delwscc01>",
          "cloud-networks": [
            {
              "cloud-network-name": "delq1ws_stage",
              "number-availability-zones": 2,
              "cloud-region": "eu-central-1",
              "routable-subnets": [],
              "private-subnets": [
                {
                  "naming-pattern": "subnet_test_project_boon_ec1_stage_delq1ws-private-subnet_2",
                  "sizes": "10.251.0.16/28"
                },
                {
                  "naming-pattern": "subnet_test_project_boon_ec1_stage_delq1ws-private-subnet_1",
                  "sizes": "10.251.0.0/28"
                },
                {
                  "naming-pattern": "subnet_test_project_boon_ec1_stage_delq1ws-pub-subnet_1",
                  "sizes": "10.251.0.32/28"
                },
                {
                  "naming-pattern": "subnet_test_project_boon_ec1_stage_delq1ws-pub-subnet_2",
                  "sizes": "10.251.0.48/28"
                },
                {
                  "naming-pattern": "subnet_test_project_boon_ec1_stage_delq1ws-routable-subnet_1",
                  "sizes": "10.17.0.32/28"
                },
                {
                  "naming-pattern": "subnet_test_project_boon_ec1_stage_delq1ws-routable-subnet_2",
                  "sizes": "10.17.0.48/28"
                }
              ],
              "public-subnets": []
            }
          ]
        }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-NETWORK-2
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: POST
    Use case: "Add additional subnet to the existing account.This should correspond with Customer UI / SNOW forms (Advanced = No).Existing cloud-network-name."
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/network?cloud-provider=aws&account-id=<delwscc01>
    Body: |
        {
          "cloud-network": {
            "cloud-network-name": "delwscc01",
            "cloud-region": "eu-central-1",
            "number-availability-zones": 2,
            "private-subnet": {
              "naming-pattern": "private_internal",
              "sizes": [
                28,
                28
              ]
            },
            "public-subnet": {
              "naming-pattern": "public_external",
              "sizes": [
                28,
                28
              ]
            },
            "routable-subnet": {
              "naming-pattern": "public_internal",
              "sizes": [
                28,
                28
              ]
            }
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "Verify resource creation in one of these:
      - Jenkins pipeline (success)
      - ideal- /status endpoint and PIPELINE_RUN_NETWORK_EXTENSION_CREATION (SUCCESSFUL)
      - Azure portal (console)Verify CIDR allocation records in CIDRAllocated table{{baseUrl}}/cidr/allocation?account-name=delwscc01-t-<projecthash>
      Verify vRA state machine was triggered and applied tag in networks:account_name, vnet, subnet_typeTags are applied in terraform directly in network creation Codebuild pipeline.
      AWS does support tags on subnet level./status endpoint and STEP_FUNCTIONS_RUN_VRA_WORKFLOW (SUCCESSFUL)"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-NETWORK-3
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: POST
    Use case: "Add additional subnet to the existing account.This should correspond with Customer UI / SNOW forms (Advanced = Yes).Unique cloud-network-name."
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/network?cloud-provider=aws&account-id=<delwscc01>
    Body: |
        {
          "cloud-network": {
            "cloud-network-name": "delwscc01a",
            "cloud-region": "eu-central-1",
            "number-availability-zones": 2,
            "private-subnet": {
              "naming-pattern": "private_internal",
              "sizes": [
                28,
                28
              ]
            },
            "public-subnet": {
              "naming-pattern": "public_external",
              "sizes": [
                28,
                28
              ]
            },
            "routable-subnet": {
              "naming-pattern": "public_internal",
              "sizes": [
                28,
                28
              ]
            }
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "Verify resource creation in one of these:
      - Jenkins pipeline (success)
      - ideal- /status endpoint and PIPELINE_RUN_NETWORK_EXTENSION_CREATION (SUCCESSFUL)
      - Azure portal (console)Verify CIDR allocation records in CIDRAllocated table{{baseUrl}}/cidr/allocation?account-name=delwscc01-t-<projecthash>
      Verify vRA state machine was triggered and applied tag in networks:account_name, vnet, subnet_typeTags are applied in terraform directly in network creation Codebuild pipeline.
      AWS does support tags on subnet level. status endpoint and STEP_FUNCTIONS_RUN_VRA_WORKFLOW (SUCCESSFUL)"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-NETWORK-4
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: POST
    Use case: "Add additional subnet to the existing account.This should correspond with Customer UI / SNOW forms (Advanced = Yes).Unique cloud-network-name.Bring Your Own CIDR (BYOC)"
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/network?cloud-provider=aws&account-id=<delwscc01>
    Body: |
        {
          "cloud-network": {
            "cloud-network-name": "delwscc01b",
            "cloud-region": "eu-central-1",
            "number-availability-zones": 2,
            "private-subnet": {
              "naming-pattern": "private_internal",
              "sizes": [
                28,
                28
              ]
            },
            "public-subnet": {
              "naming-pattern": "public_external",
              "sizes": [
                28,
                28
              ]
            },
            "routable-subnet": {
              "naming-pattern": "public_internal",
              "cidr": "10.0.10.0/28",
              "number-of-subnets": 2
            }
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "Verify resource creation in one of these:- Jenkins pipeline (success)
      - ideal- /status endpoint and PIPELINE_RUN_NETWORK_EXTENSION_CREATION (SUCCESSFUL)
      - Azure portal (console)Verify CIDR allocation records in CIDRAllocated table{{baseUrl}}/cidr/allocation?account-name=delwscc01-t-<projecthash>
      Verify vRA state machine was triggered and applied tag in networks:account_name, vnet, subnet_typeTags are applied in terraform directly in network creation Codebuild pipeline.
      AWS does support tags on subnet level. status endpoint and STEP_FUNCTIONS_RUN_VRA_WORKFLOW (SUCCESSFUL)
      No need to test BYOC again here if you already created SCC Connected with BYOC."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-NETWORK-5
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: POST
    Use case: "Add additional subnet to the existing account.This should correspond with Customer UI / SNOW forms (Advanced = No).Unique cloud-network-name.Different cloud-region"
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/network?cloud-provider=aws&account-id=<delwscc01>
    Body: |
        {
          "cloud-network": {
            "cloud-network-name": "delwscc01a",
            "cloud-region": "eu-west-3",
            "number-availability-zones": 2,
            "private-subnet": {
              "naming-pattern": "private_internal",
              "sizes": [
                28,
                28
              ]
            },
            "public-subnet": {
              "naming-pattern": "public_external",
              "sizes": [
                28,
                28
              ]
            },
            "routable-subnet": {
              "naming-pattern": "public_internal",
              "sizes": [
                28,
                28
              ]
            }
          }
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "Verify resource creation in one of these:
      - Jenkins pipeline (success)
      - ideal- /status endpoint and PIPELINE_RUN_NETWORK_EXTENSION_CREATION (SUCCESSFUL)
      - Azure portal (console)Verify CIDR allocation records in CIDRAllocated table{{baseUrl}}/cidr/allocation?account-name=delwscc01-t-<projecthash>
      Verify vRA state machine was triggered and applied tag in networks:account_name, vnet, subnet_typeTags are applied in terraform directly in network creation Codebuild pipeline.
      AWS does support tags on subnet level. status endpoint and STEP_FUNCTIONS_RUN_VRA_WORKFLOW (SUCCESSFUL)
      This scenario is only valid in Production as we have only eu-central-1 region in Staging."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-NETWORK-6
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: N
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: POST
    Use case: "Create SCC AWS account connected with BYOC"
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/network?cloud-provider=aws&account-id=<delwscc01>
    Body: |
            {
            "account-data": {
                "project-name": "Cloud Accounts",
                "account-owners": [
                "nathakrit.punyaworasin@allianz.com",
                "extern.gavenda_jindrich@allianz.de"
                ],
                "customer-environment": "stage",
                "account-tag": "delawscc121"
            },
            "cloud-network": {
                "cloud-network-name": "delawscc121",
                "cloud-region": "eu-central-1",
                "number-availability-zones": 2,
                "routable-subnet": {
                "naming-pattern": "public_internal",
                "cidr": "10.0.10.0/28",
                "number-of-subnets": 2
                    }
                }
            }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "Verify resource creation in one of these:- Jenkins pipeline (success)
      - ideal- /status endpoint and PIPELINE_RUN_NETWORK_EXTENSION_CREATION (SUCCESSFUL)
      - Azure portal (console)Verify CIDR allocation records in CIDRAllocated table{{baseUrl}}/cidr/allocation?account-name=delwscc01-t-<projecthash>
      Verify vRA state machine was triggered and applied tag in networks:account_name, vnet, subnet_typeTags are applied in terraform directly in network creation Codebuild pipeline.
      AWS does support tags on subnet level. status endpoint and STEP_FUNCTIONS_RUN_VRA_WORKFLOW (SUCCESSFUL)
      No need to test BYOC again here if you already created SCC Connected with BYOC."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-NETWORK-DELETION-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: DELETE
    Use case: Delete additional VPC with incorrect virtual network name
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: "{{baseUrl}}/network?cloud-provider=aws&account-id=<delwscc01>"
    Body: |
      {
        "dry-run": false,
        "region": "eu-central-1",
        "virtual-network-name": "my-vpc-name"
      }
    Response: |
      {
        "message": {
          "response": "No VPC found for my-vpc-name1 in xxxxxxxx and eu-central-1.",
          "action": Manual intervenation is required!....,
          "vpcs": [
            {...},
            {...},
            etc.
          ],
        "code": 404
      }
    Result:
    Remark: |
      You will get the same error for already deleted VPC.
      You can take this as kind of added validation that will not trigger step function.
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-NETWORK-DELETION-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: DELETE
    Use case: Delete "base" VPC by virtual network name
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: "{{baseUrl}}/network?cloud-provider=aws&account-id=<delwscc01>"
    Body: |
      {
        "dry-run": false,
        "region": "eu-central-1",
        "virtual-network-name": "<delwscc01>"
      }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      This "base" VPC is created automatically together with SCC connected account.
      By deleting this VPC you would create SCC basic account (no VPC).
      Therefore, this is not allowed and VPC should be deleted together with account
      by account deletion endpoint.
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-NETWORK-DELETION-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: DELETE
    Use case: Delete additional VPC A with correct virtual network name in dry-run mode
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: "{{baseUrl}}/network?cloud-provider=aws&account-id=<delwscc01>"
    Body: |
      {
        "dry-run": true,
        "region": "eu-central-1",
        "virtual-network-name": "<delwscc01a>"
      }
    Response: |
      {
        "message": "Items to be deleted: NetworkDeleteRequest(dry_run=True, region='eu-central-1', virtual_network_name='<delwscc01b>', virtual_network_id='vpc-0b316da18eb3345ee', request_id='106ea73c765c4ea3b83e34519936b237')",
        "code": 200
      }
    Result:
    Remark: |
      This is preferred way to test deletion before actual execution.
      Previously, the DRY-RUN was running in the background (step function)
      and you had to check outputs of individual steps and Cloudwatch logs.
      This is much easier and faster way to test deletion.
      We do deletion by VpcId (virtual_network_id) and request-id.
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-NETWORK-DELETION-4
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: DELETE
    Use case: Delete additional VPC A just by correct virtual network name
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: "{{baseUrl}}/network?cloud-provider=aws&account-id=<delwscc01>"
    Body: |
      {
        "dry-run": false,
        "region": "eu-central-1",
        "virtual-network-name": "<delwscc01a>"
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark: |
      Check Network Deletion state machine finished successfully.
      Checkt in AWS console the resources are deleted.
      Check allocated CIDRs are deleted in CIDRAllocated table.
      Run this for every network extension use case.
      By this we will keep our account clean.
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-NETWORK-DELETION-5
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: DELETE
    Use case: Delete additional VPC A just by correct virtual network name again for already running deletion
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: "{{baseUrl}}/network?cloud-provider=aws&account-id=<delwscc01>"
    Body: |
      {
        "dry-run": false,
        "region": "eu-central-1",
        "virtual-network-name": "<delwscc01a>"
      }
    Response: |
      {
        "message": "There is already running integration for: <delwscc01>-<vpc-012345>",
        "code": 400
      }
    Result:
    Remark: |
      This must be executed right away after the previous (SCC-AWS-NETWORK-DELETION-3) case.
      If you will do it later when the previous deletion is finished, you will get error from
      SCC-AWS-NETWORK-DELETION-1 case.
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-NETWORK-DELETION-6
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: DELETE
    Use case: Delete additional VPC B by virtual network name / virtual network id
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: "{{baseUrl}}/network?cloud-provider=aws&account-id=<delwscc01>"
    Body: |
      {
        "dry-run": false,
        "region": "eu-central-1",
        "virtual-network-name": "<delwscc01b>",
        "virtual-network-id": <vpc-012345>
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark: |
      Check Network Deletion state machine finished successfully.
      Checkt in AWS console the resources are deleted.
      Check allocated CIDRs are deleted in CIDRAllocated table.
      Run this for every network extension use case.
      By this we will keep our account clean.
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-NETWORK-DELETION-7
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: DELETE
    Use case: Delete additional VPC C by virtual network name / virtual network id and request-id
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: "{{baseUrl}}/network?cloud-provider=aws&account-id=<delwscc01>"
    Body: |
      {
        "dry-run": false,
        "region": "eu-central-1",
        "virtual-network-name": "<delwscc01c>",
        "virtual-network-id": <vpc-987654>,
        "request-id": <xxxxxxx>
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark: |
      Check Network Deletion state machine finished successfully.
      Checkt in AWS console the resources are deleted.
      Check allocated CIDRs are deleted in CIDRAllocated table.
      Run this for every network extension use case.
      By this we will keep our account clean.
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-ACCOUNT-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: GET
    Use case: Get account with prefix
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: FCP
    URL: {{baseUrl}}/account?cloud-provider=aws&prefix=delwfcpbsc01
    Body: N/A
    Response: Get list of AWS FCP accounts matched with prefix
    Result:
    Remark: "Is there difference in AWS organization to determine FCP, SCC accounts?It does not return any FCP accounts at this moment"
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-ACCOUNT-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: GET
    Use case: Verify search should not be found if the account is not exiting
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: FCP
    URL: {{baseUrl}}/account?cloud-provider=aws&prefix=delwabc001
    Body: N/A
    Response:
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-ACCOUNT-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT/FCP
    Method: POST
    Use case: (Crossplane) FCP (dedicated) account creation should be successful
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/account/aws/url"
    Body: |
      {
        "accountData": {
          "accountTag": "delwfcpded02",
          "siNumber": "SI2895979",
          "accountOwners": ["extern.gavenda_jindrich@allianz.de","extern.baar_damian@allianz.de"],
          "integrationType": "dedicated",
          "customerEnvironment": "dev",
          "debtorNumber": "1200000024",
          "oeName": "Allianz Technology Global Linux",
          "profileName": "scc-dev-mxhkx"
        }
      }
    Response: |
      {
        "requestId": "xxxx"
      }
    Result:
    Remark: |
      (Crossplane) FCP (dedicated) account is created via Step Functions (state machnine).

      Verify account cretion in AWS console (Step Functions).
      Alternatively, by checking /account/status/by or /status endpoint.

      The GIAM integration is triggered the same way as for SCC Basic, Connected.
      There is vRA integration via {{baseUrl}}/network/autodiscovery/url endpoint.
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-ACCOUNT-4
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT/FCP
    Method: POST
    Use case: (Crossplane) FCP (dedicated) account with exiting account should be failed
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/account/aws/url"
    Body: |
      {
        "accountData": {
          "accountTag": "delwfcpded02",
          "siNumber": "SI2895979",
          "accountOwners": ["extern.gavenda_jindrich@allianz.de","extern.baar_damian@allianz.de"],
          "integrationType": "dedicated",
          "customerEnvironment": "dev",
          "debtorNumber": "1200000024",
          "oeName": "Allianz Technology Global Linux",
          "profileName": "scc-dev-mxhkx"
        }
      }
    Response: |
      {
        "code": 400,
        "message": "Errors: Account already exists."
      }
    Result:
    Remark: |
      no need to test because FCP AWS there is limitation as is driven by crossplane
      so we can call this endpoint multiple times with the same payload
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-ACCOUNT-5
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT/FCP
    Method: POST
    Use case: (Crossplane) FCP (dedicated) account creation with testing validations first (duplicated owners email) should not be successful
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/account/aws/url"
    Body: |
      {
        "accountData": {
          "accountTag": "delwfcpded03",
          "siNumber": "SI2895979",
          "accountOwners": ["extern.baar_damian@allianz.de","extern.baar_damian@allianz.de"],
          "integrationType": "dedicated",
          "customerEnvironment": "dev",
          "debtorNumber": "1200000024",
          "oeName": "Allianz Technology Global Linux",
          "profileName": "scc-dev-mxhkx"
        }
      }
    Response: |
      {
        "message": {"message": "Errors: Owners must be unique", "code": 400}
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-ACCOUNT-6
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT/FCP
    Method: POST
    Use case: (Crossplane) FCP (dedicated) account creation with testing validations first (only one owner provided) should not be allowed
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated (Subscription)
    Service type: FCP
    URL: "{{baseUrl}}/account/aws/url"
    Body: |
      {
        "accountData": {
          "siNumber": "SI2895979",
          "accountTag": "delwfcpded03",
          "accountOwners": ["extern.baar_damian@allianz.de"],
          "customerEnvironment": "dev",
          "debtorNumber": "1200000024",
          "oeName": "Allianz Technology Global Linux",
          "profileName": "scc-dev-mxhkx",
          "cloudRegion": "germanywestcentral"
        }
      }
    Response: |
      {
        "message": "Validation error: [{'message': "['extern.baar_damian@allianz.de'] is too short"
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-ACCOUNT-7
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT/FCP
    Method: POST
    Use case: (Crossplane) FCP (dedicated) account creation should not be allowed if the length of account name is longer than 15 characters
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated (Subscription)
    Service type: FCP
    URL: "{{baseUrl}}/account/aws/url"
    Body: |
      {
        "accountData": {
          "accountTag": "delwfcpded0234567890",
          "siNumber": "SI2895979",
          "accountOwners": ["extern.gavenda_jindrich@allianz.de","extern.baar_damian@allianz.de"],
          "integrationType": "dedicated",
          "customerEnvironment": "dev",
          "debtorNumber": "1200000024",
          "oeName": "Allianz Technology Global Linux",
          "profileName": "scc-dev-mxhkx"
        }
      }
    Response: |
      {
        "message": "Validation error: [{'message': "'delwfcpded0234567890' is too long"
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-ACCOUNT-8
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: GET
    Use case: Get all FCP AWS accounts ID
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: FCP
    URL: {{baseUrl}}/account?cloud-provider=aws
    Body: N/A
    Response: All accounts for AWS
    Result:
    Remark: Run this after you create these test accounts
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-ACCOUNT-9
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: POST
    Use case: Create FCP AWS basic account with non-existing profile name
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Basic
    Service type: FCP
    URL: {{baseUrl}}/account?cloud-provider=aws
    Body: |
      {
        "accountData": {
          "accountTag": "delwfcpded02",
          "siNumber": "SI1234567",
          "accountOwners": ["extern.gavenda_jindrich@allianz.de","extern.baar_damian@allianz.de"],
          "integrationType": "dedicated",
          "customerEnvironment": "dev",
          "debtorNumber": "1200000024",
          "oeName": "az-tec",
          "profileName": "Not exist"
        }
      }
    Response: |
      {
        "code": 400,
        "message": "Errors: profile name doesn't exists."
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-ACCOUNT-DELETE-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: DELETE
    Use case: Account (Shared) deletion (no restore)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Shared
    Service type: FCP
    URL: {{baseUrl}}/account?cloud-provider=aws&account-id=<delafcpbsc01>
    Body: |
        {
          "dry-run": false
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "Scenario has NOT tested before need to verify.
      Check AWS delete account step function (success).
      Check in AWS console the resources are deleted and accounts is in deleted_accounts OU.
      Run this for every account creation use case.
      By this we will keep our environments clean."
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-ACCOUNT-DELETE-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT
    Method: DELETE
    Use case: Account (Dedicated) deletion (no restore)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: {{baseUrl}}/account?cloud-provider=aws&account-id=<delwfcpded01>
    Body: |
        {
          "dry-run": false
        }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      "Scenario has NOT tested before need to verify.
      Check AWS delete account step function (success).
      Check in AWS console the resources are deleted and accounts is in deleted_accounts OU.
      Check allocated CIDRs are deleted in CIDRAllocated table.
      Run this for every account creation use case.
      By this we will keep our environments clean."
    JIRA:
    GHE:
-
    Testcase ID: FCP-LEGACY-AWS-ACCOUNT-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT/FCP
    Method: POST
    Use case: (Legacy) FCP (shared) account creation
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Shared
    Service type: FCP
    URL: "{{baseUrl}}/account/fcp"
    Body: |
      {
        "account-data": {
          "si-number": "SI2896032",
          "account-tag": "delwfcpbsc01",
          "account-owners": ["extern.gavenda_jindrich@allianz.de","extern.baar_damian@allianz.de"],
          "customer-environment": "test",
          "debtor-number": "1200000024",
          "cloud-provider": "aws",
          "oe-name": "az-tec",
          "profile-name": "Cloud Accounts"
        }
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark: |
      (Legacy) FCP (shared) account is created via Step Functions (state machnine).

      Verify account cretion in AWS console (Step Functions).
      Alternatively, by checking /account/status/by or /status endpoint.

      The GIAM integration is triggered the same way as for SCC Basic, Connected.
      There is no vRA integration in place.
    JIRA: |
      FCP-13318
    GHE:
-
    Testcase ID: FCP-LEGACY-AWS-ACCOUNT-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT/FCP
    Method: POST
    Use case: (Legacy) FCP (shared) account creation without sending any notificaiton on Success
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Shared
    Service type: FCP
    URL: "{{baseUrl}}/account/fcp"
    Body: |
      {
        "account-data": {
          "si-number": "SI2896032",
          "account-tag": "delwfcpbsc01",
          "account-owners": ["extern.gavenda_jindrich@allianz.de","extern.baar_damian@allianz.de"],
          "customer-environment": "test",
          "debtor-number": "1200000024",
          "cloud-provider": "aws",
          "oe-name": "az-tec",
          "profile-name": "Cloud Accounts"
        },
        "config": {
          "send-mails": false
        }
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark: |
      (Legacy) FCP (shared) account is created via Step Functions (state machnine).
      This cannot be combined with /network/fcp or /network/aws/url endpoints.

      Verify account cretion in AWS console (Step Functions).
      Alternatively, by checking /account/status/by or /status endpoint.

      The GIAM integration is triggered the same way as for SCC Basic, Connected.
      There is no vRA integration in place.
    JIRA: |
      FCP-13318
    GHE:
-
    Testcase ID: FCP-LEGACY-AWS-ACCOUNT-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT/FCP/RERUN
    Method: POST
    Use case: (Legacy) FCP (shared) account creation re-run
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Shared
    Service type: FCP
    URL: "{{baseUrl}}/account/fcp/rerun"
    Body: |
      {
        "status-id": "STATUS#AWS#1200000024#delwfcpbsc01-t-xxxx",
        "steps": [
          "STEP_ACCOUNT_CREATION_VALIDATION",
          "STEP_ACCOUNT_CREATION_REGISTER",
        ]
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark: |
      It will force to rerun given step(s) no matter what was their previous state.
      Select steps without potential side effect for testing such as "Check environment for run" or "Record account tags".

      (Legacy) FCP (shared) account is created via Step Functions (state machnine).
      You can see progress/result directly in AWS console (state machine) or by checking account/status/by or /status endpoints.
    JIRA:
    GHE:
-
    Testcase ID: FCP-LEGACY-AWS-ACCOUNT-4
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: ACCOUNT/FCP
    Method: POST
    Use case: (Legacy) FCP (dedicated) account creation
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/account/fcp"
    Body: |
      {
        "account-data": {
          "si-number": "SI2896032",
          "account-tag": "delwfcpded01",
          "account-owners": ["extern.gavenda_jindrich@allianz.de","extern.baar_damian@allianz.de"],
          "customer-environment": "test",
          "debtor-number": "1200000024",
          "cloud-provider": "aws",
          "oe-name": "az-tec",
          "profile-name": "Cloud Accounts"
        },
        "network-data": {
          "cloud-network-name": "delwfcpded01",
          "cloud-region": "eu-central-1",
          "number-availability-zones": 2,
          "interaction-subnet": {
            "naming-pattern": "interaction",
            "sizes": [28,28]
          },
          "enterprise-subnet": {
            "naming-pattern": "enterprise",
            "sizes": [28,28]
          },
          "management-subnet": {
            "naming-pattern": "management",
            "sizes": [28,28]
          }
        }
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark: |
      (Legacy) FCP (dedicated) account is created via Step Functions (state machnine).

      Verify account cretion in AWS console (Step Functions).
      Alternatively, by checking /account/status/by or /status endpoint.

      The GIAM integration is triggered the same way as for SCC Basic, Connected.
      There is no vRA integration in place.
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-NETWORK-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: GET
    Use case: 'Get account''s network details'
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Shared
    Service type: FCP
    URL: {{baseUrl}}/network?cloud-provider=aws&account-id=<delwfcpbsc01>
    Body: N/A
    Response: |
        {
          "account-id": "<delabsc01>",
          "cloud-networks": []
        }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-NETWORK-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: POST
    Use case: Add mandatory subnets to the existing (crossplane) FCP dedicated account
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/network/aws/url"
    Body: |
      {
        "accountId": "xxxxxxx",
        "networkData": {
          "cloudRegion": "eu-central-1",
          "cloudNetworkName": "delwfcpded02a",
          "numberAvailabilityZones": 2,
          "eksSubnets": {
            "enabled": true,
            "transitional": true
          },
          "enterpriseSubnet": {
            "sizes": [28,28]
          },
          "interactionSubnet": {
            "sizes": [28,28]
          },
          "managementSubnet": {
            "sizes": [28,28]
          }
        }
      }
    Response: |
      {
        "requestId": "xxxx"
      }
    Result:
    Remark: |
      Verify resource creation in one of these:
      - Codebuild pipeline (success)
      - /status endpoint and STEP_FCP_NETWORK_EXTENSION_CREATION(SUCCESSFUL)
      - AWS portal (console)

      Verify CIDR allocation records in CIDRAllocated table
      {{baseUrl}}/cidr/allocation?account-name=delwfcpded02-<xphash>-t-<projecthash>

      Tags are applied in terraform directly in network creation Codebuild pipeline.
      AWS does support tags on subnet level.
      There is vRA integration via {{baseUrl}}/network/autodiscovery/url endpoint.
    JIRA: |
      FCP-13318
    GHE:
-
    Testcase ID: FCP-AWS-NETWORK-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: POST
    Use case: Add all subnets to the existing (crossplane) FCP dedicated account
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/network/aws/url"
    Body: |
      {
        "accountId": "xxxxxxx",
        "networkData": {
          "cloudRegion": "eu-central-1",
          "cloudNetworkName": "delwfcpded02b",
          "numberAvailabilityZones": 2,
          "eksSubnets": {
            "enabled": false,
            "transitional": false
          },
          "interactionSubnet": {
            "sizes": [28,28]
          },
          "enterpriseSubnet": {
            "sizes": [28,28]
          },
          "managementSubnet": {
            "sizes": [28,28]
          },
          "internetSubnet": {
            "sizes": [28,28]
          },
          "transitionalSubnet": {
            "sizes": [28,28]
          },
          "agnSubnet": {
            "sizes": [28,28]
          }
        }
      }
    Response: |
      {
        "requestId": "xxxx"
      }
    Result:
    Remark: |
      Verify resource creation in one of these:
      - Codebuild pipeline (success)
      - /status endpoint and STEP_FCP_NETWORK_EXTENSION_CREATION(SUCCESSFUL)
      - AWS portal (console)

      Verify CIDR allocation records in CIDRAllocated table
      {{baseUrl}}/cidr/allocation?account-name=delwfcpded02-<xphash>-t-<projecthash>

      Tags are applied in terraform directly in network creation Codebuild pipeline.
      AWS does support tags on subnet level.
      There is vRA integration via {{baseUrl}}/network/autodiscovery/url endpoint.
    JIRA: |
      FCP-13318
    GHE:
-
    Testcase ID: FCP-AWS-NETWORK-4
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: POST
    Use case: Verify CIDRs allocation should be worked properly when create 3 vpc in pararell
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/network/aws/url"
    Body: |
      body1 = {
        "accountId": "account_id1",
        "networkData": {
            "cloudRegion": "eu-central-1",
            "cloudNetworkName": "(vpc1",
            "numberAvailabilityZones": 2,
            "eksSubnets": {
            "enabled": False,
            "transitional": False
            },
            "interactionSubnet": {
            "sizes": [28, 28]
            },
            "enterpriseSubnet": {
            "sizes": [28, 28]
            },
            "managementSubnet": {
            "sizes": [28, 28]
            }
        }
    }

    body2 = {
        "accountId": "account_id2",
        "networkData": {
            "cloudRegion": "eu-central-1",
            "cloudNetworkName": "vpc2",
            "numberAvailabilityZones": 2,
            "eksSubnets": {
            "enabled": False,
            "transitional": False
            },
            "interactionSubnet": {
            "sizes": [28, 28]
            },
            "enterpriseSubnet": {
            "sizes": [28, 28]
            },
            "managementSubnet": {
            "sizes": [28, 28]
            }
        }
    }

    body3 = {
        "accountId": "account_id3",
        "networkData": {
            "cloudRegion": "eu-central-1",
            "cloudNetworkName": "vpc3",
            "numberAvailabilityZones": 2,
            "eksSubnets": {
            "enabled": False,
            "transitional": False
            },
            "interactionSubnet": {
            "sizes": [28, 28]
            },
            "enterpriseSubnet": {
            "sizes": [28, 28]
            },
            "managementSubnet": {
            "sizes": [28, 28]
            }
        }
    }
    Response: |
      {
        "requestId": "xxxx"
      }
    Result:
    Remark: Verify network creation in concurrently
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-NETWORK-DELETION-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: DELETE
    Use case: Delete DedicatedVPC with incorrect virtual network name
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/network?cloud-provider=aws&account-id=<dwfa01>"
    Body: |
      {
        "dry-run": false,
        "region": "eu-central-1",
        "virtual-network-name": "my-vpc-name"
      }
    Response: |
      {
        "message": {
          "response": "No VPC found for my-vpc-name1 in xxxxxxxx and eu-central-1.",
          "action": Manual intervenation is required!....,
          "vpcs": [
            {...},
            {...},
            etc.
          ],
        "code": 404
      }
    Result:
    Remark: |
      You will get the same error for already deleted VPC.
      You can take this as kind of added validation that will not trigger step function.
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-NETWORK-DELETION-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: DELETE
    Use case: Delete DedicatedVPC A with correct virtual network name in dry-run mode
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/network?cloud-provider=aws&account-id=<dwfa01>"
    Body: |
      {
        "dry-run": true,
        "region": "eu-central-1",
        "virtual-network-name": "<dwfn01a-abcde>"
      }
    Response: |
      {
        "message": "Items to be deleted: NetworkDeleteRequest(dry_run=True, region='eu-central-1', virtual_network_name='dwfn01a-pmccs', virtual_network_id='vpc-0368f23c9d819f584', request_id='37d1bf960b6140ce98b77ec7dbac6e81')",
        "code": 200
      }
    Result:
    Remark: |
      This is preferred way to test deletion before actual execution.
      Previously, the DRY-RUN was running in the background (step function)
      and you had to check outputs of individual steps and Cloudwatch logs.
      This is much easier and faster way to test deletion.
      We do deletion by VpcId (virtual_network_id) and request-id.
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-NETWORK-DELETION-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: DELETE
    Use case: Delete DedicatedVPC A just by correct virtual network name
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/network?cloud-provider=aws&account-id=<dwfa01>"
    Body: |
      {
        "dry-run": false,
        "region": "eu-central-1",
        "virtual-network-name": "<dwfn01a-abcde>"
      }
    Response: |
      {
        ""request-id"": ""xxxx""
      }
    Result:
    Remark: |
      Check Network Deletion state machine finished successfully.
      Checkt in AWS console the resources are deleted.
      Check allocated CIDRs are deleted in CIDRAllocated table.
      Run this for every network extension use case.
      By this we will keep our account clean.
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-NETWORK-DELETION-4
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: DELETE
    Use case: DedicatedVPC A just by correct virtual network name again for already running deletion
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/network?cloud-provider=aws&account-id=<dwfa01>"
    Body: |
      {
        "dry-run": false,
        "region": "eu-central-1",
        "virtual-network-name": "<dwfn01a-abcde>"
      }
    Response: |
      {
        "message": "There is already running integration for: <dwfn01a-abcde>-<vpc-012345>",
        "code": 400
      }
    Result:
    Remark: |
      This must be executed right away after the previous (FCP-AWS-NETWORK-DELETION-3) case.
      If you will do it later when the previous deletion is finished, you will get error from
      FCP-AWS-NETWORK-DELETION-1 case.
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-NETWORK-DELETION-5
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: DELETE
    Use case: Delete DedicatedVPC B by virtual network name / virtual network id
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/network?cloud-provider=aws&account-id=<dwfa01>"
    Body: |
      {
        "dry-run": false,
        "region": "eu-central-1",
        "virtual-network-name": "<dwfn01b-fghijk>",
        "virtual-network-id": <vpc-678901>
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark: |
      Check Network Deletion state machine finished successfully.
      Checkt in AWS console the resources are deleted.
      Check allocated CIDRs are deleted in CIDRAllocated table.
      Run this for every network extension use case.
      By this we will keep our account clean.
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-NETWORK-DELETION-6
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: DELETE
    Use case: Delete DedicatedVPC C by virtual network name / virtual network id and request-id
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/network?cloud-provider=aws&account-id=<dwfa01>"
    Body: |
      {
        "dry-run": false,
        "region": "eu-central-1",
        "virtual-network-name": "<dwfn01c-lmnop>",
        "virtual-network-id": <vpc-987654>,
        "request-id": <xxxxxxx>
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark: |
      Check Network Deletion state machine finished successfully.
      Checkt in AWS console the resources are deleted.
      Check allocated CIDRs are deleted in CIDRAllocated table.
      Run this for every network extension use case.
      By this we will keep our account clean.
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-NETWORK-DELETION-7
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: DELETE
    Use case: Delete Network in (Crossplane) FCP (dedicated) account
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/network?cloud-provider=aws&account-id=<dwfa01>"
    Body: |
      {
        "dry-run": false,
        "region": "eu-central-1",
        "virtual-network-name": "<dwfn01b-fghijk>",
        "virtual-network-id": <vpc-678901>
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-NETWORK-DELETION-8
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: DELETE
    Use case: Delete Network in (Crossplane) FCP (dedicated) account again
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/network?cloud-provider=aws&account-id=<dwfa01>"
    Body: |
      {
        "dry-run": false,
        "region": "eu-central-1",
        "virtual-network-name": "<dwfn01b-fghijk>",
        "virtual-network-id": <vpc-678901>
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark: |
      Check Network Deletion state machine finished successfully.
      Checkt in AWS console the resources are deleted.
      Check allocated CIDRs are deleted in CIDRAllocated table.
      Run this for every network extension use case.
      By this we will keep our account clean.
    JIRA:
    GHE:
-
    Testcase ID: FCP-AWS-NETWORK-DELETION-9
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK
    Method: DELETE
    Use case: Delete Network in (Crossplane) FCP (dedicated) account (Full subnet)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/network?cloud-provider=aws&account-id=<dwfa01>"
    Body: |
      {
        "dry-run": false,
        "region": "eu-central-1",
        "virtual-network-name": "<dwfn01f-fghijk>",
        "virtual-network-id": <vpc-678901>
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-AUTODISCOVERY-1
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: Y
    Cloud Privder: Azure
    Endpoint: NETWORK/AUTODISCOVERY
    Method: POST
    Use case: Register Azure SCC Connected account to VRA
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/network/autodiscovery
    Body: |
      {
        "cloud-provider": "azure",
        "account-id": <delascc01>,
        "account-name": "delascc01-germanywestcentral-test",
        "project-name": "Cloud Accounts",
        "debtor-number": 1200000024
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark: |
      Verify vRA state machine was triggered and applied tag in networks:
      account_name, vnet, subnet_type, resourge_group

      Azure does NOT support tags on subnet level.

      /status endpoint and DataItemId: VRA#WORKFLOW_STATE#SUCCESSFUL
    JIRA: |
      FCP-12137
    GHE: |
      https://github.developer.allianz.io/CloudTribe/scc-api/pull/1104
-
    Testcase ID: SCC-AWS-AUTODISCOVERY-1
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK/AUTODISCOVERY
    Method: POST
    Use case: Register AWS SCC Connected account to VRA
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/network/autodiscovery
    Body: |
      {
        "cloud-provider": "aws",
        "account-id": <delwscc01>,
        "account-name": "delwscc01-t-xxxx",
        "project-name": "Cloud Accounts",
        "debtor-number": 1200000024
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark: |
      Verify vRA state machine was triggered and applied tag in networks:
      account_name, vnet, subnet_type

      Tags are applied in terraform directly in network creation Codebuild pipeline.
      AWS does support tags on subnet level.
      This needs to be checked extra in network creation part (TF output in Extra details?).

      /status endpoint and DataItemId: VRA#WORKFLOW_STATE#SUCCESSFUL
    JIRA: |
      FCP-12137
      FCP-13318
    GHE: |
      https://github.developer.allianz.io/CloudTribe/scc-api/pull/1104
-
    Testcase ID: FCP-AWS-AUTODISCOVERY-1
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK/AUTODISCOVERY
    Method: POST
    Use case: Register AWS FCP Dedicated account to VRA
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: {{baseUrl}}/network/autodiscovery/url
    Body: |
      {
        "cloudProvider": "aws",
        "accountId": <delwfcpded01>,
        "accountName": "delwfcpded01-t-xxxx",
        "projectName": "Cloud Accounts",
        "debtorNumber": 1200000024
      }
    Response: |
      {
        "requestId": "xxxx"
      }
    Result:
    Remark: |
      Verify vRA state machine was triggered and applied tags only in transitional network:
      account_name, vnet, subnet_type

      Tags are applied in terraform directly in network creation Codebuild pipeline.
      AWS does support tags on subnet level.
      This needs to be checked extra in network creation part (TF output in Extra details?).

      /status endpoint and DataItemId: VRA#WORKFLOW_STATE#SUCCESSFUL
    JIRA: |
      FCP-12137
      FCP-13318
    GHE: |
      https://github.developer.allianz.io/CloudTribe/scc-api/pull/1104
-
    Testcase ID: FCP-AWS-AUTODISCOVERY-2
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: Y
    Cloud Privder: AWS
    Endpoint: NETWORK/AUTODISCOVERY
    Method: POST
    Use case: Register AWS FCP Dedicated account without any VPC to VRA
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: {{baseUrl}}/network/autodiscovery/url
    Body: |
      {
        "cloudProvider": "aws",
        "accountId": <delwfcpded01>,
        "accountName": "delwfcpded01-t-xxxx",
        "projectName": "Cloud Accounts",
        "debtorNumber": 1200000024
      }
    Response: |
      {
        "message": "There are no transitional subnets in your account! SCC+ vRA integration cannot be triggered.",
        "code": 404
      }
    Result:
    Remark: |
      Verify vRA state machine was NOT triggered.
    JIRA: |
      FCP-16107
    GHE: |
      https://github.developer.allianz.io/CloudTribe/scc-api/pull/1239
-
    Testcase ID: SCC-CIDR-1
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: Y
    Cloud Privder: Any
    Endpoint: CIDR/FREE
    Method: GET
    Use case: Get all free CIDR ranges per region for both AWS/Azure providers
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/free
    Body: N/A
    Response: |
        Example{
          "eu-central-1": [
            "44.120.65.128/25",
            "44.120.247.208/28",
            "44.120.255.0/24"
          ],
          "westeurope": [
            "44.112.105.0/24",
          ],...
        }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-CIDR-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: CIDR/FREE
    Method: POST
    Use case: Check if a given CIDR in provided region is free
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/free
    Body: |
        {
          "CloudRegion": "germanywestcentral",
          "CIDR": "xxxx"
        }
    Response: "Provided CIDR(xxxx) is free."
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-CIDR-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: CIDR/ALLOCATION
    Method: POST
    Use case: Add existing CIDR to CIDRAllocated table for your test account and correct region
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/allocation?cloud-provider=azure
    Body: |
      {
        "region": "germanywestcentral",
        "cidr": "xxxxx",
        "account-name": "xxxx",
        "reason": "Manually aligning data for this account"
      }
    Response: |
      "Example (error)
        {
          "code": 500,
          "message": "Provided CIDR is already occupied. Free are: ['aaaaa', 'bbbbb', 'ccccc']"
        }
    Result:
    Remark: "The CIDR in body is already in CIDRAllocated table for this regionThere is only "germanywestcentral" region in Azure staging. Test with this region."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-CIDR-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: CIDR/ALLOCATION
    Method: POST
    Use case: Add a new CIDR to CIDRAllocated table for your test account and wrong region
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/allocation?cloud-provider=azure
    Body: |
        {
          "region": "westeurope",
          "cidr": "xxxxx",
          "account-name": "xxxxx",
          "reason": "Manually aligning data for this account"
        }
    Response: |
        {
          "code": 500,
          "message": "Provided CIDR is not part of the block"
        }
    Result:
    Remark: "The CIDR in body is from "australiaeast" region which is the correct oneThere is only "germanywestcentral" region in Azure staging. Test with this region."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-CIDR-4
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: CIDR/ALLOCATION
    Method: POST
    Use case: Add a new CIDR to CIDRAllocated table for your test account and correct region
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/allocation?cloud-provider=azure
    Body: |
        {
          "region": "germanywestcentral",
          "cidr": "xxxxx",
          "account-name": "xxxxx",
          "reason": "Manually aligning data for this account"
        }
    Response: |
        {
          "Block": [
            "xxxxx"
          ],
          "Subnet": "xxxxx",
          "Cidr": "xxxxx",
          "Region": "germanywestcentral",
          "AccountName": "xxxxx",
          "Reason": "Manually aligning data for this account"
        }
    Result:
    Remark: |
      "There is only "germanywestcentral" region in Azure staging.
      Test with this region.Steps to test this completely:
      1. use GET cidr/free to get free CIDRs in region where you created your test account
      2. use this POST to create a new record for your test accountCheck the record created in CIDRAllocated table.
      All the values from payload should be correctly recorded - last time reason was missing.
      3. use the below DELETE to remove the record you just created"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-CIDR-5
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: CIDR/ALLOCATION
    Method: DELETE
    Use case: Delete existing CIDR in CIDRAllocated table for your test account
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/allocation?cidr=xxxx
    Body: N/A
    Response: "[    "xxxx"]"
    Result:
    Remark: |
      "There is only "germanywestcentral" region in Azure staging.
      Test with this region.Do not forget to delete manually created CIDR record in CIDRAllocated table!
      Verify that record was delete in CIDRAllocated table."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-CIDR-6
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: CIDR/ALLOCATION
    Method: DELETE
    Use case: Delete allocation CIDR for your test account with invalid param
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/allocation?cidr=xxxx
    Body: N/A
    Response: |
      {
    "code": 500,
    "message": [
        {
                "message": "'pool' is a required property",
                "schema": {
                    "title": "With cidr or request-id",
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "description": "Query param validator",
                    "one-of": [
                        {
                            "$ref": "WithCIDR"
                        },
                        {
                            "$ref": "WithRequestId"
                        }
                    ],
                    "$id": "CIDRCleanupParams"
                },
                "sub-schema": {
                    "title": "With CIDR",
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "type": "object",
                    "description": "Query param validator",
                    "required": [
                        "cidr",
                        "pool"
                    ],
                    "properties": {
                        "cidr": {
                            "type": "string",
                            "min-length": 2
                        },
                        "pool": {
                            "type": "string",
                            "description": "Region or cidr pool, i.e. eu-central-1#dev#interaction"
                        }
                    },
                    "$id": "WithCIDR"
                },
                "instance": {
                    "cidr": "xxx"
                }
              }
          ]
        }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-CIDR-7
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: CIDR/ALLOCATION
    Method: DELETE
    Use case: Delete not existing CIDR in CIDR Allocated table
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/allocation?cidr=xxxx&pool=eu-central-1
    Body: N/A
    Response: "["xxxx"]"
    Result:
    Remark: |
      To test
      1. Get free CIDR and select any CIDR "xxxx"
      2. Delete that selected CIDR
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-CIDR-8
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: CIDR/ALLOCATION
    Method: DELETE
    Use case: Delete CIDR with different Pool
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/allocation?cidr=xxxx&pool=germanywestcentral
    Body: N/A
    Response: "["xxxx"]"
    Result:
    Remark: |
      To test
      1. Get free CIDR and select any CIDR "xxxx" from eu-central-1
      2. Delete selected CIDR with pool=germanywestcentral
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-CIDR-9
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: CIDR/ALLOCATION
    Method: GET
    Use case: Get CIDR allocations for account
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/allocation?account-name=${account_name}
    Body: N/A
    Response: |
                [
            {
                "SubnetType": "routable",
                "Block": [
                    "44.109.0.0/18",
                    "44.120.192.0/18",
                    "44.120.128.0/18",
                    "44.120.92.0/22",
                    "44.120.112.0/20",
                    "44.142.12.0/23"
                ],
                "Subnet": "44.109.50.144/28",
                "Cidr": "44.109.50.144/28",
                "Region": "eu-central-1",
                "AccountName": "dwfanp-068-d-nFVPrW8LgqM",
                "Reason": "Manually aligning data for this account"
            },
            {
                "SubnetType": "routable",
                "Block": [
                    "44.109.0.0/18",
                    "44.120.192.0/18",
                    "44.120.128.0/18",
                    "44.120.92.0/22",
                    "44.120.112.0/20",
                    "44.142.12.0/23"
                ],
                "Subnet": "44.109.50.144/28",
                "Cidr": "44.109.50.144/28",
                "Region": "eu-west-3",
                "AccountName": "dwfanp-068-d-nFVPrW8LgqM",
                "Reason": "Manually aligning data for this account"
            }
        ]
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-CIDR-10
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: CIDR/ALLOCATION
    Method: GET
    Use case: Get details for allocated CIDR (subnet)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/allocation?subnet=44.109.50.144/28
    Body: N/A
    Response: |
        [
            {
                "SubnetType": "routable",
                "Block": [
                    "44.109.0.0/18",
                    "44.120.192.0/18",
                    "44.120.128.0/18",
                    "44.120.92.0/22",
                    "44.120.112.0/20",
                    "44.142.12.0/23"
                ],
                "Subnet": "44.109.50.144/28",
                "Cidr": "44.109.50.144/28",
                "Region": "eu-central-1",
                "AccountName": "dwfanp-068-d-nFVPrW8LgqM",
                "Reason": "Manually aligning data for this account"
            },
            {
                "SubnetType": "routable",
                "Block": [
                    "44.109.0.0/18",
                    "44.120.192.0/18",
                    "44.120.128.0/18",
                    "44.120.92.0/22",
                    "44.120.112.0/20",
                    "44.142.12.0/23"
                ],
                "Subnet": "44.109.50.144/28",
                "Cidr": "44.109.50.144/28",
                "Region": "eu-west-3",
                "AccountName": "dwfanp-068-d-nFVPrW8LgqM",
                "Reason": "Manually aligning data for this account"
            }
        ]
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-CIDR-11
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: N
    Cloud Privder: Azure
    Endpoint: CIDR/BLOCK
    Method: POST
    Use case: Update existing list of main CIDR blocks for specific region
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/block
    Body: |
        {
          "Region": "germanywestcentral",
          "Provider": "azure",
          "Blocks": [
            "xxxx"
          ]
        }
    Response: |
        {
          "Blocks": [
            "xxxx"
          ],
          "Provider": "azure",
          "Region": "germanywestcentral"
        }
    Result:
    Remark: |
      "DANGEROUS: It overwrites existing CIDR values with the value provided in the payload (list)!
      You can easily delete all the previous CIDRs with the single one you see here in the body!!!
      It means we always have to take the list from CIDRBlockTable and append new value to preserve previous CIDRs!
      The above is not true for Customer UI, it works as one would expect(?!!!)There is only "germanywestcentral" region in Azure staging.
      Test with this region."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-CIDR-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: CIDR/FREE
    Method: POST
    Use case: Check if a given CIDR in provided region is free
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/free
    Body: |
        {
          "CloudRegion": "eu-central-1",
          "CIDR": "xxxx"
        }
    Response: "Provided CIDR(xxxx) is free."
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-CIDR-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: CIDR/ALLOCATION
    Method: POST
    Use case: Add existing CIDR to CIDRAllocated table for your test account and correct region
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/allocation?cloud-provider=aws
    Body: |
        {
          "region": "eu-central-1",
          "cidr": "xxxxx",
          "account-name": "xxxx",
          "reason": "Manually aligning data for this account"
        }
    Response: |
        Example (error)
        {
          "code": 500,
          "message": "Provided CIDR is already occupied. Free are: ['aaaaa', 'bbbbb', 'ccccc']"
        }
    Result:
    Remark: "The CIDR in body is already in CIDRAllocated table for this region"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-CIDR-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: CIDR/ALLOCATION
    Method: POST
    Use case: Add a new CIDR to CIDRAllocated table for your test account and wrong region
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/allocation?cloud-provider=aws
    Body: |
        {
          "region": "eu-west-3",
          "cidr": "xxxxx",
          "account-name": "xxxxx",
          "reason": "Manually aligning data for this account"
        }
    Response: |
        {
          "code": 500,
          "message": "Provided CIDR is not part of the block"
        }
    Result:
    Remark: The CIDR in body is from "eu-central-1" region which is the correct one
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-CIDR-4
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: CIDR/ALLOCATION
    Method: POST
    Use case: Add a new CIDR to CIDRAllocated table for your test account and correct region
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/allocation?cloud-provider=aws
    Body: |
        {
          "region": "eu-central-1",
          "cidr": "xxxxx",
          "account-name": "xxxxx",
          "reason": "Manually aligning data for this account"
        }
    Response: |
        {
          "Block": [
            "xxxxx"
          ],
          "Subnet": "xxxxx",
          "Cidr": "xxxxx",
          "Region": "eu-central-1",
          "AccountName": "xxxxx",
          "Reason": "Manually aligning data for this account"
        }
    Result:
    Remark: |
      "Steps to test this completely:
      1. use GET cidr/free to get free CIDRs in region where you created your test account
      2. use this POST to create a new record for your test accountCheck the record created in CIDRAllocated table.
      All the values from payload should be correctly recorded - last time reason was missing.
      3. use the below DELETE to remove the record you just created"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-CIDR-5
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Any
    Endpoint: CIDR/ALLOCATION
    Method: DELETE
    Use case: Delete existing CIDR in CIDRAllocated table for your test account
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/allocation?cidr=xxxx
    Body: N/A
    Response: "[    "xxxx"]"
    Result:
    Remark: |
      "There is only "germanywestcentral" region in Azure staging.
      Test with this region.Do not forget to delete manually created CIDR record in CIDRAllocated table!
      Verify that record was delete in CIDRAllocated table."
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-CIDR-6
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Any
    Endpoint: CIDR/ALLOCATION
    Method: DELETE
    Use case: Delete allocation CIDR for your test account with invalid param
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/allocation?cidr=xxxx
    Body: N/A
    Response: |
      {
    "code": 500,
    "message": [
        {
                "message": "'pool' is a required property",
                "schema": {
                    "title": "With cidr or request-id",
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "description": "Query param validator",
                    "one-of": [
                        {
                            "$ref": "WithCIDR"
                        },
                        {
                            "$ref": "WithRequestId"
                        }
                    ],
                    "$id": "CIDRCleanupParams"
                },
                "sub-schema": {
                    "title": "With CIDR",
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "type": "object",
                    "description": "Query param validator",
                    "required": [
                        "cidr",
                        "pool"
                    ],
                    "properties": {
                        "cidr": {
                            "type": "string",
                            "min-length": 2
                        },
                        "pool": {
                            "type": "string",
                            "description": "Region or cidr pool, i.e. eu-central-1#dev#interaction"
                        }
                    },
                    "$id": "WithCIDR"
                },
                "instance": {
                    "cidr": "xxx"
                }
              }
          ]
        }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-CIDR-7
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Any
    Endpoint: CIDR/ALLOCATION
    Method: DELETE
    Use case: Delete not existing CIDR in CIDR Allocated table
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/allocation?cidr=xxxx&pool=eu-central-1
    Body: N/A
    Response: "["xxxx"]"
    Result:
    Remark: |
      To test
      1. Get free CIDR and select any CIDR "xxxx"
      2. Delete that selected CIDR
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-CIDR-8
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Any
    Endpoint: CIDR/ALLOCATION
    Method: DELETE
    Use case: Delete CIDR with different Pool
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/allocation?cidr=xxxx&pool=germanywestcentral
    Body: N/A
    Response: "["xxxx"]"
    Result:
    Remark: |
      To test
      1. Get free CIDR and select any CIDR "xxxx" from eu-central-1
      2. Delete selected CIDR with pool=germanywestcentral
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-CIDR-9
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: Y
    Cloud Privder: Any
    Endpoint: CIDR/ALLOCATION
    Method: GET
    Use case: Get CIDR allocations for account
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/allocation?account-name=<account name>
    Body: N/A
    Response: |
        Example from PROD[
          {
            "Block": [
              "aaaa"
            ],
            "Subnet": "xxxx",
            "Cidr": "xxxx",
            "Region": "germanywestcentral",
            "AccountName": "yyyy"
          },
          {
            "Block": [            aaaa,            bbbb,            cccc
            ],
            "Subnet": "xxxx",
            "Cidr": "xxxx",
            "Region": "westeurope",
            "AccountName": "yyyy"
          }
        ]
    Result:
    Remark: There is only "germanywestcentral" region in Azure staging. Test with this region.
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-CIDR-10
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: Y
    Cloud Privder: Any
    Endpoint: CIDR/ALLOCATION
    Method: GET
    Use case: Get details for allocated CIDR (subnet)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/allocation?subnet=<cidr>
    Body: N/A
    Response: |
        [
          {
            "Block": [
              "xxxx"
            ],
            "Subnet": "xxxx",
            "Cidr": "xxxx",
            "Region": "germanywestcentral",
            "AccountName": "yyyy"
          }
        ]
    Result:
    Remark: There is only "germanywestcentral" region in Azure staging. Test with this region.
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-CIDR-11
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: N
    Cloud Privder: AWS
    Endpoint: CIDR/BLOCK
    Method: POST
    Use case: Update existing list of main CIDR blocks for specific region
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/cidr/block
    Body: |
        {
          "Region": "eu-central-1",
          "Provider": "aws",
          "Blocks": [
            "44.143.224.0/19"
          ]
        }
    Response: |
        {
          "Blocks": [
            "44.143.224.0/19"
          ],
          "Provider": "aws",
          "Region": "eu-central-1"
        }
    Result:
    Remark: |
      "DANGEROUS: It overwrites existing CIDR values with the value provided in the payload (list)!
      You can easily delete all the previous CIDRs with the single one you see here in the body!!!
      It means we always have to take the list from CIDRBlockTable and append new value to preserve previous CIDRs!
      The above is not true for Customer UI, it works as one would expect(?!!!)"
    JIRA:
    GHE:
-
    Testcase ID: STATUS-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Any
    Endpoint: STATUS
    Method: GET
    Use case: Get list of steps (records) for provided (valid) request-id
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Any
    Service type: Any
    URL: {{baseUrl}}/status?request-id=<delabsc01>
    Body: N/A
    Response: Get list of records matching request-id
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: STATUS-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Any
    Endpoint: STATUS
    Method: GET
    Use case: Get list of steps (records) for provided (invalid) request-id
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Any
    Service type: Any
    URL: {{baseUrl}}/status?request-id=00000000000000000000000000000000
    Body: N/A
    Response: |
        {
          "code": 404,
          "message": "Status not found"
        }
    Result:
    Remark: "It's also used by Azure Jenkins pipelines for creating accounts / networks!We expect that response is 404 and message exactly "Status not found"."
    JIRA:
    GHE:
-
    Testcase ID: STATUS-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Any
    Endpoint: ACCOUNT/STATUS/BY
    Method: GET
    Use case: Get all account details from StateTable by StatusId
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: Any
    URL: {{baseUrl}}/account/status/by?status-id=STATUS%23AZURE%231200000024%delabsc01-germanywestcentral-test
    Body: N/A
    Response: Get list of all records matching StatusId from StateTable
    Result:
    Remark: |
      "Be aware that Postman automatically cutst '#'
      so paste value (StatusId) in Params tab (will be automatically url-encoded when saving)
      https://github.com/postmanlabs/postman-app-support/issues/8154ExampleSTATUS#AZURE#1200000024#delabsc01-germanywestcentral-testSTATUS%23AZURE%231200000024%23delabsc01-germanywestcentral-test"
    JIRA:
    GHE:
-
    Testcase ID: STATUS-4
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Any
    Endpoint: ACCOUNT/STATUS/BY
    Method: GET
    Use case: Get the latest single StatusId for given account
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: Any
    URL: {{baseUrl}}/account/status/by?status-id=STATUS%23AZURE%231200000024%23delabsc01-germanywestcentral-test&sort-by=CreatedAt&order-by=desc&limit=1
    Body: N/A
    Response: "Get list of filtered records matching Statusid from StateTable. It should only return 1 item in the list"
    Result:
    Remark: |
      "Be aware that Postman automatically cutst '#'
      so paste value (StatusId) in Params tab (will be automatically url-encoded when saving)
      https://github.com/postmanlabs/postman-app-support/issues/8154ExampleSTATUS#AZURE#1200000024#delabsc01-germanywestcentral-testSTATUS%23AZURE%231200000024%delabsc01-germanywestcentral-test"
    JIRA:
    GHE:
-
    Testcase ID: STATUS-5
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Any
    Endpoint: ACCOUNT/STATUS/BY
    Method: GET
    Use case: Get account details from StateTable by StatusId and additional parameters
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: Any
    URL: {{baseUrl}}/account/status/by?status-id=STATUS%23AZURE%231200000024%23delabsc01-germanywestcentral-test&sort-by=CreatedAt&order-by=desc&limit=5
    Body: N/A
    Response: "Get list of filtered records matching Statusid from StateTable. It should only return 5 items in the list"
    Result:
    Remark: |
      "Be aware that Postman automatically cutst '#'
      so paste value (StatusId) in Params tab (will be automatically url-encoded when saving)
      https://github.com/postmanlabs/postman-app-support/issues/8154ExampleSTATUS#AZURE#1200000024#delabsc01-germanywestcentral-testSTATUS%23AZURE%231200000024%delabsc01-germanywestcentral-test"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-JENKINS-PIPELINE-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: STATUS
    Method: POST
    Use case: Create steps records from Azure Jenkins pipeline
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/status?cloud-provider=azure
    Body: |
        multiple variants of payloads depending on type of account and stepsexample
        {
          "request-id": "${requestId}",
          "step": "${statusStep}",
          "value": "${statusValue}",
          "details": {
            "account-id": "${subsId}"
          }
        }
    Response: Status Item
    Result:
    Remark: |
      "We do not need to test it explicitly.
      It's part of account creation (basic, connected) for Azure and called directly from Azure Jenkins pipelines.
      If account creation (basic, connected) is successful, we can consider this as tested.
      We use it to create records for each step in account / network creation process in StateTable.aws_functions.groovy (updateAwsApiRequestStatus)"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-EDIT-STATUS-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: STATUS
    Method: PUT
    Use case: This overwrites "Details" element in specific StatusId and DataItemId
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/status?cloud-provider=azure
    Body: |
        multiple variants of payloads depending on type of account and stepsExample
        {
          "status_id": "xxxx",
          "data_item_id": "yyyy",
          "details": {
            "zzz1": "123",
            "zzz2": "456"
          }
        }
    Response: Status Item
    Result:
    Remark: "we can skip this test for nowit's unit tested and it's not used anywhere AFAIK"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-EDIT-STATUS-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: AWS
    Endpoint: STATUS
    Method: PUT
    Use case: This overwrites "Details" element in specific StatusId and DataItemId
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/status?cloud-provider=aws
    Body: |
        multiple variants of payloads depending on type of account and stepsExample
        {
          "status_id": "xxxx",
          "data_item_id": "yyyy",
          "details": {
            "zzz1": "123",
            "zzz2": "456"
          }
        }
    Response: Status Item
    Result:
    Remark: "we can skip this test for nowit's unit tested and it's not used anywhere AFAIK"
    JIRA:
    GHE:
-
    Testcase ID: STATUS-JENKINS-AZURE-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: STATUS/JENKINS
    Method: GET
    Use case: Get all account details from StateTable by StatusId
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/status/jenkins?status-id=STATUS%23AZURE%231200000024%delascc01-germanywestcentral-test
    Body: N/A
    Response: Get list of all records matching StatusId from StateTable
    Result:
    Remark: |
      "It's seems to be identical to account/status/by (same building blocks).
      It's used by Azure Jenkins pipelines for creating accounts / networks!
      Be aware that Postman automatically cutst '#' so paste value (StatusId) in Params tab (will be automatically url-encoded when saving)
      https://github.com/postmanlabs/postman-app-support/issues/8154ExampleSTATUS#AZURE#1200000024#delascc01-germanywestcentral-testSTATUS%23AZURE%231200000024%delascc01-germanywestcentral-test"
    JIRA:
    GHE:
-
    Testcase ID: STATUS-JENKINS-AZURE-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: STATUS/JENKINS
    Method: GET
    Use case: Get account details from StateTable by StatusId and additional parameters
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/status/jenkins?status-id=STATUS%23AZURE%231200000024%delascc01-germanywestcentral-test&sort-by=CreatedAt&order-by=desc&limit=5
    Body: N/A
    Response: "Get list of filtered records matching Statusid from StateTable. It should only return 5 items in the list"
    Result:
    Remark: |
      "It's seems to be identical to account/status/by (same building blocks).
      It's used by Azure Jenkins pipelines for creating accounts / networks!
      Be aware that Postman automatically cutst '#' so paste value (StatusId) in Params tab (will be automatically url-encoded when saving)
      https://github.com/postmanlabs/postman-app-support/issues/8154ExampleSTATUS#AZURE#1200000024#delascc01-germanywestcentral-testSTATUS%23AZURE%231200000024%delascc01-germanywestcentral-test"
    JIRA:
    GHE:
-
    Testcase ID: STATUS-JENKINS-AZURE-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: STATUS/JENKINS
    Method: GET
    Use case: Get the latest single StatusId for given account
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: Any
    URL: {{baseUrl}}/status/jenkins?status-id=STATUS%23AZURE%231200000024%delascc01-germanywestcentral-test&sort-by=CreatedAt&order-by=desc&limit=1
    Body: N/A
    Response: "Get list of filtered records matching Statusid from StateTable. It should only return 1 item in the list"
    Result:
    Remark: |
      "It's seems to be identical to account/status/by (same building blocks).
      It's used by Azure Jenkins pipelines for creating accounts / networks!Be aware that Postman automatically cutst '#'
      so paste value (StatusId) in Params tab (will be automatically url-encoded when saving)
      https://github.com/postmanlabs/postman-app-support/issues/8154ExampleSTATUS#AZURE#1200000024#delascc01-germanywestcentral-testSTATUS%23AZURE%231200000024%delascc01-germanywestcentral-test"
    JIRA:
    GHE:
-
    Testcase ID: STATUS-JENKINS-AZURE-4
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: STATUS/JENKINS
    Method: POST
    Use case: Creates step records from Azure Jenkins pipeline (e.g. JENKINS_PIPELINE, initial API_CALL and others)
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: Any
    URL: {{baseUrl}}/status/jenkins
    Body: |
        {
          "status": {
            "status-id": "STATUS#AZURE#1200000024#delet213-westeurope-test",
            "status-value": "ACCEPTED",
            "step": "JENKINS_PIPELINE",
            "details": {
              "account-id": "To be created"
            }
          },
          "account-name": "delet213-westeurope-test"
        }
    Response: Status Item
    Result:
    Remark: |
      "We do not need to test it explicitly.
      It's part of account creation (basic, connected) for Azure and called directly from Azure Jenkins pipelines.
      If account creation (basic, connected) is successful, we can consider this as tested."
    JIRA:
    GHE:
-
    Testcase ID: STATUS-SYNC-AZURE-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: SYNC/PROJECT
    Method: POST
    Use case: Sync CosmosDB project to StateTable
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: Any
    URL: {{baseUrl}}/sync/project
    Body: |
        {
          "projects": [
            {
              "id": "de72c384-9b2c-4892-b255-91efb052e6a7",
              "projectName": "A.GR.GR_Allianz Greece Mutual Fund",
              "oecode": "agr4",
              "oename": "Allianz Greece",
              "oeidentifier": "A.GR.GR",
              "owner": "CN=VRA-EU-EUAGR-SERVER-REQUESTERS,OU=User_Groups,OU=Groups,DC=wwg00m,DC=rootdom,DC=net",
              "costcenter": {
                "list": [
                  {
                    "value": "XXXXXXXXXX",
                    "id": "XXXXXXXXXX"
                  }
                ]
              },
              "debtor": {
                "list": [
                  {
                    "value": "2000008979",
                    "id": "2000008979"
                  }
                ]
              },
              "assignmentgroup": {
                "list": [
                  {
                    "value": "A.GR.GR.SRF.CMP",
                    "id": "A.GR.GR.SRF.CMP"
                  }
                ]
              },
              "public": {
                "platform": {
                  "azure": {
                    "location": {
                      "list": [
                        {
                          "value": "westeurope",
                          "id": "West Europe"
                        }
                      ]
                    }
                  },
                  "list": [
                    {
                      "value": "azure",
                      "id": "Azure"
                    },
                    {
                      "value": "aws",
                      "id": "AWS"
                    }
                  ]
                }
              },
              "private": {
                "platform": {
                  "vsphere": {
                    "location": {
                      "list": [
                        {
                          "value": "e2",
                          "id": "Paris"
                        },
                        {
                          "value": "e1",
                          "id": "Frankfurt"
                        }
                      ]
                    }
                  },
                  "list": [
                    {
                      "value": "vsphere",
                      "id": "vSphere"
                    }
                  ]
                }
              }
            }
          ]
        }
    Response: ????
    Result:
    Remark: I have no clue about how is this endpoint being used and what was the purpose of using this.
    JIRA:
    GHE:
-
    Testcase ID: HEALTH-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Any
    Endpoint: HEALTH
    Method: GET
    Use case: Check connectivity to other systems
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: Any
    URL: {{baseUrl}}/health
    Body: N/A
    Response: |
        {
          "type": "HealthCheckContext",
          "run-id": "e1160101-2186-4517-8aee-0b23096a4b78",
          "successful": true,
          "checks": [
            {
              "successful": true,
              "service-id": "vra",
              "details": {
                "status-code": 200,
                "response-time-ms": 1116
              }
            },
            {
              "successful": true,
              "service-id": "cloudhealth",
              "details": {
                "status-code": 200,
                "response-time-ms": 5211
              }
            },
            {
              "successful": true,
              "service-id": "giam",
              "details": {
                "status-code": 200,
                "response-time-ms": 768
              }
            },
            {
              "successful": true,
              "service-id": "prisma",
              "details": {
                "status-code": 200,
                "response-time-ms": 364
              }
            },
            {
              "successful": true,
              "service-id": "github",
              "details": {
                "status-code": 200,
                "response-time-ms": 135
              }
            },
            {
              "successful": true,
              "service-id": "jenkins",
              "details": {
                "status-code": 200,
                "response-time-ms": 17
              }
            }
          ]
        }
    Result:
    Remark: This end point is already covered by other test cases.
    JIRA:
    GHE:
-
    Testcase ID: AZURE-GIAM-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: GIAM/INTEGRATION/REGISTRATION
    Method: POST
    Use case: Request GIAM groups again (for existing or legacy account)
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: Any
    URL: {{baseUrl}}/integration/giam/register?cloud-provider=azure&subscription-id=<delabsc01>
    Body: N/A
    Response: Response from GIAM
    Result:
    Remark: |
      "We do not need to test it explicitly.
      It's part of account creation (basic, connected) for Azure and called automatically when ACCOUNT_CREATION (SUCCESSFUL) occures in DynamoDB stream.
      If account creation (basic, connected) is successful, we need check GIAM integration state machine for result or we can use /status endpoint.
      If notification email about successful account creation is received (it's only when all integrations are successful),
      we could consider this as tested.However, this is an extra trigger to run it for "legacy" accounts that needs to be onboarded to GIAM."
    JIRA:
    GHE:
-
    Testcase ID: AZURE-GIAM-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: GIAM/INTEGRATION/REGISTRATION
    Method: POST
    Use case: Request GIAM groups required for non-existing account
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: Any
    URL: {{baseUrl}}/integration/giam/register?cloud-provider=azure&subscription-id=00000000-0000-0000-0000-000000000000
    Body: N/A
    Response: |
        {
          "code": 409,
          "message": "Provided Account does not exists"
        }
    Result:
    Remark: |
      "We do not need to test it explicitly.
      It's part of account creation (basic, connected) for Azure and called automatically when ACCOUNT_CREATION (SUCCESSFUL) occures in DynamoDB stream.
      If account creation (basic, connected) is successful, we need check GIAM integration state machine for result or we can use /status endpoint.
      If notification email about successful account creation is received (it's only when all integrations are successful),
      we could consider this as tested.However, this is an extra trigger to run it for "legacy" accounts that needs to be onboarded to GIAM."
    JIRA:
    GHE:
-
    Testcase ID: AZURE-GIAM-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: AWS
    Endpoint: GIAM/INTEGRATION/REGISTRATION
    Method: POST
    Use case: Request GIAM groups again (for existing or legacy account)
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: Any
    URL: {{baseUrl}}/integration/giam/register?cloud-provider=aws&account-id=xxxx
    Body: N/A
    Response: Response from GIAM
    Result:
    Remark: |
      "We do not need to test it explicitly.
      It's part of account creation (basic, connected) for Azure and called automatically when ACCOUNT_CREATION (SUCCESSFUL) occures in DynamoDB stream.
      If account creation (basic, connected) is successful, we need check GIAM integration state machine for result or we can use /status endpoint.
      If notification email about successful account creation is received (it's only when all integrations are successful),
      we could consider this as tested.However, this is an extra trigger to run it for "legacy" accounts that needs to be onboarded to GIAM."
    JIRA:
    GHE:
-
    Testcase ID: AWS-GIAM-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: AWS
    Endpoint: GIAM/INTEGRATION/REGISTRATION
    Method: POST
    Use case: Request GIAM groups required for non-existing account
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: Any
    URL: {{baseUrl}}/integration/giam/register?cloud-provider=aws&account-id=000000000000
    Body: N/A
    Response: |
        {
          "code": 409,
          "message": "Provided Account does not exists"
        }
    Result:
    Remark: It's part of account creation (basic, connected)
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-HYBRID-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: HYBRID-SERVICE-CONFIGURATION
    Method: POST
    Use case: Request Classic TUM (Technical User Management) for HC Service scc_test test different assignableScopes
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/hybrid-service-configuration?cloud-provider=azure&account-id=<tumscctest1>&hybrid-service=scc_test
    Body: N/A
    Response: |
        {
            "daytwo": {
                "assignment-type": "attach",
                "actions": {
                    "create-or-update-roles": "/subscriptions/<tumscctest1>/providers/Microsoft.Authorization/roleDefinitions/6ab5545b-d60c-4dac-9a1f-5cb2fe17612f",
                    "attach-roles": "003a7e2e-8853-4be9-8793-3cc05dd37afc"
                }
            },
            "deploy": {
                "assignment-type": "attach",
                "actions": {
                    "create-or-update-roles": "/providers/Microsoft.Authorization/roleDefinitions/8e9309c3-f02a-4c36-8209-17dfbb066bb3",
                    "attach-roles": "84677ab0-e542-4169-890c-b6e14bec3668"
                }
            },
            "monitor": {
                "assignment-type": "attach",
                "actions": {
                    "create-or-update-roles": "/providers/Microsoft.Authorization/roleDefinitions/9213f594-d73f-4a08-ab14-7c54b3c13acf",
                    "attach-roles": "12f0e723-e87e-44e9-bce6-6577e938149e"
                }
            },
            "no-errors": true,
            "valid-till": "Tue Jun 20 09:54:27 2023"
        }
    Result:
    Remark: |
        We are having multiple possibilities of how assignableScopes can be structured, possible situations are:
        - one management group
        - one management group and subscription from this group
        - only subscriptions
        hybrid-scc_test contains all of those combinations see:
        https://github.developer.allianz.io/CloudTribe/hybrid-scc_test/tree/master/TechnicalUserManagement/Azure
        Subscription (<tumscctest1>) -> Access Control (IAM) -> Role Assignments:
        scc_test_{deploy,daytwo,monitor}_roles should be assigned now with policies as in repo above
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-HYBRID-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: HYBRID-SERVICE-CONFIGURATION
    Method: POST
    Use case: Request Classic TUM (Technical User Management) for HC Service scc_test test bad subscription scope
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/hybrid-service-configuration?cloud-provider=azure&account-id=<tumscctest3>&hybrid-service=scc_test
    Body: N/A
    Response: |
        {
            "message": "(AssignableScopeMismatch) The request to create the roleDefinition '6ab5545b-d60c-4dac-9a1f-5cb2fe17612f' is not valid.
            At least one of the scopes that are available for assignment must be within the request scope '/subscriptions/<tumscctest3>'.
            Code: AssignableScopeMismatch
            Message: The request to create the roleDefinition '6ab5545b-d60c-4dac-9a1f-5cb2fe17612f' is not valid.
            At least one of the scopes that are available for assignment must be within the request scope '/subscriptions/<tumscctest3>'.",
            "code": 500
        }
    Result:
    Remark: |
        In hybrid-scc_test repo there is no policy which contains scope /subscription/<tumscctest3>.
        Nothing should be created, error in response should be rised
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-HYBRID-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: HYBRID-SERVICE-CONFIGURATION
    Method: DELETE
    Use case: Remove Classic TUM (Technical User Management) assignments for HC Service for hybrid-scc_test repo
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{base-url}}/hybrid-service-configuration?cloud-provider=azure&account-id=<tumscctest1>&hybrid-service=scc_test
    Body: N/A
    Response: |
        {
            "daytwo": {
                "assignment-type": "detach",
                "actions": {
                    "detach-policy": "/subscriptions/<tumscctest1>/providers/Microsoft.Authorization/roleDefinitions/6ab5545b-d60c-4dac-9a1f-5cb2fe17612f"
                }
            },
            "deploy": {
                "assignment-type": "detach",
                "actions": {
                    "detach-policy": "/subscriptions/<tumscctest1>/providers/Microsoft.Authorization/roleDefinitions/8e9309c3-f02a-4c36-8209-17dfbb066bb3"
                }
            },
            "monitor": {
                "assignment-type": "detach",
                "actions": {
                    "detach-policy": "/subscriptions/<tumscctest1>/providers/Microsoft.Authorization/roleDefinitions/9213f594-d73f-4a08-ab14-7c54b3c13acf"
                }
            }
        }
    Result:
    Remark: |
        You can check directly in Azure portal
        Subscription (<tumscctest1>) -> Access Control (IAM) -> Role Assignments:
        no scc_test_{deploy,daytwo,monitor}_roles should be assigned now
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-HYBRID-4
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: HYBRID-SERVICE-CONFIGURATION
    Method: POST
    Use case: Request Classic TUM (Technical User Management) for HC Service (e.q. mssql, backup) with default TTL
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/hybrid-service-configuration?cloud-provider=azure&hybrid-service=mssql&account-id=<delabsc01>
    Body: N/A
    Response: |
        {
          "daytwo": {
            "assignment-type": "attach",
            "actions": {
              "create-or-update-roles": "/providers/Microsoft.Authorization/roleDefinitions/92fb3170-d776-4688-9004-3736ca6eab2f",
              "attach-roles": "2c057f80-c40b-44d9-b84f-6fa936a3afd3"
            }
          },
          "deploy": {
            "assignment-type": "attach",
            "actions": {
              "create-or-update-roles": "/providers/Microsoft.Authorization/roleDefinitions/b2f62284-c73c-48d0-b4fe-0bdd3cad7911",
              "attach-roles": "f16fbf50-e506-42ba-a879-f8be16d440e4"
            }
          },
          "monitor": {
            "assignment-type": "attach",
            "actions": {
              "create-or-update-roles": "/providers/Microsoft.Authorization/roleDefinitions/c608c40e-56e8-4045-8bf3-d3de8ff58ffe",
              "attach-roles": "2bab4d40-53d8-426c-80c8-8a2f78d3ecb8"
            }
          },
          "no-errors": true,
          "valid-till": "Mon Sep  5 10:37:45 2022"
        }
    Result:
    Remark: |
      "The default is 120 minutes or what is specified in config.json, config.staging.json in HC repository.
      example: https://github.developer.allianz.io/CloudTribe/hybrid-mssql/tree/master/TechnicalUserManagement
      After this period the corresponding SP for HC services is removed from custom role in subscription.
      The returned valid-till time is in UTC.You can remove the SP's from roles by calling DELETE method (see below)
      You can check directly in Azure portal (console) - betterSubscription -> Access Control (IAM) ->
      Role Assignments:mssql_deploy_role => SP_mssql_deploymssql_daytwo_role =>  SP_mssql_daytwomssql_monitor_role =>
      SP_mssql_monitoror you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-HYBRID-5
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: HYBRID-SERVICE-CONFIGURATION
    Method: POST
    Use case: Request Classic TUM (Technical User Management) for HC Service (e.q. mssql,backup) with custom TTL (in minutes)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/hybrid-service-configuration?cloud-provider=azure&hybrid-service=mssql&account-id=<delabsc01>&ttl=3
    Body: N/A
    Response: |
        {
          "daytwo": {
            "assignment-type": "attach",
            "actions": {
              "create-or-update-roles": "/providers/Microsoft.Authorization/roleDefinitions/92fb3170-d776-4688-9004-3736ca6eab2f",
              "attach-roles": "2c057f80-c40b-44d9-b84f-6fa936a3afd3"
            }
          },
          "deploy": {
            "assignment-type": "attach",
            "actions": {
              "create-or-update-roles": "/providers/Microsoft.Authorization/roleDefinitions/b2f62284-c73c-48d0-b4fe-0bdd3cad7911",
              "attach-roles": "f16fbf50-e506-42ba-a879-f8be16d440e4"
            }
          },
          "monitor": {
            "assignment-type": "attach",
            "actions": {
              "create-or-update-roles": "/providers/Microsoft.Authorization/roleDefinitions/c608c40e-56e8-4045-8bf3-d3de8ff58ffe",
              "attach-roles": "2bab4d40-53d8-426c-80c8-8a2f78d3ecb8"
            }
          },
          "no-errors": true,
          "valid-till": "Mon Sep  5 10:39:04 2022"
        }
    Result:
    Remark: |
      "The default is overwritten with specified value in TTL parameter.
      After this period the corresponding SP for HC services is removed from custom role in subscription.
      The returned valid-till time is in UTC.Check in subscription that SP were assigned to custom roles and also removed after TTL expiration.
      You can check directly in Azure portal (console) - betterSubscription -> Access Control (IAM) ->
      Role Assignments:mssql_deploy_role => SP_mssql_deploymssql_daytwo_role =>  SP_mssql_daytwomssql_monitor_role => SP_mssql_monitoror
      you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-HYBRID-6
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: HYBRID-SERVICE-CONFIGURATION
    Method: POST
    Use case: Request Classic TUM (Technical User Management) for HC Service (e.q. mssql,backup) with custom TTL (in minutes) again
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/hybrid-service-configuration?cloud-provider=azure&hybrid-service=mssql&account-id=<delabsc01>&ttl=3
    Body: N/A
    Response: |
        {
          "daytwo": {
            "assignment-type": "attach",
            "actions": {
              "create-or-update-roles": "/providers/Microsoft.Authorization/roleDefinitions/92fb3170-d776-4688-9004-3736ca6eab2f",
              "attach-roles": "2c057f80-c40b-44d9-b84f-6fa936a3afd3"
            }
          },
          "deploy": {
            "assignment-type": "attach",
            "actions": {
              "create-or-update-roles": "/providers/Microsoft.Authorization/roleDefinitions/b2f62284-c73c-48d0-b4fe-0bdd3cad7911",
              "attach-roles": "f16fbf50-e506-42ba-a879-f8be16d440e4"
            }
          },
          "monitor": {
            "assignment-type": "attach",
            "actions": {
              "create-or-update-roles": "/providers/Microsoft.Authorization/roleDefinitions/c608c40e-56e8-4045-8bf3-d3de8ff58ffe",
              "attach-roles": "2bab4d40-53d8-426c-80c8-8a2f78d3ecb8"
            }
          },
          "no-errors": true,
          "valid-till": "Mon Sep  5 10:42:11 2022"
        }
    Result:
    Remark: |
      "The default is overwritten with specified value in TTL parameter.
      If custom role was already assigned to HC SP, the TTL is updated and valid-till extended by that value.
      After this period the corresponding SP for HC services is removed from custom role in subscription.
      The returned valid-till time is in UTC.Check in subscription that SP were assigned to custom roles and also removed after TTL expiration.
      You can check directly in Azure portal (console) - betterSubscription -> Access Control (IAM) -> Role Assignments:mssql_deploy_role =>
      SP_mssql_deploymssql_daytwo_role =>  SP_mssql_daytwomssql_monitor_role =>  SP_mssql_monitoror
      you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-HYBRID-7
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: HYBRID-SERVICE-CONFIGURATION
    Method: POST
    Use case: Request Classic TUM (Technical User Management) for HC Service (e.q. mssql, backup) with non-existing account-id
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/hybrid-service-configuration?cloud-provider=azure&account-id=<tumscctest3>&hybrid-service=scc_test
    Body: N/A
    Response: |
        {
          "message": "(SubscriptionNotFound) The subscription '00000000-0000-0000-0000-000000000000' could not be found.Code: SubscriptionNotFoundMessage: The subscription '00000000-0000-0000-0000-000000000000' could not be found.",
          "code": 500
        }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-HYBRID-8
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: HYBRID-SERVICE-CONFIGURATION
    Method: POST
    Use case: Request Classic TUM (Technical User Management) for wrong HC Service (e.q. abcd)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/hybrid-service-configuration?cloud-provider=azure&hybrid-service=abcd&account-id=00000000-0000-0000-0000-000000000000
    Body: N/A
    Response: |
        {
          "message": "Validation error: [{'message': "'abcd' is not one of ['adp', 'hc_linux', 'hc_windows', 'postgres', 'mssql', 'abs', 'sftp', 'encryptionOracle', 'encryptionNoOracle', 'oracle', 'objectStorage', 'blockStorage', 'crp.tomcat', 'crp.jboss', 'backup', 'it-master-platform', 'SharedFileStorage', 'mongoDB', 'cpam']", 'schema': {'type': 'string', 'enum': ['adp', 'hc_linux', 'hc_windows', 'postgres', 'mssql', 'abs', 'sftp', 'encryptionOracle', 'encryptionNoOracle', 'oracle', 'objectStorage', 'blockStorage', 'crp.tomcat', 'crp.jboss', 'backup', 'it-master-platform', 'SharedFileStorage', 'mongoDB', 'cpam']}, 'cause': None, 'instance': 'abcd'}]",
          "code": 406
        }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-HYBRID-9
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: HYBRID-SERVICE-CONFIGURATION
    Method: DELETE
    Use case: Remove Classic TUM (Technical User Management) assignments for HC Service (e.q. mssql, backup)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/hybrid-service-configuration?cloud-provider=azure&hybrid-service=mssql&account-id=<delabsc01>
    Body: N/A
    Response: |
          {
            "daytwo": {
              "assignment-type": "detach",
              "actions": {
                "detach-policy": "/subscriptions/d936735b-349e-4d93-84e2-a82eed16fd7a/providers/Microsoft.Authorization/roleDefinitions/92fb3170-d776-4688-9004-3736ca6eab2f"
              }
            },
            "deploy": {
              "assignment-type": "detach",
              "actions": {
                "detach-policy": "/subscriptions/d936735b-349e-4d93-84e2-a82eed16fd7a/providers/Microsoft.Authorization/roleDefinitions/b2f62284-c73c-48d0-b4fe-0bdd3cad7911"
              }
            },
            "monitor": {
              "assignment-type": "detach",
              "actions": {
                "detach-policy": "/subscriptions/d936735b-349e-4d93-84e2-a82eed16fd7a/providers/Microsoft.Authorization/roleDefinitions/c608c40e-56e8-4045-8bf3-d3de8ff58ffe"
              }
            }
          }
    Result:
    Remark: |
      "You can check directly in Azure portal (console) - betterSubscription -> Access Control (IAM) ->
      Role Assignments:no mssql_{deploy,daytwo,monitor}_roles should be assigned now or
      you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-HYBRID-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: HYBRID-SERVICE-CONFIGURATION
    Method: POST
    Use case: Request Classic TUM (Technical User Management) for HC Service (e.q. mssql, backup) with default TTL
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/hybrid-service-configuration?cloud-provider=aws&hybrid-service=backup&account-id=<delwbsc01>
    Body: N/A
    Response: |
            {
              "monitor": {
                "backup-monitor-role": {
                  "actions": {
                    "create-policies": [
                      "arn:aws:iam::650818633299:policy/backup_monitor_role"
                    ],
                    "create-roles": [
                      "arn:aws:iam::650818633299:role/backup_monitor_role"
                    ],
                    "attach-roles": [
                      "arn:aws:iam::650818633299:policy/backup_monitor_role"
                    ],
                    "create-admin-roles": [
                      "arn:aws:iam::624836204311:role/backup_monitor_role"
                    ]
                  }
                },
                "new-relic-infrastructure": {
                  "actions": {
                    "create-managed-roles": [
                      "arn:aws:iam::650818633299:role/NewRelicInfrastructure"
                    ],
                    "managed-policies-assignment": [
                      "arn:aws:iam::aws:policy/ReadOnlyAccess"
                    ]
                  }
                }
              },
              "deploy": {
                "backup-deploy-role": {
                  "actions": {
                    "create-policies": [
                      "arn:aws:iam::650818633299:policy/backup_deploy_role"
                    ],
                    "create-roles": [
                      "arn:aws:iam::650818633299:role/backup_deploy_role"
                    ],
                    "attach-roles": [
                      "arn:aws:iam::650818633299:policy/backup_deploy_role"
                    ],
                    "create-admin-roles": [
                      "arn:aws:iam::624836204311:role/backup_deploy_role"
                    ]
                  }
                }
              },
              "daytwo": {
                "backup-daytwo-role": {
                  "actions": {
                    "create-policies": [
                      "arn:aws:iam::650818633299:policy/backup_daytwo_role"
                    ],
                    "create-roles": [
                      "arn:aws:iam::650818633299:role/backup_daytwo_role"
                    ],
                    "attach-roles": [
                      "arn:aws:iam::650818633299:policy/backup_daytwo_role"
                    ],
                    "create-admin-roles": [
                      "arn:aws:iam::624836204311:role/backup_daytwo_role"
                    ]
                  }
                }
              },
              "no-errors": true,
              "valid-till": "Mon Sep  5 11:27:14 2022"
            }
    Result:
    Remark: |
      "The default is 120 minutes or what is specified in config.json, config.staging.json in HC repository.
      example: https://github.developer.allianz.io/CloudTribe/hybrid-backup/tree/master/TechnicalUserManagementAfter
      this period the corresponding SP for HC services is removed from custom role in subscription.
      The returned valid-till time is in UTC.You can remove the SP's from roles by calling DELETE method (see below)You can check directly in
      AWS console - betterSwitch role:  <account-tag>-<shortenv>-<projecthash>-infraadmin-assumerole | <accountId>Example: delwbsc01-t--FWlwLoh3qc-infraadmin-assumerole | 650818633299Account -> IAM -> Roles:backup_deploy_role => backup_deploy_role (policy)backup_daytwo_role => backup_daytwo_role (policy)backup_monitor_role => backup_monitor_role (policy)or you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-HYBRID-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: HYBRID-SERVICE-CONFIGURATION
    Method: POST
    Use case: Request Classic TUM (Technical User Management) for HC Service (e.q. mssql,backup) with custom TTL (in minutes)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/hybrid-service-configuration?cloud-provider=aws&hybrid-service=backup&account-id=<delwbsc01>&ttl=3
    Body: N/A
    Response: |
            {
              "monitor": {
                "backup-monitor-role": {
                  "actions": {
                    "create-policies": [
                      "arn:aws:iam::650818633299:policy/backup_monitor_role"
                    ],
                    "create-roles": [
                      "http_status(200)"
                    ],
                    "attach-roles": [
                      "arn:aws:iam::650818633299:policy/backup_monitor_role"
                    ],
                    "create-admin-roles": [
                      "arn:aws:iam::624836204311:role/backup_monitor_role"
                    ]
                  }
                },
                "new-relic-infrastructure": {
                  "actions": {
                    "create-managed-roles": [
                      "http_status(200)"
                    ],
                    "managed-policies-assignment": [
                      "arn:aws:iam::aws:policy/ReadOnlyAccess"
                    ]
                  }
                }
              },
              "deploy": {
                "backup-deploy-role": {
                  "actions": {
                    "create-policies": [
                      "arn:aws:iam::650818633299:policy/backup_deploy_role"
                    ],
                    "create-roles": [
                      "http_status(200)"
                    ],
                    "attach-roles": [
                      "arn:aws:iam::650818633299:policy/backup_deploy_role"
                    ],
                    "create-admin-roles": [
                      "arn:aws:iam::624836204311:role/backup_deploy_role"
                    ]
                  }
                }
              },
              "daytwo": {
                "backup-daytwo-role": {
                  "actions": {
                    "create-policies": [
                      "arn:aws:iam::650818633299:policy/backup_daytwo_role"
                    ],
                    "create-roles": [
                      "http_status(200)"
                    ],
                    "attach-roles": [
                      "arn:aws:iam::650818633299:policy/backup_daytwo_role"
                    ],
                    "create-admin-roles": [
                      "arn:aws:iam::624836204311:role/backup_daytwo_role"
                    ]
                  }
                }
              },
              "no-errors": true,
              "valid-till": "Mon Sep  5 11:37:12 2022"
            }
    Result:
    Remark: |
      "The default is overwritten with specified value in TTL parameter.
      After this period the corresponding SP for HC services is removed from custom role in subscription.
      The returned valid-till time is in UTC.Check in subscription that SP were assigned to custom roles and also removed after TTL expiration.
      You can check directly in AWS console - betterSwitch role:  <account-tag>-<shortenv>-<projecthash>-infraadmin-assumerole |
      <accountId>Example: delwbsc01-t--FWlwLoh3qc-infraadmin-assumerole | 650818633299Account -> IAM ->
      Roles:backup_deploy_role => backup_deploy_role (policy)backup_daytwo_role => backup_daytwo_role (policy)backup_monitor_role => backup_monitor_role (policy)
      or you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-HYBRID-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: HYBRID-SERVICE-CONFIGURATION
    Method: POST
    Use case: Request Classic TUM (Technical User Management) for HC Service (e.q. mssql,backup) with custom TTL (in minutes) again
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/hybrid-service-configuration?cloud-provider=aws&hybrid-service=backup&account-id=<delwbsc01>&ttl=3
    Body: N/A
    Response: |
            {
              "monitor": {
                "backup-monitor-role": {
                  "actions": {
                    "create-policies": [
                      "arn:aws:iam::650818633299:policy/backup_monitor_role"
                    ],
                    "create-roles": [
                      "http_status(200)"
                    ],
                    "attach-roles": [
                      "arn:aws:iam::650818633299:policy/backup_monitor_role"
                    ],
                    "create-admin-roles": [
                      "arn:aws:iam::624836204311:role/backup_monitor_role"
                    ]
                  }
                },
                "new-relic-infrastructure": {
                  "actions": {
                    "create-managed-roles": [
                      "http_status(200)"
                    ],
                    "managed-policies-assignment": [
                      "arn:aws:iam::aws:policy/ReadOnlyAccess"
                    ]
                  }
                }
              },
              "deploy": {
                "backup-deploy-role": {
                  "actions": {
                    "create-policies": [
                      "arn:aws:iam::650818633299:policy/backup_deploy_role"
                    ],
                    "create-roles": [
                      "http_status(200)"
                    ],
                    "attach-roles": [
                      "arn:aws:iam::650818633299:policy/backup_deploy_role"
                    ],
                    "create-admin-roles": [
                      "arn:aws:iam::624836204311:role/backup_deploy_role"
                    ]
                  }
                }
              },
              "daytwo": {
                "backup-daytwo-role": {
                  "actions": {
                    "create-policies": [
                      "arn:aws:iam::650818633299:policy/backup_daytwo_role"
                    ],
                    "create-roles": [
                      "http_status(200)"
                    ],
                    "attach-roles": [
                      "arn:aws:iam::650818633299:policy/backup_daytwo_role"
                    ],
                    "create-admin-roles": [
                      "arn:aws:iam::624836204311:role/backup_daytwo_role"
                    ]
                  }
                }
              },
              "no-errors": true,
              "valid-till": "Mon Sep  5 11:43:54 2022"
            }
    Result:
    Remark: |
      "The default is overwritten with specified value in TTL parameter.
      If custom role was already assigned to HC SP, the TTL is updated and valid-till extended by that value.
      After this period the corresponding SP for HC services is removed from custom role in subscription.
      The returned valid-till time is in UTC.Check in subscription that SP were assigned to custom roles and also removed after TTL expiration.
      You can check directly in AWS console - betterSwitch role:  <account-tag>-<shortenv>-<projecthash>-infraadmin-assumerole |
      <accountId>Example: delwbsc01-t--FWlwLoh3qc-infraadmin-assumerole | 650818633299Account -> IAM -> Roles:backup_deploy_role =>
      backup_deploy_role (policy)backup_daytwo_role => backup_daytwo_role (policy)backup_monitor_role => backup_monitor_role (policy)
      or you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-HYBRID-4
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: HYBRID-SERVICE-CONFIGURATION
    Method: POST
    Use case: Request Classic TUM (Technical User Management) for HC Service (e.q. mssql, backup) with non-existing account-id
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/hybrid-service-configuration?cloud-provider=aws&hybrid-service=backup&account-id=000000000000
    Body: N/A
    Response: |
        {
          "code": 400,
          "message": "'AccessDenied'"
        }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-HYBRID-5
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: HYBRID-SERVICE-CONFIGURATION
    Method: POST
    Use case: Request Classic TUM (Technical User Management) for wrong HC Service (e.q. abcd)
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/hybrid-service-configuration?cloud-provider=aws&hybrid-service=abcd&account-id=000000000000
    Body: N/A
    Response: |
        {
          "message": "Validation error: [{'message': "'abcd' is not one of ['adp', 'hc_linux', 'hc_windows', 'postgres', 'mssql', 'abs', 'sftp', 'encryptionOracle', 'encryptionNoOracle', 'oracle', 'objectStorage', 'blockStorage', 'crp.tomcat', 'crp.jboss', 'backup', 'it-master-platform', 'SharedFileStorage', 'mongoDB', 'cpam']", 'schema': {'type': 'string', 'enum': ['adp', 'hc_linux', 'hc_windows', 'postgres', 'mssql', 'abs', 'sftp', 'encryptionOracle', 'encryptionNoOracle', 'oracle', 'objectStorage', 'blockStorage', 'crp.tomcat', 'crp.jboss', 'backup', 'it-master-platform', 'SharedFileStorage', 'mongoDB', 'cpam']}, 'cause': None, 'instance': 'abcd'}]",
          "code": 406
        }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-HYBRID-6
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: HYBRID-SERVICE-CONFIGURATION
    Method: DELETE
    Use case: Remove Classic TUM (Technical User Management) assignments for HC Service (e.q. mssql, backup)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/hybrid-service-configuration?cloud-provider=aws&hybrid-service=backup&account-id=<delwbsc01>
    Body: N/A
    Response: |
        {
          "daytwo": {
            "assignment-type": "detach",
            "actions": {
              "detach-policy": "arn:aws:iam::650818633299:policy/backup_daytwo_role"
            }
          },
          "deploy": {
            "assignment-type": "detach",
            "actions": {
              "detach-policy": "arn:aws:iam::650818633299:policy/backup_deploy_role"
            }
          },
          "monitor": {
            "assignment-type": "detach",
            "actions": {
              "detach-policy": "arn:aws:iam::650818633299:policy/backup_monitor_role"
            }
          }
        }
    Result:
    Remark: |
      "You can check directly in AWS console - betterSwitch role:  <account-tag>-<shortenv>-<projecthash>-infraadmin-assumerole |
      <accountId>Example: delwbsc01-t--FWlwLoh3qc-infraadmin-assumerole | 650818633299Account -> IAM -> Roles:backup_deploy_role => no policy assignedbackup_daytwo_role =>
      no policy assignedbackup_monitor_role => no policy assignedor you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-HYBRID-7
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: HYBRID-SERVICE-CONFIGURATION
    Method: POST
    Use case: Request Classic TUM (Technical User Management) for HC Service (e.q. mssql, backup) with default TTL and verify caching
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Any
    Service type: SCC
    URL: {{baseUrl}}/hybrid-service-configuration?cloud-provider=aws&hybrid-service=backup&account-id=<delwbsc01>&ttl=15
    Body: N/A
    Response: |
      {
          "daytwo": {
              "hybrid-service-role": {
                  "actions": {
                      "create-policies": [
                          "arn:aws:iam::814967015901:policy/hc_linux_daytwo_role"
                      ],
                      "create-roles": [
                          "http_status(200)"
                      ],
                      "attach-roles": [
                          "arn:aws:iam::814967015901:policy/hc_linux_daytwo_role"
                      ],
                      "create-admin-roles": [
                          "arn:aws:iam::624836204311:role/hc_linux_daytwo_role"
                      ]
                  }
              }
          },
          "deploy": {
              "hybrid-service-role": {
                  "actions": {
                      "create-policies": [
                          "arn:aws:iam::814967015901:policy/hc_linux_deploy_role"
                      ],
                      "create-roles": [
                          "http_status(200)"
                      ],
                      "attach-roles": [
                          "arn:aws:iam::814967015901:policy/hc_linux_deploy_role"
                      ],
                      "create-admin-roles": [
                          "arn:aws:iam::624836204311:role/hc_linux_deploy_role"
                      ]
                  }
              }
          },
          "monitor": {
              "hybrid-service-role": {
                  "actions": {
                      "create-policies": [
                          "arn:aws:iam::814967015901:policy/hc_linux_monitor_role"
                      ],
                      "create-roles": [
                          "http_status(200)"
                      ],
                      "attach-roles": [
                          "arn:aws:iam::814967015901:policy/hc_linux_monitor_role"
                      ],
                      "create-admin-roles": [
                          "arn:aws:iam::624836204311:role/hc_linux_monitor_role"
                      ]
                  }
              },
              "new-relic-infrastructure": {
                  "actions": {
                      "create-managed-roles": [
                          "http_status(200)"
                      ],
                      "managed-policies-assignment": [
                          "arn:aws:iam::aws:policy/ReadOnlyAccess"
                      ]
                  }
              }
          },
          "no-errors": true,
          "valid-till": "Thu Oct 12 13:08:43 2023"
      }
    Result:
    Remark: |
      We need to verify caching (memoization) of assume role / STS assume role.

      Make sure that STS_ASSUME_ROLE_DURATION_SECONDS in AppConfig is set to 900 (15 minutes).
      Make 1st call to /hybrid-service-configuration with TTL=15.
      Wait 5 minutes and make 2nd call (same params).
      Wait 5 minutes and make 3rd call (same params).

      Now, on exactly 15th minute, we want to make more repeated calls to test cache invalidation properly.
      So, wait 5 minutes and make 5 more calls (same params) in a row.

      Better, we would be to have 2 accounts to make calls in parallel on 15th minute.
    JIRA: FCP-15920
    GHE: https://github.developer.allianz.io/CloudTribe/scc-api/pull/1206
-
    Testcase ID: SCC-AZURE-VRA-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: Request VRA TUM (Technical User Management) for HC Service scc_test daytwo role
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=azure&account-id=<tumscctest1>
    Body: |
        {
            "service-id": "scc_test",
            "role-assignment-type": "attach",
            "operation-type": "daytwo"
        }
    Response: |
        {
            "daytwo": {
                "assignment-type": "attach",
                "actions": {
                    "create-or-update-roles": "/subscriptions/<tumscctest1>/providers/Microsoft.Authorization/roleDefinitions/6ab5545b-d60c-4dac-9a1f-5cb2fe17612f",
                    "attach-roles": "00b64448-7423-4761-8d57-95549fef3592"
                }
            },
            "no-errors": true
        }
    Result:
    Remark: |
      This only works for SCC Connected accounts. In subscription <tumscctest1>
      in IAM -> role assignments under scc_test_daytwo_role you should have VRA SP assigned
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-VRA-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: Request VRA TUM (Technical User Management) for HC Service scc_test deploy role
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=azure&account-id=<tumscctest1>
    Body: |
        {
            "service-id": "scc_test",
            "role-assignment-type": "attach",
            "operation-type": "deploy"
        }
    Response: |
        {
            "deploy": {
                "assignment-type": "attach",
                "actions": {
                    "create-or-update-roles": "/providers/Microsoft.Authorization/roleDefinitions/8e9309c3-f02a-4c36-8209-17dfbb066bb3",
                    "attach-roles": "00b64448-7423-4761-8d57-95549fef3592"
                }
            },
            "no-errors": true
        }
    Result:
    Remark: |
      This only works for SCC Connected accounts. In subscription <tumscctest1>
      in IAM -> role assignments under scc_test_deploy_role you should have VRA SP assigned
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-VRA-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: DELETE
    Use case: Request VRA TUM (Technical User Management) for HC Service scc_test detach roles role
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=azure&account-id=<tumscctest1>
    Body: |
        {
            "service-id": "scc_test"
        }
    Response: |
        {
            "daytwo": {
                "assignment-type": "detach",
                "actions": {
                    "detach-policy": "/subscriptions/<tumscctest1>/providers/Microsoft.Authorization/roleDefinitions/6ab5545b-d60c-4dac-9a1f-5cb2fe17612f"
                }
            },
            "deploy": {
                "assignment-type": "detach",
                "actions": {
                    "detach-policy": "/subscriptions/<tumscctest1>/providers/Microsoft.Authorization/roleDefinitions/8e9309c3-f02a-4c36-8209-17dfbb066bb3"
                }
            },
            "no-errors": true
        }
    Result:
    Remark: |
      This only works for SCC Connected accounts. In subscription <tumscctest1>
      in IAM -> role assignments there should be no VRA SP assigned
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-VRA-4
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: Request VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup)
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=azure&account-id=<delabsc01>
    Body: |
        {
          "service-id": "mssql",
          "role-assignment-type": "attach",
          "operation-type": "deploy"
        }
    Response: |
        {
          "code": 412,
          "message": "The <delabsc01> is not in the connected_accounts mgmt group!"
        }
    Result:
    Remark: This only works for SCC Connected accounts.
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-VRA-5
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: "Request VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup)Invalid HC service name"
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=azure&account-id=<delabsc01>
    Body: |
        {
          "service-id": "abcd",
          "role-assignment-type": "attach",
          "operation-type": "deploy"
        }
    Response: |
        {
          "message": "Validation error: [{'message': "'abcd' is not one of ['adp', 'hc_linux', 'hc_windows', 'postgres', 'mssql', 'abs', 'sftp', 'encryptionOracle', 'encryptionNoOracle', 'oracle', 'objectStorage', 'blockStorage', 'crp.tomcat', 'crp.jboss', 'backup', 'it-master-platform', 'SharedFileStorage', 'mongoDB', 'cpam']", 'schema': {'type': 'string', 'enum': ['adp', 'hc_linux', 'hc_windows', 'postgres', 'mssql', 'abs', 'sftp', 'encryptionOracle', 'encryptionNoOracle', 'oracle', 'objectStorage', 'blockStorage', 'crp.tomcat', 'crp.jboss', 'backup', 'it-master-platform', 'SharedFileStorage', 'mongoDB', 'cpam']}, 'cause': None, 'instance': 'abcd'}]",
          "code": 406
        }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-VRA-6
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: "Request VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup)Invalid role-assignment-type"
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=azure&account-id=<delascc01>
    Body: |
        {
          "service-id": "mssql",
          "role-assignment-type": "abcd",
          "operation-type": "deploy"
        }
    Response: |
        {
          "message": "Validation error: [{'message': "'abcd' is not one of ['attach', 'detach']", 'schema': {'type': 'string', 'enum': ['attach', 'detach']}, 'cause': None, 'instance': 'abcd'}]",
          "code": 406
        }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-VRA-7
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: "Request VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup)Invalid operation-type"
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=azure&account-id=<delascc01>
    Body: |
        {
          "service-id": "mssql",
          "role-assignment-type": "attach",
          "operation-type": "abcd"
        }
    Response: |
        {
          "message": "Validation error: [{'message': "'abcd' is not one of ['deploy', 'daytwo', 'monitor']", 'schema': {'type': 'string', 'enum': ['deploy', 'daytwo', 'monitor']}, 'cause': None, 'instance': 'abcd'}]",
          "code": 406
        }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-VRA-8
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: Request VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup) operation-type deploy
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=azure&account-id=<delascc01>
    Body: |
        {
          "service-id": "mssql",
          "role-assignment-type": "attach",
          "operation-type": "deploy"
        }
    Response: |
        {
          "deploy": {
            "assignment-type": "attach",
            "actions": {
              "create-or-update-roles": "/providers/Microsoft.Authorization/roleDefinitions/b2f62284-c73c-48d0-b4fe-0bdd3cad7911",
              "attach-roles": "9935e3c1-4fc2-4a8a-9783-7f75d153623f"
            }
          },
          "no-errors": true
        }
    Result:
    Remark: |
      "Role definitions updated from repositoryexample: https://github.developer.allianz.io/CloudTribe/hybrid-mssql/tree/master/TechnicalUserManagement
      No TTL aplied here. It stays assigned until it's explicitly detached.You can check directly in Azure portal (console) - betterSubscription ->
      Access Control (IAM) -> Role Assignments:mssql_deploy_role => sp-vra8-<delascc01>or you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-VRA-9
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: Remove VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup) operation-type deploy
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=azure&account-id=<delascc01>
    Body: |
        {
          "service-id": "mssql",
          "role-assignment-type": "detach",
          "operation-type": "deploy"
        }
    Response: |
        {
          "deploy": {
            "assignment-type": "detach",
            "actions": {
              "detach-policy": "/subscriptions/7de0a990-3ef3-4f9b-9fa9-4f8c01c27108/providers/Microsoft.Authorization/roleDefinitions/b2f62284-c73c-48d0-b4fe-0bdd3cad7911"
            }
          },
          "no-errors": true
        }
    Result:
    Remark: |
      "The sp-vra8-<delascc01> is unassigned from mssql_deploy_role
      You can check directly in Azure portal (console) - betterSubscription -> Access Control (IAM) ->
      Role Assignments:No user assignment existsor you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-VRA-10
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: Request VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup) operation-type daytwo
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=azure&account-id=<delascc01>
    Body: |
        {
          "service-id": "mssql",
          "role-assignment-type": "attach",
          "operation-type": "daytwo"
        }
    Response: |
        {
          "deploy": {
            "assignment-type": "attach",
            "actions": {
              "create-or-update-roles": "/providers/Microsoft.Authorization/roleDefinitions/b2f62284-c73c-48d0-b4fe-0bdd3cad7911",
              "attach-roles": "9935e3c1-4fc2-4a8a-9783-7f75d153623f"
            }
          },
          "no-errors": true
        }
    Result:
    Remark: |
      "Role definitions updated from repositoryexample: https://github.developer.allianz.io/CloudTribe/hybrid-mssql/tree/master/TechnicalUserManagement
      No TTL aplied here. It stays assigned until it's explicitly detached.You can check directly in Azure portal (console) - betterSubscription -> Access Control (IAM) ->
      Role Assignments:mssql_daytwo_role => sp-vra8-<delascc01>or you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-VRA-11
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: Remove VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup) operation-type daytwo
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=azure&account-id=<delascc01>
    Body: |
        {
          "service-id": "mssql",
          "role-assignment-type": "detach",
          "operation-type": "daytwo"
        }
    Response: |
        {
          "deploy": {
            "assignment-type": "detach",
            "actions": {
              "detach-policy": "/subscriptions/7de0a990-3ef3-4f9b-9fa9-4f8c01c27108/providers/Microsoft.Authorization/roleDefinitions/b2f62284-c73c-48d0-b4fe-0bdd3cad7911"
            }
          },
          "no-errors": true
        }
    Result:
    Remark: |
      "The sp-vra8-<delascc01> is unassigned from mssql_deploy_role
      You can check directly in Azure portal (console) - betterSubscription -> Access Control (IAM) ->
      Role Assignments:No user assignment existsor you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-VRA-12
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: Request VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup) operation-type monitor
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=azure&account-id=<delascc01>
    Body: |
        {
          "service-id": "mssql",
          "role-assignment-type": "attach",
          "operation-type": "monitor"
        }
    Response: |
        {
          "deploy": {
            "assignment-type": "attach",
            "actions": {
              "create-or-update-roles": "/providers/Microsoft.Authorization/roleDefinitions/b2f62284-c73c-48d0-b4fe-0bdd3cad7911",
              "attach-roles": "9935e3c1-4fc2-4a8a-9783-7f75d153623f"
            }
          },
          "no-errors": true
        }
    Result:
    Remark: |
      "Role definitions updated from repositoryexample: https://github.developer.allianz.io/CloudTribe/hybrid-mssql/tree/master/TechnicalUserManagement
      No TTL aplied here. It stays assigned until it's explicitly detached.You can check directly in Azure portal (console) - betterSubscription -> Access Control (IAM) ->
      Role Assignments:mssql_daytwo_role => sp-vra8-<delascc01>or you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-VRA-13
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: Request VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=azure&account-id=<delascc01>
    Body: |
        {
          "service-id": "mssql",
          "role-assignment-type": "attach",
          "operation-type": "monitor"
        }
    Response: |
        {
          "monitor": {
            "assignment-type": "attach",
            "actions": {
              "create-or-update-roles": "/providers/Microsoft.Authorization/roleDefinitions/c608c40e-56e8-4045-8bf3-d3de8ff58ffe",
              "attach-roles": "9935e3c1-4fc2-4a8a-9783-7f75d153623f"
            }
          },
          "no-errors": true
        }
    Result:
    Remark: |
      "Role definitions updated from repositoryexample: https://github.developer.allianz.io/CloudTribe/hybrid-mssql/tree/master/TechnicalUserManagement
      No TTL aplied here. It stays assigned until it's explicitly detached.You can check directly in Azure portal (console) - betterSubscription -> Access Control (IAM) ->
      Role Assignments:mssql_monitor_role => sp-vra8-<delascc01>or you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-VRA-14
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: DELETE
    Use case: Remove all VRA TUM (Technical User Management) for HC Service (e.q. mssql,backup)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=azure&account-id=<delascc01>
    Body: |
        {
          "service-id": "mssql"
        }
    Response: |
        {
          "daytwo": {
            "assignment-type": "detach",
            "actions": {
              "detach-policy": "/subscriptions/7de0a990-3ef3-4f9b-9fa9-4f8c01c27108/providers/Microsoft.Authorization/roleDefinitions/92fb3170-d776-4688-9004-3736ca6eab2f"
            }
          },
          "deploy": {
            "assignment-type": "detach",
            "actions": {
              "detach-policy": "Exception for action(detach-policy) for Fail with code(412), details(No role assignment found for scope - /subscriptions/7de0a990-3ef3-4f9b-9fa9-4f8c01c27108!)"
            }
          },
          "no-errors": false
        }
    Result:
    Remark: |
      "The sp-vra8-<delascc01> is unassigned from mssql_deploy_role, mssql_daytwo_role.
      If no assignment found for role it's gracefully handled, mssql_monitor_role stays there untill explicitely removed.
      You can check directly in Azure portal (console) - betterSubscription -> Access Control (IAM) ->
      Role Assignments:mssql_monitor_role => sp-vra8-<delascc01>or you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AZURE-VRA-15
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: Remove VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup) operation-type monitor
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=azure&account-id=<delascc01>
    Body: |
        {
          "service-id": "backup",
          "role-assignment-type": "detach",
          "operation-type": "monitor"
        }
    Response: |
        {
          "monitor": {
            "assignment-type": "detach",
            "actions": {
              "detach-policy": "/subscriptions/7de0a990-3ef3-4f9b-9fa9-4f8c01c27108/providers/Microsoft.Authorization/roleDefinitions/c608c40e-56e8-4045-8bf3-d3de8ff58ffe"
            }
          },
          "no-errors": true
        }
    Result:
    Remark: |
      "The sp-vra8-<delascc01> is unassigned from mssql_monitor_roleYou can check directly in Azure portal (console)
      - betterSubscription -> Access Control (IAM) -> Role Assignments:No user assignment existsor you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-VRA-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: Request VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup)
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=aws&account-id=<delwbsc01>
    Body: |
        {
          "service-id": "backup",
          "role-assignment-type": "attach",
          "operation-type": "deploy"
        }
    Response: |
        {
          "code": 412,
          "message": "The <delwbsc01> is not in the connected_accounts mgmt group!"
        }
    Result:
    Remark: This only works for SCC Connected accounts.
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-VRA-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: "Request VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup)Invalid HC service name"
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Basic
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=aws&account-id=<delwbsc01>
    Body: |
        {
          "service-id": "abcd",
          "role-assignment-type": "attach",
          "operation-type": "deploy"
        }
    Response: |
        {
          "message": "Validation error: [{'message': "'abcd' is not one of ['adp', 'hc_linux', 'hc_windows', 'postgres', 'mssql', 'abs', 'sftp', 'encryptionOracle', 'encryptionNoOracle', 'oracle', 'objectStorage', 'blockStorage', 'crp.tomcat', 'crp.jboss', 'backup', 'it-master-platform', 'SharedFileStorage', 'mongoDB', 'cpam']", 'schema': {'type': 'string', 'enum': ['adp', 'hc_linux', 'hc_windows', 'postgres', 'mssql', 'abs', 'sftp', 'encryptionOracle', 'encryptionNoOracle', 'oracle', 'objectStorage', 'blockStorage', 'crp.tomcat', 'crp.jboss', 'backup', 'it-master-platform', 'SharedFileStorage', 'mongoDB', 'cpam']}, 'cause': None, 'instance': 'abcd'}]",
          "code": 406
        }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-VRA-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: "Request VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup)Invalid role-assignment-type"
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=aws&account-id=<delwscc01>
    Body: |
        {
          "service-id": "backup",
          "role-assignment-type": "abcd",
          "operation-type": "deploy"
        }
    Response: |
        {
          "message": "Validation error: [{'message': "'abcd' is not one of ['attach', 'detach']", 'schema': {'type': 'string', 'enum': ['attach', 'detach']}, 'cause': None, 'instance': 'abcd'}]",
          "code": 406
        }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-VRA-4
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: "Request VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup)Invalid operation-type"
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=aws&account-id=<delwscc01>
    Body: |
        {
          "service-id": "backup",
          "role-assignment-type": "attach",
          "operation-type": "abcd"
        }
    Response: |
        {
          "message": "Validation error: [{'message': "'abcd' is not one of ['deploy', 'daytwo', 'monitor']", 'schema': {'type': 'string', 'enum': ['deploy', 'daytwo', 'monitor']}, 'cause': None, 'instance': 'abcd'}]",
          "code": 406
        }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-VRA-5
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: Request VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup) operation-type deploy
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=aws&account-id=<delwscc01>
    Body: |
        {
          "service-id": "backup",
          "role-assignment-type": "attach",
          "operation-type": "deploy"
        }
    Response: |
        {
          "deploy": {
            "assignment-type": "attach",
            "actions": {
              "create-policy": "arn:aws:iam::223031865084:policy/backup_deploy_role",
              "attach-user-policy": "http_status(200)"
            }
          },
          "no-errors": true
        }
    Result:
    Remark: |
      "Role definitions updated from repositoryexample: https://github.developer.allianz.io/CloudTribe/hybrid-mssql/tree/master/TechnicalUserManagement
      No TTL aplied here. It stays assigned until it's explicitly detached.You can check directly in AWS console
      - betterSwitch role:  <account-tag>-<shortenv>-<projecthash>-infraadmin-assumerole | <accountId>Example: delwscc01-t--FWlwLoh3qc-infraadmin-assumerole | 650818633299Account -> IAM ->
      Users:vra_aws_technical_user => backup_deploy_role assignedor you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-VRA-6
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: Remove VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup) operation-type deploy
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=aws&account-id=<delwscc01>
    Body: |
        {
          "service-id": "backup",
          "role-assignment-type": "detach",
          "operation-type": "deploy"
        }
    Response: |
        {
          "deploy": {
            "assignment-type": "detach",
            "actions": {
              "detach-user-policy": "http_status(200)"
            }
          },
          "no-errors": true
        }
    Result:
    Remark: |
      "The backup_deploy_role is unassigned from vra_aws_technical_userYou can check directly in AWS console
      - betterSwitch role:  <account-tag>-<shortenv>-<projecthash>-infraadmin-assumerole | <accountId>Example: delwscc01-t--FWlwLoh3qc-infraadmin-assumerole | 650818633299Account ->
      IAM -> Users:vra_aws_technical_user => no role assignedor you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-VRA-7
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: Request VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup) operation-type daytwo
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=aws&account-id=<delwscc01>
    Body: |
        {
          "service-id": "backup",
          "role-assignment-type": "attach",
          "operation-type": "daytwo"
        }
    Response: |
        {
          "daytwo": {
            "assignment-type": "attach",
            "actions": {
              "create-policy": "arn:aws:iam::223031865084:policy/backup_daytwo_role",
              "attach-user-policy": "http_status(200)"
            }
          },
          "no-errors": true
        }
    Result:
    Remark: |
      "Role definitions updated from repositoryexample: https://github.developer.allianz.io/CloudTribe/hybrid-mssql/tree/master/TechnicalUserManagement
      No TTL aplied here. It stays assigned until it's explicitly detached.You can check directly in AWS console
      - betterSwitch role:  <account-tag>-<shortenv>-<projecthash>-infraadmin-assumerole | <accountId>Example: delwscc01-t--FWlwLoh3qc-infraadmin-assumerole | 650818633299Account ->
      IAM -> Users:vra_aws_technical_user => backup_daytwo_role assignedor you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-VRA-8
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: DELETE
    Use case: Remove VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup) operation-type daytwo
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=aws&account-id=<delwscc01>
    Body: |
        {
          "service-id": "backup",
          "role-assignment-type": "detach",
          "operation-type": "daytwo"
        }
    Response: |
        {
          "daytwo": {
            "assignment-type": "detach",
            "actions": {
              "detach-user-policy": "http_status(200)"
            }
          },
          "no-errors": true
        }
    Result:
    Remark: |
      "The backup_monitor_role is unassigned from vra_aws_technical_userYou can check directly in AWS console
      - betterSwitch role:  <account-tag>-<shortenv>-<projecthash>-infraadmin-assumerole | <accountId>Example: delwscc01-t--FWlwLoh3qc-infraadmin-assumerole | 650818633299Account ->
      IAM -> Users:vra_aws_technical_user => no role assignedor you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-VRA-9
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: Request VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup) operation-type monitor
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=aws&account-id=<delwscc01>
    Body: |
        {
          "service-id": "backup",
          "role-assignment-type": "attach",
          "operation-type": "monitor"
        }
    Response: |
        {
          "monitor": {
            "assignment-type": "attach",
            "actions": {
              "create-policy": "arn:aws:iam::223031865084:policy/backup_monitor_role",
              "attach-user-policy": "http_status(200)"
            }
          },
          "no-errors": true
        }
    Result:
    Remark: |
      "Role definitions updated from repositoryexample: https://github.developer.allianz.io/CloudTribe/hybrid-mssql/tree/master/TechnicalUserManagement
      No TTL aplied here. It stays assigned until it's explicitly detached.You can check directly in AWS console
      - betterSwitch role:  <account-tag>-<shortenv>-<projecthash>-infraadmin-assumerole | <accountId>Example: delwscc01-t--FWlwLoh3qc-infraadmin-assumerole | 650818633299Account ->
      IAM -> Users:vra_aws_technical_user => backup_monitor_role assignedor you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-VRA-10
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: POST
    Use case: Remove VRA TUM (Technical User Management) for HC Service (e.q. mssql, backup) operation-type monitor
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=aws&account-id=<delwscc01>
    Body: |
        {
          "service-id": "backup",
          "role-assignment-type": "detach",
          "operation-type": "monitor"
        }
    Response: |
        {
          "monitor": {
            "assignment-type": "detach",
            "actions": {
              "detach-user-policy": "http_status(200)"
            }
          },
          "no-errors": true
        }
    Result:
    Remark: |
      "The backup_monitor_role is unassigned from vra_aws_technical_userYou can check directly in AWS console
      - betterSwitch role:  <account-tag>-<shortenv>-<projecthash>-infraadmin-assumerole | <accountId>Example: delwscc01-t--FWlwLoh3qc-infraadmin-assumerole |
      650818633299Account -> IAM -> Users:vra_aws_technical_user => no role assignedor you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: SCC-AWS-VRA-11
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AWS
    Endpoint: VRA/PERMISSIONS-FOR-PROVISIONING
    Method: DELETE
    Use case: Remove all VRA TUM (Technical User Management) for HC Service (e.q. mssql,backup)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Connected
    Service type: SCC
    URL: {{baseUrl}}/vra/permissions-for-provisioning?cloud-provider=aws&account-id=<delwscc01>
    Body: |
        {
          "service-id": "backup"
        }
    Response: |
        {
          "daytwo": {
            "assignment-type": "detach",
            "actions": {
              "detach-user-policy": "http_status(200)"
            }
          },
          "deploy": {
            "assignment-type": "detach",
            "actions": {
              "detach-user-policy": "http_status(200)"
            }
          },
          "no-errors": true
        }
    Result:
    Remark: |
      "The backup_deploy_role, backup_daytwo_role are unassigned from vra_aws_technical_user.
      If no assignment found for role it's gracefully handled, backup_monitor_role stays there untill explicitely removed.
      You can check directly in AWS console - betterSwitch role:  <account-tag>-<shortenv>-<projecthash>-infraadmin-assumerole | <accountId>Example: delwscc01-t--FWlwLoh3qc-infraadmin-assumerole |
      650818633299Account -> IAM -> Users:vra_aws_technical_user => backup_monitor_role assignedor you can also check /status endpoint for records in StateTable"
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-ACCOUNT-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: ACCOUNT/FCP
    Method: POST
    Use case: (Crossplane) FCP (dedicated) account creation should be successful
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated (Subscription)
    Service type: FCP
    URL: "{{baseUrl}}/account/azure/url"
    Body: |
      {
        "accountData": {
          "accountTag": "delafcpacc4",
          "siNumber": "SI2895979",
          "accountOwners": ["extern.gavenda_jindrich@allianz.de","extern.baar_damian@allianz.de"],
          "customerEnvironment": "dev",
          "debtorNumber": "1200000024",
          "oeName": "Allianz Technology Global Linux",
          "profileName": "scc-dev-mxhkx",
          "cloudRegion": "germanywestcentral"
        }
      }
    Response: |
      {
        "requestId": "xxxx"
      }
    Result:
    Remark: |
      (Crossplane) FCP (dedicated) account is created via Step Functions (state machnine).

      Verify account cretion in Azure console (Step Functions).
      Alternatively, by checking /account/status/by or /status endpoint.

      The GIAM integration is triggered the same way as for SCC Basic, Connected.
      There is vRA integration via {{baseUrl}}/network/autodiscovery/url endpoint.
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-ACCOUNT-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: ACCOUNT/FCP
    Method: POST
    Use case: (Crossplane) FCP (dedicated) account creation with exiting account should be failed
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated (Subscription)
    Service type: FCP
    URL: "{{baseUrl}}/account/azure/url"
    Body: |
      {
        "accountData": {
          "accountTag": "delafcpacc4",
          "siNumber": "SI2895979",
          "accountOwners": ["extern.gavenda_jindrich@allianz.de","extern.baar_damian@allianz.de"],
          "customerEnvironment": "dev",
          "debtorNumber": "1200000024",
          "oeName": "Allianz Technology Global Linux",
          "profileName": "scc-dev-mxhkx",
          "cloudRegion": "germanywestcentral"
        }
      }
    Response: |
      {
        "code": 400,
        "message": "Errors: Account already exists."
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-ACCOUNT-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: ACCOUNT/FCP
    Method: GET
    Use case: Get FCP AZURE accounts ID matching with prefix
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated (Subscription)
    Service type: FCP
    URL: "{{baseUrl}}/account?cloud-provider=${CLOUD_PROVIDER}&prefix=${prefix}"
    Body: N/A
    Response: |
      {
        "account-id": ["xxxx", "yyyy"]
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-ACCOUNT-4
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: ACCOUNT/FCP
    Method: GET
    Use case: Verify search should not be found if the account is not exiting
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated (Subscription)
    Service type: FCP
    URL: "{{baseUrl}}/account?cloud-provider=${CLOUD_PROVIDER}&prefix=${prefix}"
    Body: N/A
    Response: |
      {
        "account-id": []
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-ACCOUNT-5
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: ACCOUNT/FCP
    Method: POST
    Use case: (Crossplane) FCP (dedicated) account creation with testing validations first (duplicated owners email) should not be successful
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated (Subscription)
    Service type: FCP
    URL: "{{baseUrl}}/account/azure/url"
    Body: |
      {
        "accountData": {
          "siNumber": "SI2895979",
          "accountTag": "delafcpacc4",
          "accountOwners": ["extern.gavenda_jindrich@allianz.de","extern.gavenda_jindrich@allianz.de"],
          "customerEnvironment": "dev",
          "debtorNumber": "1200000024",
          "oeName": "Allianz Technology Global Linux",
          "profileName": "scc-dev-mxhkx",
          "cloudRegion": "germanywestcentral"
        }
      }
    Response: |
      {
        "message": {"message": "Errors: Owners must be unique", "code": 400}
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-ACCOUNT-6
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: ACCOUNT/FCP
    Method: POST
    Use case: (Crossplane) FCP (dedicated) account creation with testing validations first (only one owner provided) should not be allowed
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated (Subscription)
    Service type: FCP
    URL: "{{baseUrl}}/account/azure/url"
    Body: |
      {
        "accountData": {
          "siNumber": "SI2895979",
          "accountTag": "delafcpacc4",
          "accountOwners": ["extern.gavenda_jindrich@allianz.de"],
          "customerEnvironment": "dev",
          "debtorNumber": "1200000024",
          "oeName": "Allianz Technology Global Linux",
          "profileName": "scc-dev-mxhkx",
          "cloudRegion": "germanywestcentral"
        }
      }
    Response: |
      {
        "message": "Validation error: [{'message': "['extern.gavenda_jindrich@allianz.de'] is too short"
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-ACCOUNT-7
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: ACCOUNT/FCP
    Method: POST
    Use case: (Crossplane) FCP (dedicated) account creation should not be allowed if the length of account name is longer than 12 characters
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated (Subscription)
    Service type: FCP
    URL: "{{baseUrl}}/account/azure/url"
    Body: |
      {
        "accountData": {
          "siNumber": "SI2895979",
          "accountTag": "delazurefcp1234",
          "accountOwners": ["extern.gavenda_jindrich@allianz.de","extern.baar_damian@allianz.de"],
          "customerEnvironment": "dev",
          "debtorNumber": "1200000024",
          "oeName": "Allianz Technology Global Linux",
          "profileName": "scc-dev-mxhkx",
          "cloudRegion": "germanywestcentral"
        }
      }
    Response: |
      {
        "message": "Validation error: [{'message': "'delazurefcp1234' is too long"
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-ACCOUNT-8
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: ACCOUNT/FCP
    Method: GET
    Use case: Get all account creation status
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: FCP
    URL: "{{baseUrl}}/status?request-id=<request-id>"
    Body: N/A
    Response: |
      [
        {
          "StatusId": "STATUS#AZURE#1200000029#delafcpco111-d-rEvhW2-USho",
          "DataItemId": "STEP#fa92e958257c4f39a26fa4ce50da8015#FCP_ACCOUNT_CREATION#SUCCESSFUL",
          "RequestId": "fa92e958257c4f39a26fa4ce50da8015",
          "Details": {
            "AccountId": "cab5370a-8d9f-4686-a9dd-6781c32f1184",
            "Organization": "EuDev",
            "OuId": null,
            "TunnelId": null,
            "NetworkData": null,
            "PipelineVersion": null,
            "Errors": null,
            "Type": "AzureFCPAccountCreationContext",
            "StepsToRefresh": [],
            "NetworkGateways": null,
            "Extra": null,
            "Callbacks": null,
            "AccountData": {
              "CustomerEnvironment": "dev",
              "CloudRegion": "germanywestcentral",
              "SiNumber": "SI2895979",
              "AccountTag": "delafcpco111",
              "oeName": "Allianz Technology Global Linux",
              "AccountOwners": [
                  "mirza.grbic@allianz.de",
                  "kiro.mihajlovski@allianz.de"
              ],
              "profileName": "scc-dev-mxhkx",
              "DebtorNumber": "1200000024"
            },
            "CorrelationId": "7a409fcb02c04f44ba4a61c4a8c31415",
            "Tags": {
              "scc.oeName": "az-tec",
              "scc.debtorNumber": "1200000024",
              "scc.accountOwners": "mirza.grbic@allianz.de,kiro.mihajlovski@allianz.de",
              "scc.projectName": "scc-dev-mxhkx",
              "scc.siNumber": "SI2895979",
              "scc.env": "dev"
            },
            "SqsMessages": null
          },
          "CreatedAt": "2023-03-20 07:29:36.526341",
          "UpdatedAt": "2023-03-22 05:11:20.895727",
          "EntityType": "STATUS",
          "StatusValue": "SUCCESSFUL",
          "Step": "FCP_ACCOUNT_CREATION"
        }
      ]
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-ACCOUNT-9
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: GET
    Use case: Get all Azure accounts
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: FCP
    URL: "{{baseUrl}}/account?cloud-provider=azure"
    Body: N/A
    Response: All accounts for Azure
    Result:
    Remark: Run this after you create these test accounts
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-ACCOUNT-10
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: ACCOUNT
    Method: GET
    Use case: Get Azure account(s) matching with prefix
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Any
    Service type: FCP
    URL: {{baseUrl}}/account?cloud-provider=azure&prefix=dela
    Body: N/A
    Response: Get list of Azure accounts matched with prefix
    Result:
    Remark: Run this after you create these test accounts
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-ACCOUNT-DELETE-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: ACCOUNT/FCP
    Method: DELETE
    Use case: Delete FCP (dedicted) Account By Request ID Should Be Successful
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated (Subscription)
    Service type: FCP
    URL: "{{baseUrl}}/account?cloud-provider=${CLOUD_PROVIDER}&account-id=${account_id}"
    Body: |
      {
        "dry-run": false
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-ACCOUNT-DELETE-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: ACCOUNT/FCP
    Method: GET
    Use case: Verify Account Was Deleted Successful
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated (Subscription)
    Service type: FCP
    URL: "{{baseUrl}}/account?cloud-provider=${CLOUD_PROVIDER}"
    Body: N/A
    Response: |
      {
        "account-id": []
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-NETWORK-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: NETWORK/FCP
    Method: POST
    Use case: Create Azure FCP Network (mandatory)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/network/azure/url"
    Body: |
      {
        "subscriptionId": "xxxx-xxxx-xxxx-xxxx",
        "networkData": {
          "cloudRegion": "germanywestcentral",
          "resourceGroupName": "delafcpacc4a",
          "crpAksCluster": true,
          "interactionSubnet": {
            "sizes": [28,28]
          },
          "enterpriseSubnet": {
            "sizes": [28,28]
          },
          "managementSubnet": {
            "sizes": [28,28]
          }
        }
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-NETWORK-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: NETWORK/FCP
    Method: GET
    Use case: Get FCP AZure network status
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Any
    Service type: FCP
    URL: "{{baseUrl}}/network?cloud-provider=azure&account-id=<delwfcpbsc01>"
    Body: N/A
    Response: |
      {
        "account-id": "<delwfcpbsc01>",
        "cloud-networks": []
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-NETWORK-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: NETWORK/FCP
    Method: GET
    Use case: Verify Network Was Deleted Successful
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated (Subscription)
    Service type: FCP
    URL: "{{baseUrl}}/network?cloud-provider=${CLOUD_PROVIDER}&account-id=${account_id}"
    Body: N/A
    Response: |
      {
        "cloud-networks": []
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-NETWORK-4
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: NETWORK/FCP
    Method: POST
    Use case: Create Azure FCP Network (full)
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/network/azure/url"
    Body: |
      {
        "subscriptionId": "xxxx-xxxx-xxxx-xxxx",
        "networkData": {
          "cloudRegion": "germanywestcentral",
          "resourceGroupName": "delafcpacc4b",
          "crpAksCluster": true,
          "interactionSubnet": {
            "sizes": [28]
          },
          "enterpriseSubnet": {
            "sizes": [28]
          },
          "managementSubnet": {
            "sizes": [28]
          },
          "internetIngressAgwSubnet": {
            "sizes": [28]
          },
          "internetIngressAlbSubnet": {
            "sizes": [28]
          },
          "transitionalSubnet": {
            "sizes": [28]
          },
          "agnIngressSubnet": {
            "sizes": [28]
          }
        }
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-NETWORK-5
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: NETWORK/FCP
    Method: POST
    Use case: Add additional subnet to the existing account by using the same account-tag name
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/network/azure/url"
    Body: |
      {
        "subscriptionId": "xxxx-xxxx-xxxx-xxxx",
        "networkData": {
          "cloudRegion": "germanywestcentral",
          "resourceGroupName": "delafcpacc4b",
          "crpAksCluster": true,
          "interactionSubnet": {
            "sizes": [28]
          },
          "enterpriseSubnet": {
            "sizes": [28]
          },
          "managementSubnet": {
            "sizes": [28]
          }
        }
      }
    Response: |
      {
        "code": 400,
        "message": "Errors: Resource group name already exists."
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-NETWORK-6
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: NETWORK/FCP
    Method: POST
    Use case: Add additional subnet to the existing account with unique cloud-network-name
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/network/azure/url"
    Body: |
      {
        "subscriptionId": "xxxx-xxxx-xxxx-xxxx",
        "networkData": {
          "cloudRegion": "germanywestcentral",
          "resourceGroupName": "dafa1-a",
          "crpAksCluster": true,
          "interactionSubnet": {
            "sizes": [28,28]
          },
          "enterpriseSubnet": {
            "sizes": [28,28]
          },
          "managementSubnet": {
            "sizes": [28,28]
          }
        }
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-NETWORK-7
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: NETWORK/FCP
    Method: POST
    Use case: Verify CIDRs allocation should be worked properly when create 3 vpc in pararell
    Standard Run: Y
    Fast Track Run: N
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/network/azure/url"
    Body: |
      body1 = {
        "subscriptionId": "xxxx-xxxx-xxxx-xxxx",
        "networkData": {
          "cloudRegion": "germanywestcentral",
          "resourceGroupName": "dafa-a",
          "crpAksCluster": true,
          "interactionSubnet": {
            "sizes": [28,28]
          },
          "enterpriseSubnet": {
            "sizes": [28,28]
          },
          "managementSubnet": {
            "sizes": [28,28]
          }
        }
      }

      body2 = {
        "subscriptionId": "xxxx-xxxx-xxxx-xxxx",
        "networkData": {
          "cloudRegion": "germanywestcentral",
          "resourceGroupName": "dafa-b",
          "crpAksCluster": true,
          "interactionSubnet": {
            "sizes": [28,28]
          },
          "enterpriseSubnet": {
            "sizes": [28,28]
          },
          "managementSubnet": {
            "sizes": [28,28]
          }
        }
      }

      body3 = {
        "subscriptionId": "xxxx-xxxx-xxxx-xxxx",
        "networkData": {
          "cloudRegion": "germanywestcentral",
          "resourceGroupName": "dafa-c",
          "crpAksCluster": true,
          "interactionSubnet": {
            "sizes": [28,28]
          },
          "enterpriseSubnet": {
            "sizes": [28,28]
          },
          "managementSubnet": {
            "sizes": [28,28]
          }
        }
      }
    Response: |
      {
        "request-id": "xxxx"
      }
    Result:
    Remark: Trigger network a b and c under the same account within a second
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-NETWORK-8
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: NETWORK/FCP
    Method: POST
    Use case: Create Azure FCP Network (mandatory) with RG name longer than 35 characters
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: SCC
    URL: "{{baseUrl}}/network/azure/url"
    Body: |
      {
        "subscriptionId": "xxxx-xxxx-xxxx-xxxx",
        "networkData": {
          "cloudRegion": "germanywestcentral",
          "resourceGroupName": "delafcpacc4a-with-very-long-rg-name-over-35-chars",
          "crpAksCluster": true,
          "interactionSubnet": {
            "sizes": [28,28]
          },
          "enterpriseSubnet": {
            "sizes": [28,28]
          },
          "managementSubnet": {
            "sizes": [28,28]
          }
        }
      }
    Response: |
      {
          "message": "Validation error: [{'message': \"'delafcpacc4a-with-very-long-rg-name-over-35-chars' is too long\", 'schema': {'type': 'string', 'minLength': 2, 'maxLength': 35, 'pattern': '^([a-zA-Z0-9_-]){2,35}$'}, 'cause': None, 'instance': 'delafcpacc4a-with-very-long-rg-name-over-35-chars'}, {'message': \"'delafcpacc4a-with-very-long-rg-name-over-35-chars' does not match '^([a-zA-Z0-9_-]){2,35}$'\", 'schema': {'type': 'string', 'minLength': 2, 'maxLength': 35, 'pattern': '^([a-zA-Z0-9_-]){2,35}$'}, 'cause': None, 'instance': 'delafcpacc4a-with-very-long-rg-name-over-35-chars'}]",
          "code": 406
      }
    Result:
    Remark:
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-NETWORK-DELETION-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: NETWORK
    Method: DELETE
    Use case: "Delete dedicated network in FCP account"
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/network/azure/url"
    Body: |
      {
        "dryRun": false,
        "region": "germanywestcentral",
        "virtualNetworkName": "rg-d-gwc1-<dafn01a>-networking",
        "subscriptionId": "f918ec86-2cae-4902-9bab-0eaadc5e2595",
        "requestId": "abb7ad3e63a5436ca2cf409388023fd4"
      }
    Response: |
        {
          "request-id": "xxxx"
    Result:
    Remark: |
      Check Network Deletion state machine finished successfully.
      Checkt in Azure portal that resources are deleted.
      Check mainly peering on hub / spoke side if everything is removed!
      Check that routes in Route Table are removed correctly.
      Check allocated CIDRs are deleted in CIDRAllocated table.
      Run this for every network extension use case.
      By this we will keep our account clean.
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-NETWORK-DELETION-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: NETWORK
    Method: DELETE
    Use case: "Delete dedicated network in FCP account again"
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: "{{baseUrl}}/network/azure/url"
    Body: |
      {
        "dryRun": false,
        "region": "germanywestcentral",
        "virtualNetworkName": "rg-d-gwc1-<dafn01a>-networking",
        "subscriptionId": "f918ec86-2cae-4902-9bab-0eaadc5e2595",
        "requestId": "abb7ad3e63a5436ca2cf409388023fd4"
      }
    Response: |
        {
          "request-id": "xxxx"
        }
    Result:
    Remark: |
      We want to test repeated deletions are not an issue.
      If previous deletion was not successful, we can run again to remove leftovers.
      If previous deletion was successful, calling it again with the same data should NOT be an issue.
      Check Network Deletion state machine finished successfully.
      Checkt in Azure portal that resources are deleted.
      Check mainly peering on hub / spoke side if everything is removed!
      Double check that routes in Route Table are removed correctly.
      Double check allocated CIDRs are deleted in CIDRAllocated table.
      Run this for every network extension use case.
      By this we will keep our account clean.
    JIRA:
    GHE:
-

    Testcase ID: FCP-AZURE-CIDR-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: Y
    Cloud Privder: Azure
    Endpoint: CIDR/ALLOCATION
    Method: POST
    Use case: Add existing CIDR to CIDRAllocated table for your test account and correct region
    Standard Run: Y
    Fast Track Run: SKIP
    Account Type: Any
    Service type: FCP
    URL: {{baseUrl}}/cidr/allocation?cloud-provider=azure
    Body: |
      {
        "region": "germanywestcentral",
        "cidr": "xxxxx",
        "account-name": "xxxx",
        "reason": "Manually aligning data for this account"
      }
    Response: |
        {
          "code": 500,
          "message": "Provided CIDR is already occupied. Free are: ['aaaaa', 'bbbbb', 'ccccc']"
        }
    Result:
    Remark: "The CIDR in body is already in CIDRAllocated table for this region. There is only "germanywestcentral" region in Azure staging. Test with this region."
    JIRA:
    GHE:
-
    Testcase ID: FCP-AZURE-AUTODISCOVERY-1
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: NETWORK/AUTODISCOVERY
    Method: POST
    Use case: Register FCP Dedicated account to VRA
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: {{baseUrl}}/network/autodiscovery/url
    Body: |
      {
        "cloudProvider": "azure",
        "accountId": <delafcpded01>,
        "accountName": "delafcpded01-t-xxxx",
        "projectName": "Cloud Accounts",
        "debtorNumber": 1200000024
      }
    Response: |
      {
        "requestId": "xxxx"
      }
    Result:
    Remark: |
      Verify vRA state machine was triggered and applied tags only in transitional network:
      account_name, vnet, subnet_type

      Tags are applied in terraform directly in network creation Codebuild pipeline.
      AWS does support tags on subnet level.
      This needs to be checked extra in network creation part (TF output in Extra details?).

      /status endpoint and DataItemId: VRA#WORKFLOW_STATE#SUCCESSFUL
    JIRA: |
      FCP-12137
      FCP-13318
    GHE: |
      https://github.developer.allianz.io/CloudTribe/scc-api/pull/1104
-
    Testcase ID: FCP-AZURE-AUTODISCOVERY-2
    Postman: Y
    Servicenow: N
    Customer UI: Y
    Automation: Y
    Cloud Privder: AZURE
    Endpoint: NETWORK/AUTODISCOVERY
    Method: POST
    Use case: Register Azure FCP Dedicated account without any VNET to VRA
    Standard Run: Y
    Fast Track Run: Y
    Account Type: Dedicated
    Service type: FCP
    URL: {{baseUrl}}/network/autodiscovery/url
    Body: |
      {
        "cloudProvider": "azure",
        "accountId": <delafcpded01>,
        "accountName": "delafcpded01-t-xxxx",
        "projectName": "Cloud Accounts",
        "debtorNumber": 1200000024
      }
    Response: |
      {
        "message": "There are no transitional subnets in your account! SCC+ vRA integration cannot be triggered.",
        "code": 404
      }
    Result:
    Remark: |
      Verify vRA state machine was NOT triggered.
    JIRA: |
      FCP-16107
    GHE: |
      https://github.developer.allianz.io/CloudTribe/scc-api/pull/1239
-
    Testcase ID: SCC-AZURE-NETWORK-DNS-A-RECORD-1
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: NETWORK/DNS/A-RECORD
    Method: POST
    Use case: Add DNS larger than 253 chars name and without (optional) owner
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: "{{baseUrl}}/network/dns/a-record"
    Body: |
        {
          "fqdn": "thisisfirstlabel.thisissecondlabel.thisisthirdlabel.thisisforthlabel.thisisfifthlabel.thisissixthlabel.thisisseventhlabel.thisiseigthlabel.thisisninethlabel.thisistenthlabel.thisiseleventhlabel.thisistwelvethlabel.nextlabel.privatelink.notebooks.azure.net",
          "ip-address": "1.2.3.4"
        }
    Response: |
      {
        "message": "Validation error: [{'message': \"'thisisfirstlabel.thisissecondlabel.thisisthirdlabel.thisisforthlabel.thisisfifthlabel.thisissixthlabel.thisisseventhlabel.thisiseigthlabel.thisisninethlabel.thisistenthlabel.thisiseleventhlabel.thisistwelvethlabel.nextlabel.privatelink.notebooks.azure.net' is too long\", 'schema': {'type': 'string', 'minLength': 2, 'maxLength': 253, 'description': 'Private DNS Zone name'}, 'cause': None, 'instance': 'thisisfirstlabel.thisissecondlabel.thisisthirdlabel.thisisforthlabel.thisisfifthlabel.thisissixthlabel.thisisseventhlabel.thisiseigthlabel.thisisninethlabel.thisistenthlabel.thisiseleventhlabel.thisistwelvethlabel.nextlabel.privatelink.notebooks.azure.net'}]",
        "code": 406
      }
    Result:
    Remark:
    JIRA: |
      AWSS-6820 => original implementation
      AWSS-8779 => adding groups and Service Principals as owners (types)
      FCP-16396 => extending fqdn validation to 253 chars
      FCP-16613 => making owners optional
    GHE: |
      https://github.developer.allianz.io/CloudTribe/scc-api/pull/1246
      https://github.developer.allianz.io/CloudTribe/scc-api/pull/1249
-
    Testcase ID: SCC-AZURE-NETWORK-DNS-A-RECORD-2
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: NETWORK/DNS/A-RECORD
    Method: POST
    Use case: Add DNS name and without (optional) owner
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: "{{baseUrl}}/network/dns/a-record"
    Body: |
        {
          "fqdn": "user.privatelink.database.windows.net",
          "ip-address": "1.2.3.4"
        }
    Response: |
        {
          "private-dns-zone-id": "/subscriptions/3bb7fe00-d361-4008-ba74-99a871c266ec/resourceGroups/rgp-t-gwc1-sharedservices-privatezones/providers/Microsoft.Network/privateDnsZones/privatelink.database.windows.net/A/user"
        }
    Result:
    Remark: |
      There is not endpoint for udpate or deletion.
      DO NOT forget to delete created test DNS A-Record manually in
      Azure portal.sharedservices-gwc1-s -> rgp-t-gwc1-sharedservices-privatezones -> privatelink.database.windows.net"
    JIRA: |
      AWSS-6820 => original implementation
      AWSS-8779 => adding groups and Service Principals as owners (types)
      FCP-16613 => making owners optional
    GHE: |
      https://github.developer.allianz.io/CloudTribe/scc-api/pull/1249
-
    Testcase ID: SCC-AZURE-NETWORK-DNS-A-RECORD-3
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: NETWORK/DNS/A-RECORD
    Method: POST
    Use case: Add (again) same DNS name and without (optional) owner
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: "{{baseUrl}}/network/dns/a-record"
    Body: |
        {
          "fqdn": "user.privatelink.database.windows.net",
          "ip-address": "1.2.3.4"
          ]
        }
    Response: |
        {
          "code": 412,
          "message": "Azure API response: Operation failed with status: 'Precondition Failed'. Details: The Record set user exists already and hence cannot be created again."
        }
    Result:
    Remark:
    JIRA: |
      AWSS-6820 => original implementation
      AWSS-8779 => adding groups and Service Principals as owners (types)
      FCP-16613 => making owners optional
    GHE: |
      https://github.developer.allianz.io/CloudTribe/scc-api/pull/1249
-
    Testcase ID: SCC-AZURE-NETWORK-DNS-A-RECORD-4
    Postman: Y
    Servicenow: N
    Customer UI: N
    Automation: N
    Cloud Privder: Azure
    Endpoint: NETWORK/DNS/A-RECORD
    Method: POST
    Use case: Add DNS name and (optional) owners -  Resource owner as mix of group, user and service principal
    Standard Run: N
    Fast Track Run: SKIP
    Account Type: Connected
    Service type: SCC
    URL: "{{baseUrl}}/network/dns/a-record"
    Body: |
        {
          "fqdn": "mixture.privatelink.database.windows.net",
          "ip-address": "1.2.3.4",
          "owners": [
            {
              "resource-owner": "mirza.grbic@allianzmstest.onmicrosoft.com",
              "owner-type": "User"
            },
            {
              "resource-owner": "dns a-record group",
              "owner-type": "Group"
            },
            {
              "resource-owner": "SP_mssql_monitor",
              "owner-type": "ServicePrincipal"
            }
          ]
        }
    Response: |
        {
          "private-dns-zone-id": "/subscriptions/3bb7fe00-d361-4008-ba74-99a871c266ec/resourceGroups/rgp-t-gwc1-sharedservices-privatezones/providers/Microsoft.Network/privateDnsZones/privatelink.database.windows.net/A/mixture"
        }
    Result:
    Remark: |
      Verify owner-type(s) are assigned in
      created Private DNS A-Record.privatelink.database.windows.net -> name -> Access Control (IAM) -> Role Assignments -> Customer-DNS-A-Record-Read-Write
      There is not endpoint for udpate or deletion.
      DO NOT forget to delete created test DNS A-Record manually
      in Azure portal.sharedservices-gwc1-s -> rgp-t-gwc1-sharedservices-privatezones -> privatelink.database.windows.net"
    JIRA: |
      AWSS-6820 => original implementation
      AWSS-8779 => adding groups and Service Principals as owners (types)
      FCP-16613 => making owners optional
    GHE: |
      https://github.developer.allianz.io/CloudTribe/scc-api/pull/1249
-

"""


