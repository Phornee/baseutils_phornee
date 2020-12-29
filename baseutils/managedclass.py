import os
from datetime import datetime, timedelta
import logging
import yaml
from pathlib import Path
from shutil import copyfile


class ManagedClass:

    def __init__(self, classname, execpath):
        self.execfolder = Path(execpath).parent
        self.readConfig()
        self.setupLogger(classname)

    def setupLogger(self, classname,):
        self.logger = logging.getLogger('{}_log'.format(classname))
        log_path = os.path.join(self.execfolder, self.config['logpath'])

        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s-%(message)s', '%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def readConfig(self):
        config_yml_path = os.path.join(self.execfolder, 'config.yml')

        # If config file doesn't exist yet, create it from the template
        if not os.path.isfile(config_yml_path):
            config_template_yml_path = os.path.join(self.execfolder, 'config-template.yml')
            copyfile(config_template_yml_path, config_yml_path)

        with open(config_yml_path, 'r') as config_file:
            self.config = yaml.load(config_file, Loader=yaml.FullLoader)
