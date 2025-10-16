import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"))
VS_ID    = os.getenv("VECTOR_STORE_ID")

#files = client.vector_stores.files.list(vector_store_id=VS_ID)
#for f in files.data:
    #print(f.id, f.status)

print("今アップロードされてるファイルはこれだよ")
all_files = client.files.list(purpose="user_data").data
for f in all_files:
    print(f.id, f.filename, f.bytes)
print("全" + str(len(all_files)) + "件")

print("消す？")
if input("y/n? ").lower() == "y":
    for f in all_files:
        client.files.delete(file_id=f.id)
    print("消したよ")
else:
    print("消さないよ")