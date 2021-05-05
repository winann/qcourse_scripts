import json
import os
import time

import utils
from downloader import download_single, lg_download, download_zip_doc

from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException, NoSuchElementException

import shutil
from multiprocessing import Pool

BASE_DIR = os.getcwd()
COURSE_DIR = os.path.join(BASE_DIR, 'courses')
if not os.path.exists(COURSE_DIR):
    os.mkdir(COURSE_DIR)


class QCourse:
    def __init__(self):
        # 初始化options
        self.prefs = {"download.default_directory": os.getcwd()}
        self.options = EdgeOptions()
        self.options.use_chromium = True
        self.options.add_argument("log-level=3")
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_experimental_option('prefs', self.prefs)
        self.options.add_argument("--mute-audio")

        self.login_url = 'https://ke.qq.com/'

        # Mac 下配置 options 报错，故扔掉了。如果是 Windows，请使用路径下面的 msedgedriver.exe。（注释掉下面一行，放开下下行）
        self.driver = Edge(executable_path=os.path.join(BASE_DIR, 'msedgedriver'), capabilities={})
        # self.driver = Edge(executable_path='msedgedriver.exe', options=self.options)

        # self.driver = Edge(executable_path=os.path.join(BASE_DIR, 'msedgedriver'), capabilities=desired_cap, options=self.options)

    def login(self):
        self.driver.get('https://ke.qq.com/')
        self.driver.find_element_by_id('js_login').click()
        time.sleep(1)

        WebDriverWait(self.driver, 300).until_not(
            EC.presence_of_element_located((By.CLASS_NAME, 'ptlogin-mask'))
        )

        dictCookies = self.driver.get_cookies()
        jsonCookies = json.dumps(dictCookies)
        with open('cookies.json', 'w') as f:
            f.write(jsonCookies)
        print('登陆成功！')

    def close(self):
        self.driver.close()

    def _get_video(self, video_url=None, path=None, index=None):
        if not video_url:
            print('请输入视频url！')
        # 跳转一次没法跳转，可能是设置了preventDefault
        self.driver.get(video_url)
        self.driver.get(video_url)
        try:
            # 等待视频开始播放
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'loki-time'))
            )
            WebDriverWait(self.driver, 60).until_not(
                lambda driver: driver.find_element_by_class_name('loki-time').get_attribute("innerHTML") == '00:00 / 00:00'
            )

            title = self.driver.title
            if index is not None:
                title = "{:02}_{}".format(index, title)

            networks = self.driver.execute_script('return window.performance.getEntries()')
            ts_url = key_url = ''
            for network in networks:
                if '.ts?start' in network.get('name'):
                    ts_url = network.get('name')
                elif 'get_dk' in network.get('name'):
                    key_url = network.get('name')
            download_single(ts_url, key_url, title, path)
        except TimeoutException:
            # 如果超时，可能是下载的资料，则查看是否有下载按钮，有的话，就下载
            title = self.driver.title
            try:
                down_btn = self.driver.find_element_by_class_name('download-btn')
                if down_btn.text == '下载资料':
                    url = down_btn.get_attribute('href')
                    download_zip_doc(url, title, path)
            except Exception:
                print('没有找到视频，也没有找到可下载的文件，可能是还未开课')

    def get_video(self, video_url=None, path=None, index=None):
        if isinstance(video_url, list):
            for url in video_url:
                if url:
                    self._get_video(url, path, index)
        else:
            self._get_video(video_url, path, index)

    def load_cookies(self):
        if not os.path.exists('cookies.json'):
            self.login()
        with open('cookies.json', 'r') as f:
            listCookies = json.loads(f.read())
        self.driver.get(self.login_url)
        for cookie in listCookies:
            self.driver.add_cookie({
                'domain': '.ke.qq.com',
                'httpOnly': cookie['httpOnly'],
                'name': cookie['name'],
                'path': '/',
                'secure': cookie['secure'],
                'value': cookie['value']
            })
        for cookie in utils.get_cookies_dic_list():
            self.driver.add_cookie({
                'domain': '.ke.qq.com',
                'httpOnly': False,
                'name': cookie[0],
                'path': '/',
                'secure': False,
                'value': cookie[1]
            })

