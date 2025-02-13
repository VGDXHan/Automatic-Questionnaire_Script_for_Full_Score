# How to start?

## 环境配置

本人运行环境：

Python==3.10

```bash
pip install -r requirements.txt
playwright install
```

填写 config.yaml 中的 api_key（自己 deepseek 的 api-key）

运行 main.py 会展示测试问卷的运行效果

## 在自己的问卷上运行

- 问卷星问卷：修改 config.yaml 文件即可
- 其余网站问卷：修改 config.yaml 的基础上需要根据问卷实际布局修改 Interactor 类中的代码