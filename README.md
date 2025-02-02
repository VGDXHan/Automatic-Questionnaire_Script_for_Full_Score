# How to start?
1. 安装依赖 playwright v1.18.1 
2. 修改 Interactor.py
    1. self.url 改为自己问卷的链接
    2. 根据问卷实际情况修改网页 selector
3. 根据问卷实际情况修改 main.py 中创建 Solver 对象传入的 n_questions（问题数目）, n_options（每个问题的选项数目） 参数
4. 运行 main.py

> 运行前清空 logs 文件夹

