import bjoern
import configparser
from arkivi.app import app


config = configparser.ConfigParser()
config.read('config.ini')

app.configs = {
    'smtp': dict(config.items('smtp')),
    'db': dict(config.items('db'))
}

bjoern.run(app, '0.0.0.0', 9999)
