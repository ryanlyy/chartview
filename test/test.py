import yaml

with open('md.yml', 'r') as file:
    docs = yaml.safe_load_all(file)

    for doc in docs:
        print(doc['name'])
