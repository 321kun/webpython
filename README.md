# doubanban 电影收藏网页

*welcome to doubanban*

程序网址: 106.53.94.148  （本来有域名，且配了证书，但要进行网站备案，暂时放弃中）

示例管理员账号：ydqsn@163.com
示例管理员密码：1234567a


######## important ########

本版本暂时无注释，亦无生成虚拟数据功能，直接使用 mongoDB 数据库

webpython 包下有一个 movie.json 文件，需导入 mongoDB 方可使用本版本程序

mongoDB 和邮箱的私密配置没法分享，请自行设置在 .env 文件中， .env 需放在 webpython 目录

建议数据库名为 douban，内含集合 movie 和 user

测试包 test 里有重要提示，注意查看!

######## important ########


## Installation

```
$ pip install pipenv
$ git clone https://github.com/321kun/webpython
$ cd webpython
$ pipenv install --dev
$ pipenv shell
$ python -m flask run
* Running on http://127.0.0.1:5000/
