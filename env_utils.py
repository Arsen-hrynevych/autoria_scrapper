import os
from dotenv import load_dotenv

load_dotenv()


def get_env_variable(variable_name):
    try:
        return os.environ[variable_name]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(variable_name)
        raise Exception(error_msg)


# Define your environment variables
DATABASE_URL = os.environ["DATABASE_URL"]
MAX_PAGES = int(os.environ["MAX_PAGES"])
