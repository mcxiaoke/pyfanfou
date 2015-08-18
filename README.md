## 饭否数据备份工具

备份指定用户的全部饭否消息和相册照片，可选备份好友资料列表，备份数据格式为SQLite/Html/Markdown/Txt四种，推荐保存Html格式

### 安装和使用

#### Windows

从[百度云](http://pan.baidu.com/s/1o6GcH9S#path=%252FPublic2)或[Github](https://github.com/mcxiaoke/pyfanfou/releases/latest)下载，解压运行 **pyfanfou.exe** 即可。

### 所有系统

```
// pip安装
pip install pyfanfou
// 使用命令行
fanfoubackup
// 打开GUI界面
fanfoubackupui

```

### 命令行使用

```
fanfoubackup [-h] [-u USERNAME] [-p PASSWORD] [-t TARGET] [-s] [-i]
                 [-o OUTPUT]

  -h, --help   显示帮助信息
  -u USERNAME, --username USERNAME 你的饭否帐号
  -p PASSWORD, --password PASSWORD 你的饭否密码
  -t TARGET, --target TARGET 要备份的用户ID，默认是登录帐号
  -s , --include-user 是否备份好友资料列表，默认否
  -i , --include-photo 是否备份全部相册照片，默认是
  -o OUTPUT, --output OUTPUT 备份数据存放目录，默认是当前目录下的output目录
```

## 截图

#### Windows截图一

![ui1](images/win1.png)

#### Windows截图二

![ui1](images/win2.png)

#### Mac OS X截图一

![ui1](images/backupui1.png)

#### Mac OS X截图二

![ui2](images/backupui2.png)
