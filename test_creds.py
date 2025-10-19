import os
from dotenv import load_dotenv
import boto3

# Force load .env
load_dotenv()

print("AWS_ACCESS_KEY_ID =", os.getenv("AWS_ACCESS_KEY_ID"))
print("AWS_SECRET_ACCESS_KEY =", os.getenv("AWS_SECRET_ACCESS_KEY")[:6] + "********")

client = boto3.client("sts")
print(client.get_caller_identity())