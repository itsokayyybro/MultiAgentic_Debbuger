from google import genai

client = genai.Client(api_key="AIzaSyAq4PW5Ni-67EiLBAPSVWA0ITRUeYR6xK8")

models = client.models.list()

for model in models:
    print(model.name)