# 通过 URL 下载视频
def download_from_urls():
    url = input('输入视频链接(多个使用逗号分割)：')
    qq_course = QCourse()
    qq_course.load_cookies()
    for url in url.split(','):
        chapter_path = os.path.join(COURSE_DIR, 'single')
        qq_course.get_video(video_url=url, path=chapter_path)
    qq_course.close()

# 通过课程 ID，下载需要的章节
def download_course_range():
    cid = input('请输入课程cid:')
    course_name = utils.get_course_from_api(cid)
    print('获取课程信息成功')
    url_dict = utils.get_all_urls(course_name+'.json')
    chapter_names = list(url_dict.keys())
    utils.print_menu(chapter_names)
    indexs = input('请输入要下载的章节(例如：1, 3, 5-8)：')
    indexs = indexs.split(',')
    l = []
    for num in indexs:
        if '-' in num:
            nums = num.split('-')
            l += list(range(int(nums[0]), int(nums[1]) + 1))
        else:
            l.append(int(num))
    print('输入的章节：' + ','.join([str(i) for i in l]))
    qq_course = QCourse()
    qq_course.load_cookies()

    p = Pool(1)

    for index in l:
        chapter_name = chapter_names[index]
        courses = url_dict.get(chapter_name)
        chapter_name = chapter_name.replace('/', '／') .replace('\\', '＼')
        print('即将开始下载章节：' + chapter_name)
        print('='*20)
        chapter_path = os.path.join(COURSE_DIR, course_name, f'{index:02}_' + chapter_name)
        if not os.path.exists(chapter_path):
            os.makedirs(chapter_path)
        for i, course in enumerate(courses):
            course_url = courses.get(course)
            qq_course.get_video(video_url=course_url, path=chapter_path, index=i)
        print('正在后台移动 %s ...' % chapter_name)
        p.apply_async(move_to_nas, args=(chapter_path, course_name))

    p.close()
    p.join()
    print('%s 下载和移动完成！' % course_name)
    qq_course.close()

# 通过课程 ID 下载所有的章节
def download_courses():
    cids = input('请输入课程cid(多个 ID 用 `,` 分割)：')
    cids = cids.split(',')
    print('即将下载：%s' % cids)
    p = Pool(1)
    for cid in cids:
        print(cid)
        course_name = utils.get_course_from_api(cid)
        print('获取课程信息成功,准备下载！')
        qq_course = QCourse()
        qq_course.load_cookies()
        url_dict = utils.get_all_urls(course_name+'.json')
        chapter_names = list(url_dict.keys())

        for chapter in url_dict:
            chapter_path = os.path.join(COURSE_DIR, course_name, "{:02}_{}".format(chapter_names.index(chapter), chapter))
            if not os.path.exists(chapter_path):
                os.makedirs(chapter_path)
            print('正在下载章节：' + chapter)
            courses = url_dict.get(chapter)
            for i, course in enumerate(courses):
                course_url = courses.get(course)
                print('正在下载课程：' + course + ', ', end='')
                qq_course.get_video(video_url=course_url, path=chapter_path, index=i)
            print('正在后台移动 %s ...' % chapter)
            p.apply_async(move_to_nas, args=(chapter_path, course_name))

    p.close()
    p.join()
    print('%s 下载和移动完成！' % course_name)
    qq_course.close()

# 移动到其他地方，乞丐 Mac 表示没有地方放这么多东西
def move_to_nas(chapter_path, course_name):
    return
    # target_path = os.path.join('/Volumes/downloads/', course_name)
    # if not os.path.exists(target_path):
    #     os.makedirs(target_path)
    # shutil.move(chapter_path, target_path)

def main():
    menu = ['通过链接下载课程', '下载课程指定章节', '下载课程全部视频']
    utils.print_menu(menu)
    chosen = input('\n输入需要的功能：')
    chosen = int(chosen)
    if chosen == 0:
        download_from_urls()
    elif chosen == 1:
        download_course_range()
    elif chosen == 2:
        download_courses()

if __name__ == '__main__':
    main()
