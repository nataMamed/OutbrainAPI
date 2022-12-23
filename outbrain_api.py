import requests
from datetime import datetime, timedelta
import requests


class OutbrainAPI:
    def __init__(self, username, password, token=''):
        self.base_url = 'https://api.outbrain.com/amplify/v0.1'

        self.auth_token = self.authenticate_by_login(token, username, password)
        self.marketer_id = self.fetch_marketers_list()['marketers'][0]['id']

    def authenticate_by_login(self, token, username, password):
        if token:
            return token
        
        response =  requests.get(self.base_url + '/login', auth=requests.auth.HTTPBasicAuth(username, password))
        return response.json()['OB-TOKEN-V1']

    def fetch_marketers_list(self):
        resp = requests.get(self.base_url + '/marketers', headers={'OB-TOKEN-V1': self.auth_token})
        return resp.json()

    def list_campaigns(self):
        campaigns = requests.get(self.base_url + '/marketers/'+self.marketer_id+'/campaigns', headers={'OB-TOKEN-V1': self.auth_token}).json()['campaigns']
        campaign_list = []
        for campaign in campaigns:
            campaign_list.append(campaign)

        return campaign_list

    def fetch_campaign_data_per_day(self, from_date, to_date):

        payload={}
        headers = {
        'OB-TOKEN-V1': self.auth_token
        }
        campaigns = self.list_campaigns()
        campaign_data = []
        for campaign in campaigns:
            
            url = f"https://api.outbrain.com/amplify/v0.1/reports/marketers/{self.marketer_id}/periodic?from={from_date}&to={to_date}&campaignId={campaign['id']}&limit=500&breakdown=daily" 

            response = requests.request("GET", url, headers=headers, data=payload).json()

            campaign_results = response['results']
            temp = []
            
            for unique_result in campaign_results:
                unique_result['campaign_id'] = campaign['id']
                unique_result['campaign_name'] = campaign['name']
                campaign_data.append(unique_result)
                
            

        return campaign_data







if __name__=="__main__":

    yesterday  = datetime.now().date() - timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    from_date = ''
    #Credentials
    username = ''
    token = ''
    password = ''
    api = OutbrainAPI(username=username, password=password, token=token)
    result = api.fetch_campaign_data_per_day(from_date=from_date, to_date=yesterday)

