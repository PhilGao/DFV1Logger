import requests
from DFV1Logger.config import SUBSCRIPTION_ID,AAD_ID,SECRET,TENANT_ID
import json

def gettoken():
    oauth_url = "https://login.microsoftonline.com/{tenantid}/oauth2/token".format(tenantid=TENANT_ID)
    data ={'grant_type':'client_credentials','client_id':AAD_ID,'client_secret':SECRET,'resource':'https://management.core.windows.net/'}
    oauthreq = requests.post(url= oauth_url,data=data,headers={'Content-Type':'application/x-www-form-urlencoded'})
    dict_oauthreq = eval(oauthreq.text)
    assert dict_oauthreq["token_type"] =='Bearer' and dict_oauthreq["access_token"] is not None
    access_token = dict_oauthreq["token_type"]+"\t"+dict_oauthreq["access_token"]
    return access_token


def getlinks(access_token,url=None,links = None):
    #print(url)
    if url is None:
        url = "https://management.azure.com/subscriptions/{subscriptionid}/resourcegroups/{resourcegroupname}/providers/Microsoft.DataFactory/datafactories/{datafactoryname}/datapipelines/{pipelinename}/activitywindows?api-version={apiversion}" \
            .format(
            subscriptionid=SUBSCRIPTION_ID, resourcegroupname="edp-dev", datafactoryname='edp-dev-adf01',
            pipelinename="PL_DATA_Finance_Redbox_MSQL2DB", apiversion='2015-10-01')
    if links is None:
        links = [url]
    headers = {'authorization': access_token}
    #body = json.dumps({"WindowState":"Failed"})
    body = {"WindowState":"Failed"}

    response = requests.post(url=url, headers=headers,json=body)
    jsoncontent = response.json()
    #print(response.json())
    if 'nextLink' in jsoncontent.keys():
        nextlink = jsoncontent['nextLink']
        #print(nextlink)
        links+nextlink
        getlinks(access_token,nextlink,links)
    else:
        if len(links) == 1:
            print(jsoncontent)
        return links


def savejsonfile(json):
    with open("response.json","wb") as f:
        f.write(json)
        #f.write(req.content)

if __name__=="__main__":
    adftoken = gettoken()
    print(getlinks(adftoken))