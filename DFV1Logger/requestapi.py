import requests
from DFV1Logger.config import SUBSCRIPTION_ID,AAD_ID,SECRET,TENANT_ID


oauth_url = "https://login.microsoftonline.com/{tenantid}/oauth2/token".format(tenantid=TENANT_ID)
data ={'grant_type':'client_credentials','client_id':AAD_ID,'client_secret':SECRET,'resource':'https://management.core.windows.net/'}
oauthreq = requests.post(url= oauth_url,data=data,headers={'Content-Type':'application/x-www-form-urlencoded'})

dict_oauthreq = eval(oauthreq.text)

assert dict_oauthreq["token_type"] =='Bearer' and dict_oauthreq["access_token"] is not None
access_token = dict_oauthreq["token_type"]+"\t"+dict_oauthreq["access_token"]

url = "https://management.azure.com/subscriptions/{subscriptionid}/resourcegroups/{resourcegroupname}/providers/Microsoft.DataFactory/datafactories/{datafactoryname}/datapipelines/{pipelinename}/activitywindows?api-version={apiversion}".format(
subscriptionid= SUBSCRIPTION_ID,resourcegroupname ="edp-dev",datafactoryname='edp-dev-adf01',pipelinename="PL_DATA_Finance_Redbox_MSQL2DB",apiversion = '2015-10-01')
headers = {'authorization':access_token}
req = requests.post(url=url,headers=headers)
print(type(req.json()))


