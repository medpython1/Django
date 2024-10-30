from myapp.models import *
from fastapi import FastAPI

from mongoengine import *
import json
app=FastAPI()
# connect(db="mydatabase",host="localhost",port=27017)
@app.get("/get_book_data_id_based")
def function_for_get_date():
    get_data=Book.objects().to_json()
    convert_json=json.loads(get_data)
    for loop_data_convert_json in convert_json:
        a={"id_number":loop_data_convert_json["id_number"],"title":loop_data_convert_json["title"],"author":loop_data_convert_json["author"]}
    return a
    
