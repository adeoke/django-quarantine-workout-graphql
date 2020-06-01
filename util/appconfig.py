import os
import yaml
from os import environ


class AppConfig:
    yaml_file = os.path.join(os.path.dirname(__file__), '..', 'config.yml')

    @classmethod
    def current_config(cls):
        return environ.get('environment', 'local')

    @classmethod
    def conf_for_current_env(cls):
        chosen_env = cls.current_config()

        with open(AppConfig.yaml_file, 'r') as yaml_file:
            yaml_obj = yaml.load(yaml_file, Loader=yaml.FullLoader)

        return yaml_obj.get(chosen_env)
