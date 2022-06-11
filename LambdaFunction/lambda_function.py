from getTimelineUtil import getTimelineWithID
import json
import os
import datetime
from os.path import exists
from util import check_s3folder_exists, create_s3folder, upload_s3, check_startdate_in_bookmark, update_bookmark
#from pprint import pprint

def lambda_handler(event, context):
    # TODO implement
    user_ids=['1233052817390284800','851431642950402048','40129171','332617373','1701930446']
    max_results=100 #5 up to 100
    tweet_startdate_default='2022-06-07T08:00:00Z'
    environment="dev"
    bucket="tweets-ingested"
    prefix=f'{environment}/timeline/{datetime.date.today().year}/{datetime.date.today().month}/{datetime.date.today().day}'
    current_folder=f'{datetime.datetime.now().hour}'
    prefix_bookmark=f'{environment}/meta/tweets_batchload_bookmarks'
    #print(datetime.datetime.utcnow().isoformat())
    for user_id in user_ids:
        pagination_token=None
        next_round=True
        #tweet_startdate=check_startdate_in_bookmark(bucket, f'{environment}/landing/timeline/{user_id}/bookmark/bookmark',tweet_startdate_default)
        tweet_startdate=check_startdate_in_bookmark(bucket, f'{prefix_bookmark}/bookmark_{user_id}',tweet_startdate_default)
        #print(bucket)
        #print(f'{prefix}/')
        #print(f'{user_id}/')
        if check_s3folder_exists(bucket,f'{prefix}/',f'{current_folder}/'):
            pass
        else: 
            create_s3folder(bucket,prefix,f'{current_folder}/')
       
        while next_round:
            try:
                data=getTimelineWithID(user_id,tweet_startdate, pagination_token,max_results)
                try:
                    file_name=f'timeline_{user_id}_{data["meta"]["oldest_id"]}_{data["meta"]["newest_id"]}.json'
                    file=f'{prefix}/{current_folder}/{file_name}'
                    try: 
                        print("The next pagination_token is:",data["meta"]["next_token"])
                        pagination_token=data["meta"]["next_token"]
                        next_round=True
                    except:
                        next_round=False
                        print("No futher pagination_token available!")
                   
                    #with open('mydatafile.json','w',encoding = 'utf-8') as f:
                    #    for i in range(0,len(data['data'])):
                    #        line = json.dumps(data['data'][i], sort_keys=True)
                    #        f.write(line)
                    #        f.write('\n')        
                    tweets=""
                    for i in range(0,len(data['data'])):
                            data['data'][i]["processed_at"]=int(datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S"))
                            line = json.dumps(data['data'][i])
                            print("HELLLO")
                            print(type(line))
                            tweets= tweets + line + '\n'                            
                    print(tweets)
                    upload_s3(tweets, bucket, file)              
                    update_bookmark("tweets-ingested", f'{prefix_bookmark}/bookmark_{user_id}',f"{datetime.datetime.utcnow().isoformat()[:-7]}Z")

                except:
                    next_round=False
            except:
                raise Exception(f"Fetching the latest Tweets from {user_id} failed at {datetime.datetime.utcnow().isoformat()[:-7]}Z")
        
    return {
            'statusCode': 200,
            'body': json.dumps('Tweets batch load was successful')
        }
