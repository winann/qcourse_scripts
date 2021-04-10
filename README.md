### 腾讯课堂脚本
![pypi supported versions](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-blue)  
要学一些东西，但腾讯课堂不支持自定义变速，播放时有水印，且有些老师的课一遍不够看，于是这个脚本诞生了。  
~~时间有限，所以还是半自动的。(shitcode for now)~~

### 使用方法
#### 环境
python3 + edge 89.0，其他浏览器换个webdriver就行了
#### 登录
首次运行会自动登录，若cookie失效，请手动删除`cookies.json`并重新运行脚本
#### 手动下载：  
1.新建`1.txt`  
2.浏览器抓包  
- 搜索`start`, 你会得到一堆ts文件的地址，填入`1.txt`第一行  
- 搜索`dk`， 你会得到key，是个网址，打开是乱码，不管他，填入`1.txt`第二行

3.第三行写文件名  
4.依次类推，把要下载的视频都放在`1.txt`里  
5.当前目录执行`python downloader.py`等待即可
#### 自动下载：
直接在当前目录运行`python qcourse.py`

### 更新日志
> 2020.4.10  
> 简化脚本，全自动下载

> 2020.4.9  
> 视频下载到`<chapter_name>`文件夹内

> 2020.4.8  
> 新增输入视频地址一键下载  
> 重构部分代码

> 2020.4.6  
> 上线

### 计划更新：
- 自动下载课程
- ts转换mp4
- 多线程下载
- 待补充