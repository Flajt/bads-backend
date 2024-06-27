import sys
from typing import List
from flask import make_response, request, jsonify, Flask
from dotenv import load_dotenv
from src.services.InteractedAdService import InteractedAdService
from src.services.StorageService import StorageService
from src.services.UserDataService import UserDataService
import src.AdService as AdService
from src.DB import DB
import os

app = Flask(__name__)
__db = DB()
__storage_service = StorageService(access_key=os.getenv("MINIO_ACCESS_KEY"),secret_key=os.getenv("MINIO_SECRET_KEY"),endpoint=os.getenv("MINIO_ENDPOINT"))
__ad_service = AdService.AdSerivce(__db,storage_service=__storage_service)
__interacted_ad_service = InteractedAdService(__db)
__user_data_service = UserDataService(__db)

@app.route("/hello")
def hello():
    return make_response("Hello World",200)


@app.route("/publisher/ads", methods=['POST'])
def ads():
    json = request.json
    if request.method == 'POST':
        ad_id = __ad_service.create_ad(title=json["title"],data=json["data_bytes"],ad_type=json["ad_type"],lang=json["lang"],content_type=json["content_type"],keywords=json["keywords"],bloom_filter=json["bloom_filter"], description=json["description"],target_url=json["target_url"])
        return make_response(jsonify({"ad_id":ad_id}),201)

@app.route("/ad", methods=['GET'])
def match_ad():
    try:
        if request.method == 'GET':
            args = request.args
            user_id = args.get("user_id",type=str)
            lang = args.get("lang",type=str)
            ad_type = args.get("ad_type",type=int)
            profile =__user_data_service.get_user_data(user_id)
            if profile is None:
                return make_response(jsonify({"error":"Profile not found"}),404)
            ads = __ad_service.match_ad(profile,lang,ad_type)# O(n*m+1) Time complexity, O(n*m+1) Space complexity
            json_ads = []
            for ad in ads: # O(1) Time compexity, since the size is limited to 10 ads
                json_ads.append(ad.toJson()) 
            if (len(ads) == 0):
                return make_response(jsonify({"msg":"No ads found"}),404)
            return make_response(jsonify({"ads":json_ads}),200)
        else:
            return make_response(jsonify({"error":"Invalid request"}),400)
    except Exception as e:
        return make_response(jsonify({"error":str(e)}),500)
    

@app.route("/interacted-ads", methods=['GET',"POST","PUT"])
def interacted_ads():
    interacted_ads = []
    if request.method == 'GET':
        ids_str = request.args.get("user_ids",type=str)
        for user_id in ids_str.split(","):
            merged_models = __interacted_ad_service.retrive_interactions(user_id)
            if (merged_models is None):
                continue
            for merged_models in merged_models:
                interacted_ads.append(merged_models.toJson())
            if (len(interacted_ads) == 0):
                return make_response(jsonify({"msg":"No ads found"}),404)
            else:
                return make_response(jsonify({"interacted_ads":interacted_ads}),200)
    elif request.method == 'POST':
            json = request.json
            __interacted_ad_service.create_interaction_profiles(user_ids=json["user_ids"])
            return "Created", 201
    elif request.method == 'PUT':
        json = request.json
        __interacted_ad_service.record_interaction(ad_id=json["ad_id"],user_id=json["user_id"],app_id=json["app_id"])
        return "Created", 201
    return make_response(jsonify({"error":"Invalid request"}),500)

@app.route("/ad-profile",methods=["POST"])
def ad_Profile():
    try:
        json = request.json
        if request.method == 'POST':
            for user_ad_profile in json["user_ad_profiles"]:
                __user_data_service.create_user_data(bloom_filter=user_ad_profile["bloom_filter"],user_id=user_ad_profile["identifier"],num_hash_functions=user_ad_profile["num_hash_func"])
            return "Created", 201
        return "Error",500
    except Exception as e:
        return make_response(jsonify({"error":str(e)}),500)

# Only use for development and testing, block in PROD!!!!
@app.route("/delete-all",methods=["DELETE"])
def test_delete():
    try:
        if (os.getenv("ALLOW_DELETE") == "DEBUG" and request.method == "DELETE"):
            __db.TEST_WIPE_ALL()
            __storage_service.wipe_all()
            return "OK",200
        return "Not Found", 404
    except Exception as e:
        return make_response(jsonify({"error":str(e)}),500)

if __name__ == '__main__':
    if os.getenv("ENV","DEBUG") == "DEBUG":
        load_dotenv(dotenv_path="./.env")
        print("RUNNING!")
        app.run(host="0.0.0.0",port=8000,debug=True)