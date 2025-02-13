from playwright.sync_api import sync_playwright
from time import sleep
import random
from Params import Params


class Interactor:
    
    def __init__(self, n_questions=30):
        self.params = Params()
    
    def examine(self, page):
        q_selector_test = "".join([self.params.selector_prefix, '1', self.params.selector_question_suffix])
        a_selector_test = "".join([self.params.selector_prefix, '1', self.params.selector_answer_suffix])
        if page.locator(q_selector_test).count() == 0:
            print("提取问题描述的 selector 配置错误")
            exit(1)
        if page.locator(a_selector_test).count() == 0:
            print("提取选项描述的 selector 配置错误")
            exit(1)
        if page.locator(self.params.subbmit_selector).count() == 0:
            print("提交问卷的 selector 配置错误")
            exit(1)
        option_selector_test = "".join([self.params.selector_prefix, '1', 
                                   self.params.selector_option_suffix, "({})".format(1)])
        if page.locator(option_selector_test).count() == 0:
            print("选择选项的 selector 配置错误")
            exit(1)
    
    def extract_qa(self, page, q_selector, a_selector):
        question_locator = page.locator(q_selector)
        question = question_locator.all_inner_texts()
        answer_locator = page.locator(a_selector)
        answer = answer_locator.all_inner_texts()

        return question, answer
    
    def storage_all_qa(self, page):
        with open(self.params.QUESTIONS_PATH, "w") as f:
            f.write("") # 清空文件
        for i in range(self.params.n_questions):
            with open(self.params.QUESTIONS_PATH, 'a') as f:
                q_selector = "".join([self.params.selector_prefix, str(i+1), self.params.selector_question_suffix])
                a_selector = "".join([self.params.selector_prefix, str(i+1), self.params.selector_answer_suffix])
                q, a = self.extract_qa(page, q_selector, a_selector)
                f.write(q[0])
                f.write("\n")
                f.write(a[0])
                f.write("\n[题目分割符号]")
                f.write("\n\n")
        print("成功获取所有题目")
    
    def finish_questionaire(self, page):
        print("答案填写中...")
        with open(self.params.ANSWERS_PATH, 'r') as f:
            raw_answers = f.readlines() # 每一行是一个题目
        
        if len(raw_answers) != self.params.n_questions :# 检查答案数量是否等于题目数量
            print("题目数量为{},而答案数量为{}".format(self.params.n_questions, len(raw_answers)))
            print("大鲸鱼生成的答案有问题，重新运行一遍程序吧")
            exit(1)
            
        answers = [a.strip() for a in raw_answers]
        
        for q_idx in range(len(answers)):
            answer = answers[q_idx]
            if ' ' in answer: # 多选题
                multi_choice_answers = answer.split()
                for answer in multi_choice_answers:
                    self.click_option(page, q_idx, answer)
            else: # 单选题
                self.click_option(page, q_idx, answer)
    
    def click_option(self, page, qustion_idx, option_idx):
        sleep(random.uniform(0.1, 0.3))
        option_selector = "".join([self.params.selector_prefix, str(qustion_idx+1), 
                                   self.params.selector_option_suffix, "({})".format(option_idx)])
        page.locator(option_selector).click()

    def get_score(self, page):
        page.locator(self.params.subbmit_selector).click()
        if page.locator(self.params.valid_button_selector).count() > 0:
            print("进行智能验证")
            page.locator(self.params.valid_button_selector).click()
            print("验证成功")
        score = int(page.locator(self.params.score_selector).inner_text())
        print("最后得分: {}".format(score))
        sleep(random.uniform(2, 3))
        return score
            