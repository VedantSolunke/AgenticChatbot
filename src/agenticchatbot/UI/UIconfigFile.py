from configparser import ConfigParser
from pathlib import Path

class Config:
    def __init__(self, config_file=None):
        self.config = ConfigParser()
        if config_file is None:
            config_file = Path(__file__).with_name('UIconfigFile.ini')
        self.config.read(config_file)

    def get_page_title(self):
        return self.config['DEFAULT']['PAGE_TITLE']

    def get_llm_model(self):
        return self.config['DEFAULT']['LLM_MODEL'].split(',')   

    def get_usecase_options(self):
        return [option.strip() for option in self.config['DEFAULT']['USECASE_OPTIONS'].split(',')]

    def get_groq_model_options(self):
        return [option.strip() for option in self.config['DEFAULT']['GROQ_MODEL_OPTIONS'].split(',')]