## 饭否消息备份脚本

备份指定用户的全部饭否消息，可选备份用户的相册照片和好友资料列表，存储为SQLite3数据库文件，后续将支持导出为HTML/Markdown/PDF 


### GUI界面使用

不带参数启动

```
python fanfoubackup.py
```

或者使用这个脚本启动

```
python backupui.py
```

#### 截图一

![ui1](images/backupui1.png)

#### 截图二

![ui2](images/backupui2.png)

### 命令行使用

```
python fanfoubackup.py [-h] [-u USERNAME] [-p PASSWORD] [-t TARGET]
                       [-o OUTPUT]

  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        你的饭否帐号
  -p PASSWORD, --password PASSWORD
                        你的饭否密码
  -t TARGET, --target TARGET
                        要备份的用户ID，默认是登录帐号
  -o OUTPUT, --output OUTPUT
                        备份数据存放目录，默认是当前目录下的
                        output目录
```
