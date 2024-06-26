from datetime import timedelta
from minio import Minio
from src.model.AdModel import AdType
import io

class StorageService:
    def __init__(self, endpoint:str, access_key:str, secret_key:str):
        self.storage = Minio(access_key=access_key,secret_key=secret_key,endpoint=endpoint,secure=False)
        self.bucket_name = "bads"
        if not self.storage.bucket_exists(self.bucket_name):
            self.storage.make_bucket(self.bucket_name)

    def save(self, data:bytes,ad_type:AdType,lang:str,ad_id:str,contet_type:str):
        buffer = io.BytesIO(data)
        self.storage.put_object(self.bucket_name,ad_id,buffer,metadata={"ad_type":ad_type,"lang":lang,"ad_id":ad_id},content_type=contet_type,length=len(data))

    def get_ad_download_url(self,ad_id:str)->str:
        return self.storage.get_presigned_url(method="GET",bucket_name=self.bucket_name,object_name=ad_id)# In prod pass custom duration based on campaign run time

    def delete_ad(self,ad_id:str):
        self.storage.remove_object(self.bucket_name,ad_id)
    
    def wipe_all(self):
        object_iterator = self.storage.list_objects(self.bucket_name)
        for obj in object_iterator:
            self.storage.remove_object(self.bucket_name,obj.object_name)
        self.storage.remove_bucket(self.bucket_name)
        self.storage.make_bucket(self.bucket_name)