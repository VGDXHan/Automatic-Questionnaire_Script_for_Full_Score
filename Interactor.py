from playwright.sync_api import sync_playwright
from time import sleep
import random
# #SM_BTN_WRAPPER_1

class Interactor:
    
    def __init__(self, n_questions, n_options):
        # 修改为你问卷的 url
        self.url = "https://kaoshi.wjx.top/vm/wFcQaPc.aspx#"
        # 修改为你问卷网页元素的 selector
        self.prefix = "#div"
        self.q_suffix = " > div.field-label > div.topichtml"
        self.a_suffix = " > div.ui-controlgroup.column1"
        self.score_selector = "#divdsc > div > div.score-form__details-wrapper.score-form__details_table > div.score-form__news.pull-left.score-form__totalval > div.tht-content > div"
        self.subbmit_selector = "#ctlNext"
        self.valid_button_selector = "#SM_BTN_WRAPPER_1"
        
        self.n_questions = n_questions
        self.n_options = n_options
                
    def select_first_options(self):
        FIRST_OPTION_IDX = 0
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.set_default_timeout(300000)
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """)
            page.goto(self.url)
            
            for q_idx in range(self.n_questions):
                self.click_option(page, q_idx, FIRST_OPTION_IDX)
                sleep(random.uniform(0.1, 0.2))
                
            q, a = self.extract_all_qa(page)
            
            score = self.get_score(page)
            
            sleep(2)
            browser.close()
            
            return q, a, score
        
    def finish_quetionaire(self, answer_table, question_pointer, option_pointer):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.set_default_timeout(300000)
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """)
            page.goto(self.url)
            
            _, answers = self.extract_all_qa(page)
            
            options = self.match_options(answers,
                answer_table, question_pointer, option_pointer)
            
            for question_num in range(self.n_questions):
                self.click_option(page, question_num, options[question_num])
                sleep(random.uniform(0.1, 0.5))
                
            score = self.get_score(page)
            sleep(random.uniform(1, 2))
            
            browser.close()
            
        return score
    
    def match_options(self, answers:list, answer_table:list, question_pointer, option_pointer):
        answer_select = [None for _ in range(self.n_questions)]
        for i in range(self.n_questions):
            if any(list(answer_table[i].values())):
                for key, val in answer_table[i].items():
                    if val == True:
                        # print("第 {} 题选择 {}".format(i+1, key))
                        answer_select[i] = key
                        break
            else:
                break

        answer_select[question_pointer] = list(answer_table[question_pointer].keys())[option_pointer]
        
        FIRST_OPTION_IDX = 0
        for i in range(question_pointer+1, self.n_questions):
            answer_select[i] = list(answer_table[i].keys())[FIRST_OPTION_IDX]
        
        options_result = [0 for i in range(self.n_questions)]
        for i in range(self.n_questions):
            for j in range(self.n_options):
                if answer_select[i] == answers[i][j]:
                    options_result[i] = j
        
        return options_result
    
    def extract_all_qa(self, page):
        q_list = []
        a_list = []
        for i in range(self.n_questions):
            q_selector = "".join([self.prefix, str(i+1), self.q_suffix])
            a_selector = "".join([self.prefix, str(i+1), self.a_suffix])
            q, a = self.extract_qa(page, q_selector, a_selector)
            q_list.append(q)
            a_list.append(a)
        
        return q_list, a_list

    def extract_qa(self, page, q_selector, a_selector):
        question_locator = page.locator(q_selector)
        question = question_locator.inner_text()
        answer_locator = page.locator(a_selector)
        answer = answer_locator.all_inner_texts()

        return question, answer[0].split('\n')

    def click_option(self, page, state, action):
        option_selector = "".join([self.prefix, str(state+1), 
                                   " > div.ui-controlgroup.column1 > div:nth-child({})".format(action+1)])
        page.locator(option_selector).click()

    def get_score(self, page):
        page.locator(self.subbmit_selector).click()
        if page.locator(self.valid_button_selector).count() > 0:
            print("进行智能验证")
            page.locator(self.valid_button_selector).click()
            print("验证成功")
        score = int(page.locator(self.score_selector).inner_text())
        print("得到奖励: {}".format(score))
        return score



            