import yaml

with open('conf/config.yml', 'r') as file:
    config_data = yaml.safe_load(file)


class Constants:
    mongo_uri = config_data['mongodb']['uri']
    db = config_data['mongodb']['database']
    user_collection = config_data['mongodb']['user_collection']
    movie_collection = config_data['mongodb']['movie_collection']
    user_booking_collection = config_data['mongodb']['user_booking_collection']

