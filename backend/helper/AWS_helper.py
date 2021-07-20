import boto3, botocore
from io import StringIO # python3; python2: BytesIO 
import datetime
# from custom_actions.db_actions import add_model_results
# from custom_actions.s3_actions import upload_df
import pandas as pd

# ================================================================================================================================================================================================
# Establish Session Connections
# ================================================================================================================================================================================================
from delve_site.settings import M2M_S3

s3 = boto3.client(
   "s3",
   aws_access_key_id=M2M_S3['S3_KEY'],
   aws_secret_access_key=M2M_S3['S3_SECRET']
)

def upload_df_or_file_to_s3(file, acl="public-read", path = 'misc'):
    time_key = hash(datetime.datetime.now())
    if isinstance(file, pd.DataFrame): # check if file is actually a pandas df
        csv_buffer = StringIO()
        file.to_csv(csv_buffer)
        del file
        file = csv_buffer 
        file_key = path + '/{}H{}'.format('df', time_key) 
       
    else:
        file_key = path + '/{}H{}'.format(file.name, time_key) 


    try:

        s3.upload_fileobj(
            file,
            M2M_S3["S3_BUCKET"],
            file_key,
            ExtraArgs={
                "ACL": acl,
                # "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return False

    return "http://{}.s3.{}.amazonaws.com/".format(M2M_S3["S3_BUCKET"], M2M_S3['REGION'])+file_key
