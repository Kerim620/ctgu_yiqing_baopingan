# ctgu_yiqing_baopingan
新增云函数上报！！！



### 使用云函数部署

使用腾讯云函数可每天自动上报，每天可以收到上报通知。

#### 使用方法：
1. 点此[注册腾讯云函数](https://console.cloud.tencent.com/)。
2. 点此[新建云函数](https://console.cloud.tencent.com/scf/list-create?rid=4&ns=default&keyword=helloworld%20%E7%A9%BA%E7%99%BD%E6%A8%A1%E6%9D%BF%E5%87%BD%E6%95%B0%26python3)，配置都不用管。

![image-20210814173933269](https://gitee.com/zzzjoy/My_Pictures/raw/master/image-20210814173933269.png)

3. 配置云函数：
   * 更改函数执行超时时间为900，不改也行，只是在日志里会报不通过，但是运行没问题。
   
     ![image-20210814174322964](https://gitee.com/zzzjoy/My_Pictures/raw/master/image-20210814174322964.png)

   * 新建触发器，每天定时7点运行为cron表达式为0 0 7 * * *，建议自行查看文档设置定时任务。

      ![image-20210814175714071](https://gitee.com/zzzjoy/My_Pictures/raw/master/image-20210814175714071.png)

   * 部署函数代码，新建文件config.json配置文件，复制index.py内容和config.json内容，更改config文件内容，配置如下。其中消息推送渠道只有pushplus，请自行上[pushplus官网](https://pushplus.hxtrip.com/message)注册，获取token。

      ```
      config参数说明
      pushplus_token(string)： pushplus推送渠道的token，自行去pushplus官网获取。
      push_level(int)：通知等级，1-5级，分别是：
          1. 每次都通知，通知详细信息。
          2. 每次都通知，通知简略信息。
          3. 报平安成功率!=100%时通知，通知详细信息。
          4. 报平安成功率<90%时通知，通知详细信息。
          5. 报平安成功率<50%时通知，通知详细信息。
      timeout(double)：登录的超时时间，判断报平安服务器是否挂掉。
      wait_time(double)：每报完一个的等待时间。
      users(list)：用户列表，格式为[[usr1,pwd1,token1],[usr2,pwd2]]，其中每个用户的token为各自的pushplus_token，失败会推送消息到单个用户，可不填此参数。
      ```

      完成之后部署云函数。

      ![image-20210814175110990](https://gitee.com/zzzjoy/My_Pictures/raw/master/image-20210814175110990.png)

4. 测试

   点击部署旁的测试即可，测试结果在日志管理中查看，测试成功后会收到pushplus推送消息

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
