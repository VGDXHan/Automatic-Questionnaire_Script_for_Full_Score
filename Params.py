import yaml

class Params:
    
    def __init__(self):
        with open('config.yaml', 'r') as f:
            cfgs = yaml.safe_load(f)
        
        self.url = cfgs["url"]
        
        self.api_key = cfgs["api_key"]
        self.base_url = cfgs["base_url"]
        
        self.QUESTIONS_PATH = cfgs["QUESTIONS_PATH"]
        self.ANSWERS_PATH = cfgs["ANSWERS_PATH"]

        self.n_questions = cfgs["n_questions"]

        self.selector_prefix = cfgs["selector_prefix"]
        self.selector_question_suffix = cfgs["selector_question_suffix"]
        self.selector_answer_suffix = cfgs["selector_answer_suffix"]
        self.selector_option_suffix = cfgs["selector_option_suffix"]
        self.subbmit_selector = cfgs["subbmit_selector"]
        self.valid_button_selector = cfgs["valid_button_selector"]
        self.score_selector = cfgs["score_selector"]
        
        
if __name__ == "__main__":
    params = Params()
    