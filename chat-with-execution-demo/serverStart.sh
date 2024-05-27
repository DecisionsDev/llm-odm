#!/bin/bash

# Check environment variable
if [[ -z "$ODM_SERVER_URL" ]]; then
    echo "ODM_SERVER Environment variable not found. Need to specify the ODM Server URL location."
    exit 1
else 
    echo "Using ODM Server URL : $ODM_SERVER_URL"
fi

# # Deploy the Ruleapp needed for the Rule engine
# result=$(curl -o /dev/null -s -w "%{http_code}" $ODM_SERVER_URL/res/api/v1/ruleapps -u odmAdmin:odmAdmin -q | grep -q ^200 && echo 0 || echo 1)
# if [[ $result -eq 0 ]]; then

#   deployed=$(curl -X POST --data-binary @data/ruleAppsMarketing.jar $ODM_SERVER_URL/res/api/v1/ruleapps -H "Content-Type: application/octet-stream" -u odmAdmin:odmAdmin -s)

#   isDeployed=$(echo "$deployed" | grep -q "succeeded>true</succeeded")
#   if [[ $isDeployed -eq 0 ]]; then
#     echo "Ruleset is successfully deployed !."
#   else
#     echo "Cannot deploy Rules archive"
#     echo "Please Verify your ODM Server".
#   fi 
# else 
#   echo "Cannot connect to the ODM Server URL : $ODM_SERVER_URL. Exiting"
#   exit 1
# fi 

# # Deploy the RuleProject needed for the Tracability
#   deployed=$(curl -X POST --write-out "%{http_code}"  --retry 5 --retry-delay 10 -F 'file=@data/decisioncenter_project.zip;type=application/zip' $ODM_SERVER_URL/decisioncenter-api/v1/decisionservices/import -H "Content-Type: multipart/form-data" -u odmAdmin:odmAdmin -s)
#   isDeployed=$(echo "$deployed" | grep -q "already exist\|200")

# if [ $? -eq 0 ]; then
#   echo "Rules Project is successfully deployed in the Business Console !."
# else 
#   echo "Cannot deploy Rule Project to the business console. Exiting"
#   exit 1
# fi 



python3 app.py