# ctgu_yiqing_baopingan

自用小范围自动报平安，可从xlsx文件读取账号密码数据批量上报。

目前有两种途径上报，一种是使用selenium模块模拟浏览器来上报，一种是使用requests模块操纵数据上报。选择其一就行。

### 使用selenium模块：

#### 优缺点：

模拟浏览器登录上报，安全可靠，但是会由于如果页面加载慢的话，需要自行调整等待加载时间，而且linux服务器不能用。

#### 使用方法：

1. 安装依赖包：pip install -r requirements.txt
2. 下载你的chrome浏览器相同版本chromedriver驱动，chrome版本自己在浏览器中查看，下载地址：http://npm.taobao.org/mirrors/chromedriver/
3. 将chromedriver.exe放置在python的Scripts路径下
4. 改info.xlsx的绝对路径
5. 如遇到别的问题，一般是等待时间问题，改下面的各个sleep时间就行

### 使用requests模块：

#### 优缺点：

速度快效率高，没啥缺点，直接操纵网页代码，如果报平安服务器新增了奇奇怪怪的验证，可能要重新改代码适配。

#### 使用方法：

1. 安装依赖包：pip install -r requirements.txt
2. 改info.xlsx的绝对路径

