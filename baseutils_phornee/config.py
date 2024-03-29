""" Config class """
import os
import copy
from pathlib import Path
import logging
import yaml

log = logging.getLogger(__name__)


class Config:
    """ Manages a config file that will be generated in the /var/ folder
    """

    def __init__(self, package_name: str, template_path: str, config_file_name: str):
        """_summary_

        Args:
            package_name (str): Name of the package owner of the config file
            template_path (str): Path of the template file
            config_path (str): Name of config file (will be placed in home/var/{modulename} folder)
        """
        self._template_path = template_path
        self._config_file_name = config_file_name
        self.homevar = os.path.join(str(Path.home()), 'var', package_name)

        if not os.path.exists(self.homevar):
            os.makedirs(self.homevar)

        self.config = {}

        self._read_config()

    def __getitem__(self, key):
        return self.config.get(key, None)

    @staticmethod
    def get_config_path(package_name: str, config_file_name: str) -> str:
        """Get the path for the config, inside the homevar path
        Args:
            package_name (str): The name of the package... will be joined after the homevar
            config_file_name (str): Name of the config file itself (without folder... just the file name)

        Returns:
            str: The path of the config file
        """
        return os.path.join(str(Path.home()), 'var', package_name, config_file_name)

    def get_dict(self) -> dict:
        """Returns the config  dictionary
        Returns:
            dict: Config
        """
        return self.config

    def get_dict_copy(self) -> dict:
        """Returns a copy of the dictionary
        Returns:
            dict: Copy of the config
        """
        return copy.deepcopy(self.config)

    def _read_config(self):
        # First get default values from template config file
        try:
            # First try to get the template
            with open(self._template_path, 'r', encoding="utf-8") as config_template_file:
                template_config = yaml.load(config_template_file, Loader=yaml.FullLoader)
        except OSError:
            # No template
            template_config = None

        # Try to get the config
        try:
            config_yml_path = os.path.join(self.homevar, self._config_file_name)
            with open(config_yml_path, 'r', encoding="utf-8") as config_file:
                config = yaml.load(config_file, Loader=yaml.FullLoader)
        except OSError:
            config = None

        if config:
            if template_config:
                self._merge_config(config, template_config)
                self.config = template_config
            else:
                self.config = config
        else:  # No previous config
            if template_config:  # If config file doesn´t exist, but template does, write config with template content
                self.update(template_config)
                self.write()

    def refresh(self):
        """Force to read again the config file (and template)
        """
        self._read_config()

    @staticmethod
    def _merge_config(source_config: dict, dest_config: dict):
        """Merges one config dictionaty into another

        Args:
            source_config (dict): Source dictionary to merge
            dest_config (dict): Destination dictionary to be modified with the source one
        """
        # if type(source_config) != type(dest_config):
        #     raise Exception('Source and destination configs dont match its data types: {} vs {}'
        #                     .format(source_config, dest_config))
        # Update keys
        if isinstance(dest_config, dict):
            for key, value in source_config.items():
                if key not in dest_config:
                    if isinstance(value, dict):
                        dest_config[key] = {}
                    elif isinstance(value, list):
                        dest_config[key] = []
                if type(value) in [int, str]:
                    dest_config[key] = value
                Config._merge_config(source_config[key], dest_config[key])
        elif isinstance(dest_config, list):
            if not isinstance(source_config, list):
                raise TypeError()
            for elem in source_config:
                if elem not in dest_config:
                    dest_config.append(elem)
        else:
            dest_config = source_config

    def update(self, config_update):
        """Update the config with new data
        Args:
            config_update (dict): Values to modify
        """
        # Update keys
        self._merge_config(config_update, self.config)

    def write(self):
        """Write to disk the memory config 
        """
        config_yml_path = os.path.join(self.homevar, self._config_file_name)
        try:
            with open(config_yml_path, 'w', encoding="utf-8") as config_file:
                yaml.dump(self.config, config_file)
        except OSError:
            pass

    def delete(self):
        """ Delete the config file """
        config_yml_path = os.path.join(self.homevar, self._config_file_name)
        try:
            os.remove(config_yml_path)
        except OSError:
            pass
