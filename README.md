# 这是一个用来获取创图教育答案的软件

### 各文件功能
- exercise.xls 这是题库的excel表，感谢这位老哥 [uasier](https://github.com/uasier/xszc)
- getQ.py 用来获取试卷题目，并返回一个list
- getA.py 将excel表上的题目和答案存入字典，并遍历list的内容找到对应答案，此处参考了这位老哥的代码 [wisecsj](https://github.com/wisecsj/hfut-brush)

### 已知问题
- 可能有的题目在excel表里和从网页获取到的存在些许字符差异，导致获取不到答案，请自行查找

### （2019年4月10日）由于提交答案时请求头里面的Authorized为js控制的，本人目前不会看js代码，所以没有加入自动填写答案的功能。所以只能将答案存入本地，请打开本地的“answer.txt”，自行填写答案