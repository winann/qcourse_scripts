# 腾讯课堂脚本
脚本来自：@aiguoli 的 [https://github.com/aiguoli/qcourse_scripts](https://github.com/aiguoli/qcourse_scripts)，我只是做了简单修改和适配，版权归原作者所有。在此非常感谢原作者！

### 修改内容

* 使用 `URL` 下载支持多个 `URL` 排队下载
* 下载选中的章节，支持输入 `3,4,6-9,13` 的格式多个排队下载
* 通过 cid 下载全部课程，支持 `123,321` 的格式多个排队下载
* 支持下载课程内的资料
* 支持直接填入 cookie 进行下载（在 `utils.py -> get_cookies_dic_list->str` 变量中填入 cookie 字符串）
* 支持一节课内的多个视频下载
* 支持 Mac 系统

###  使用方法

#### Mac

1. 安装 `chromium` 内核的 `Edge` 浏览器（90.0版本已测试通过）
2. 安装 `ffmpeg`（ `brew install ffmpeg` ）
3. 在项目目录执行：`pip install -r requirements.txt`
4. 在项目目录执行：`python qcourse.py`

#### Windows

1. 安装 `chromium` 内核的 `Edge` 浏览器（90.0版本已测试通过）
2. 找到工程中有 `Windows` 注释的两行，根据注释修改即可
3. 在项目目录执行：`pip install -r requirements.txt`
4. 在项目目录执行`python qcourse.py`



下面是原 [README.md](https://github.com/aiguoli/qcourse_scripts)

> 要学一些东西，但腾讯课堂不支持自定义变速，播放时有水印，且有些老师的课一遍不够看，于是这个脚本诞生了。
>
> > 2020.4.17测试可用
>
> ### 使用方法
>
> 很简单，三部完成
>
> ``` python
> 下载代码, 配置环境为python3 + edge 89
> ```
>
> ``` python
> > pip install -r requirements.txt
> ```
>
> ``` python
> > python qcourse.py
> ```
>
> ##### Tips
>
> - cid是你登录后url里面的参数，代表course_id
> - 若登录失效，删除`cookies.json`再重新运行脚本
>
> ### 功能
>
> - 模拟登录，获取cookies
> - 下载单个视频
> - 按章节下载
> - 下载整个课程
> - 视频下载后自动转换为`mp4`格式(ffmpeg)

