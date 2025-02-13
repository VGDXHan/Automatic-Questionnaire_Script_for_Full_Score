from openai import OpenAI
import json
from Params import Params

class Solver():
    
    def __init__(self):
        self.params = Params()
    
    def solve(self):
        client = OpenAI(api_key=self.params.api_key, base_url=self.params.base_url)
        
        reminder = "我上面向你提供的是一个问卷的提取文本，不同题目间用换行符进行了间隔，你必须严格按照下列要求作答\
        作答规则:\
        1. 题目无论单选多选还是判断,都以数字形式作答，数字为选项的序号(如一题的答案选项为BCDA,则B对应序号1,A对应序号4)\
        2. 只有题干中出现多选题字样的题目（如“王某夫妇收到陌生人电话，称有一款理财产品回报率高，便去银行汇款，银行工作人员怕其上当阻止，王某夫妇应该怎么办?【多选题】”）才按照多选题处理,多个序号间用空格隔开\
        3. 判断题答题规则与单选题一致，也按照序号回答，跟对错字样无关\
        4. 不同题目的答案之间要用\n隔开\
        5. 答案行数应该与题目数量一致"
        
        with open(self.params.QUESTIONS_PATH, 'r') as f:
            f_content = f.read()
            
        try:
            print("向大鲸鱼提问...")
            content = "".join([f_content, reminder])
            # print("content:{}".format(content))
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个回答问卷的小能手"},
                    {"role": "user", "content": content},
                ],
                stream=False
            )
            print("大鲸鱼成功返回答案：")
            answer = response.choices[0].message.content
            print(answer)
        except json.JSONDecodeError as e:
            print("大鲸鱼在忙")
            exit(1)
        except Exception as e:
            print("出现意料之外的错误: {}".format(e))
            exit(1)
        
        with open(self.params.ANSWERS_PATH, "w") as f:
            f.write(answer)
        