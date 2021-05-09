import os
import yaml
import copy
from pathlib import Path
from shutil import copyfile
from abc import ABC, abstractmethod


class Config():

    def __init__(self, execpath):
        self._installfolder = Path(execpath).parent
        self.homevar = "{}/var/{}".format(str(Path.home()), self.getClassName())

        if not os.path.exists(self.homevar):
            os.makedirs(self.homevar)

        self.config = None
        self.readConfig()

    @classmethod
    @abstractmethod
    def getClassName(cls):
        pass

    def getHomevarPath(self):
        return "{}/var/{}".format(str(Path.home()), self.getClassName())

    def readConfig(self):
        config_yml_path = os.path.join(self.homevar, 'config.yml')

        # If config file doesn't exist yet, create it from the template
        if not os.path.isfile(config_yml_path):
            config_template_yml_path = os.path.join(self._installfolder, 'config-template.yml')
            copyfile(config_template_yml_path, config_yml_path)

        with open(config_yml_path, 'r') as config_file:
            self.config = yaml.load(config_file, Loader=yaml.FullLoader)

    def getConfig(self):
        return copy.deepcopy(self.config)

    def setCache(self, config):
        self.config = config

    def writeConfig(self, config):
        config_yml_path = os.path.join(self.getHomevarPath(), 'config.yml')

        with open(config_yml_path, 'w') as config_file:
            yaml.dump(config, config_file)