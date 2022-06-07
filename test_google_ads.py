import _locale
import googleads
import pandas as pd
import traceback
from googleads import adwords
from googleads import oauth2

_locale._getdefaultlocale = (lambda *args: ['en_UK', 'UTF-8'])

class searchVolumePuller():
      def __init__(self,client_ID,client_secret,refresh_token,developer_token,client_customer_id):
            self.client_ID = client_ID
            self.client_secret = client_secret
            self.refresh_token = refresh_token
            self.developer_token = developer_token
            self.client_customer_id = client_customer_id
            
      def get_client(self):
          access_token = oauth2.GoogleRefreshTokenClient(self.client_ID,
                                                         self.client_secret,
                                                         self.refresh_token)
          adwords_client = adwords.AdWordsClient(self.developer_token,
                                                 access_token,
                                                 client_customer_id = self.client_customer_id,
                                                 cache=googleads.common.ZeepServiceProxy.NO_CACHE)
 
          return adwords_client
      
      def get_service(self,service,client):
 
          return client.GetService(service)

      def get_search_volume(self,service_client,keyword_list):
            #empty dataframe to append data into and keywords and search volume lists#
            keywords = []
            search_volume = []
            keywords_and_search_volume = pd.DataFrame()
            #need to split data into smaller lists of 700#
            sublists = [keyword_list[x:x+700] for x in range(0,len(keyword_list),700)]
            for sublist in sublists:
                  # Construct selector and get keyword stats.
                  selector = {
                  'ideaType': 'KEYWORD',
                  'requestType' : 'STATS'
                    }
                    
                  #select attributes we want to retrieve#
                  selector['requestedAttributeTypes'] = [
                    'KEYWORD_TEXT',
                    'SEARCH_VOLUME'
                    ]
                    
                  #configure selectors paging limit to limit number of results#
                  offset = 0
                  selector['paging'] = {
                  'startIndex' : str(offset),
                  'numberResults' : str(len(sublist))
                        }
                    
                  #specify selectors keywords to suggest for#
                  selector['searchParameters'] = [{
                  'xsi_type' : 'RelatedToQuerySearchParameter',
                  'queries' : sublist
                        }]
                  
                  #pull the data#
                  page = service_client.get(selector)
                  #access json elements to return the suggestions#
                  for i in range(0,len(page['entries'])):
                        keywords.append(page['entries'][i]['data'][0]['value']['value'])
                        search_volume.append(page['entries'][i]['data'][1]['value']['value'])
                        
            keywords_and_search_volume['Keywords'] = keywords
            keywords_and_search_volume['Search Volume'] = search_volume
            
            return keywords_and_search_volume
        
if __name__ == '__main__':
     CLIENT_ID = ''
     CLIENT_SECRET = ''
     REFRESH_TOKEN = ''
     DEVELOPER_TOKEN = ''
     CLIENT_CUSTOMER_ID = ''

     keyword_list = ['SEO','Leeds','Google']

     volume_puller = searchVolumePuller(CLIENT_ID,
                                        CLIENT_SECRET,
                                        REFRESH_TOKEN,
                                        DEVELOPER_TOKEN,
                                        CLIENT_CUSTOMER_ID)

     adwords_client = volume_puller.get_client()
            
            
     targeting_service = volume_puller.get_service('TargetingIdeaService', adwords_client)

     kw_sv_df = volume_puller.get_search_volume(targeting_service,keyword_list)
