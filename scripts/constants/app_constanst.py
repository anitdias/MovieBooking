import yaml

with open('conf/config.yml', 'r') as file:
    config_data = yaml.safe_load(file)


class Constants:
    mongo_uri = config_data['mongodb']['uri']
    db = config_data['mongodb']['database']
    user_collection = config_data['mongodb']['database']
    movie_collection = db["movie_collection"]

