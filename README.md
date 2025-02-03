# How to start?

**运行前先清空 ./logs 文件夹**

## 直接运行

1. 安装依赖 playwright v1.18.1 
2. 运行 main.py

## 在自己的问卷上运行

1. 修改 Interactor.py
    1. self.url 改为自己问卷的链接
    2. 根据问卷实际情况修改网页 selector
2. 根据问卷实际情况修改 main.py 中创建 Solver 对象传入的 n_questions（问题数目）, n_options（每个问题的选项数目） 参数
3. 运行 main.py