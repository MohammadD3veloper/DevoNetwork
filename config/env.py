import environ
import os


BASE_DIR = environ.Path(__file__) - 2


env = environ.Env()


env.read_env(os.path.join(BASE_DIR, '.env/.local.env'))
