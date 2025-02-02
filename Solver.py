import json
import os
from Interactor import Interactor
from collections import OrderedDict

ANSWER_TABLE_PATH = "./logs/answer_table.json"
QUESTION_POINTER_PATH = "./logs/question_pointer.json"
OPTION_POINTER_PATH = "./logs/option_pointer.json"
QUESTIOS_PATH = "./logs/questions.json"
FINAL_ASNWERS_PATH = "./logs/final_answers.txt"

class Solver():
    
    def __init__(self, n_questions, n_options):
        self.n_questions = n_questions
        self.n_options = n_options
        
        self.interactor = Interactor(n_questions=self.n_questions,
                                     n_options=self.n_options)

        self.answer_table = []
        self.question_pointer = 0
        self.option_pointer = 0
        self.is_finished = False
    
    def solve(self):
        if self.is_answer_table_exit():
            print("读取答案文件")
            self.read_answer_files()
        else:
            print("未找到答案文件,进行初始化...")
            self.init_answer_table()
            self.init_options()
            self.write_answer_files()

        loop_cnt = 0
        while not self.is_finished:
            loop_cnt += 1
            print("-"*80)
            print("进行第 {} 次迭代 | 题目指针 {} | 选项指针 {} |".format(
                loop_cnt, self.question_pointer, self.option_pointer))
            print()
            self.change_option()
            self.score_new = self.interactor.finish_quetionaire(self.answer_table, 
                                            self.question_pointer, 
                                            self.option_pointer)
            self.update_strategy()
            self.detect_finish_flag()
        
        self.storage_answers()
        
    def is_answer_table_exit(self):
        if os.path.exists(ANSWER_TABLE_PATH):
            return True
        else:
            return False
        
    def read_answer_files(self):
        with open(ANSWER_TABLE_PATH, 'r') as f:
            self.answer_table = json.load(f) 
        with open(QUESTION_POINTER_PATH, 'r') as f:
            self.question_pointer = json.load(f) 
        with open(OPTION_POINTER_PATH, 'r') as f:
            self.option_pointer = json.load(f)
        with open(QUESTIOS_PATH, 'r') as f:
            self.questions = json.load(f)
        self.detect_finish_flag()
        if not self.is_finished:
            self.score_last = self.interactor.finish_quetionaire(self.answer_table, 
                                                            self.question_pointer, 
                                                            self.option_pointer) 
        
    def init_answer_table(self):
        self.questions, options_of_all_questions, self.score_last = self.interactor.select_first_options()
        for options_of_a_question in options_of_all_questions:
            options_dict_of_a_question = OrderedDict()
            for option in options_of_a_question:
                options_dict_of_a_question[option] = False
            self.answer_table.append(options_dict_of_a_question)
    
    def init_options(self):
        self.option_pointer = 0
        self.question_pointer = 0
    
    def write_answer_files(self):
        with open(ANSWER_TABLE_PATH, 'w') as f:
            json.dump(self.answer_table, f) 
        with open(QUESTION_POINTER_PATH, 'w') as f:
            json.dump(self.question_pointer, f)  
        with open(OPTION_POINTER_PATH, 'w') as f:
            json.dump(self.option_pointer, f)
        with open(QUESTIOS_PATH, 'w') as f:
            json.dump(self.questions, f)
            
    def change_option(self):
        if self.option_pointer < self.n_options:
            self.option_pointer += 1
        else:
            print("选项指针超出范围")
    
    def change_question(self):
        if self.question_pointer < self.n_questions:
            self.question_pointer += 1
            self.option_pointer = 0
        else:
            print("题目指针超出范围")
    
    def update_strategy(self):
        delta_score = self.score_new - self.score_last
        options_dict = self.answer_table[self.question_pointer]
        if delta_score > 0: # 分数增加则更改后的答案是正确答案
            print("第 {} 题正确答案是第 {} 个选项".format(
                self.question_pointer+1, self.option_pointer+1))
            options_dict[list(options_dict.keys())[self.option_pointer]] = True
            self.change_question()
        elif delta_score < 0: # 分数减小则说明上一个答案是正确答案
            print("第 {} 题正确答案是第 {} 个选项".format(
                self.question_pointer+1, self.option_pointer))
            options_dict[list(options_dict.keys())[self.option_pointer-1]] = True
            self.change_question()
        else: # 分数不变则说明当前答案也是错误答案
            pass
        self.write_answer_files()
        if self.score_new > self.score_last:
            self.score_last = self.score_new

    def detect_finish_flag(self):
        if not self.question_pointer < self.n_questions:
            self.is_finished = True
            print("迭代完成!")
        
    def storage_answers(self):
        '''将答案以人看得懂的形式写到文件里呈现'''
        for i in range(self.n_questions):
            if any(list(self.answer_table[i].values())):
                for key, val in self.answer_table[i].items():
                    if val == True:
                        print("第 {} 题选择 {}".format(i+1, key))
                        break
                    
        with open(FINAL_ASNWERS_PATH, 'w') as f:
            for i in range(self.n_questions):
                f.write("{}. {}".format(i+1, self.questions[i]))
                for key, val in self.answer_table[i].items():
                    if val == True:
                        f.write("\n")
                        f.write(key)
                f.write("\n\n")
        print("答案已写入到 {}".format(FINAL_ASNWERS_PATH))
                        