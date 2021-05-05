import requests
import json
import os
import subprocess
import ffmpeg

def get_course_from_api(cid=None):
    # 获取课程信息
    if cid is None:
        print('请输入cid！')
        return
    url = 'https://ke.qq.com/cgi-bin/course/basic_info?cid=' + str(cid)
    response = requests.get(url).json()
    name = response.get('result').get('course_detail').get('name')
    name = name.replace('/', '／').replace('\\', '＼').replace(' ', '')
    with open(name+'.json', 'w') as f:
        f.write(json.dumps(response))
    return name


def get_chapters(filename):
    # 从json文件内获取章节信息
    with open(filename, 'r') as f:
        course_info = json.loads(f.read())
    # 如果一个课程下面有多个子课程，可以通过 terms 的下标获取正确的课程。默认只有第一个
    chapters = course_info.get('result').get('course_detail').get('terms')[0].get('chapter_info')[0].get('sub_info')
    return chapters


def get_courses_from_chapter(chapter):
    return chapter.get('task_info')


def get_course_url(course):
    # 传入课程字典，拼接成课程链接
    cid = course.get('cid')
    term_id = course.get('term_id')
    course_id = course.get('taid')
    resid_str = course.get('resid_list').replace('&quot;', '"')
    if resid_str == '':
        return []
    resid_list = json.loads(resid_str)
    if not isinstance(resid_list, list):
        resid_list = [resid_list]
    l = []
    for subid in resid_list:
        url = 'https://ke.qq.com/webcourse/{}/{}#taid={}&vid={}'.format(cid, term_id, course_id, subid)
        l.append(url)
    return l


def get_all_urls(filename):
    chapters = get_chapters(filename)
    result = {}
    for chapter in chapters:
        chapter_name = chapter.get('name')
        courses = get_courses_from_chapter(chapter)
        chapter_info = {}
        for course in courses:
            chapter_info.update({course.get('name'): get_course_url(course)})
        result.update({chapter_name: chapter_info})
    return result


def print_menu(menu):
    for item in menu:
        print(str(menu.index(item))+'. '+item)


def ts2mp4(file):
    # 如果是 Windows ，则放开下面这一行，并且注释掉 line 5:import ffmpeg
    # ffmpeg = os.path.join(os.getcwd(), 'ffmpeg.exe')
    basename = os.path.basename(file).split('.')[0]
    file_dir = os.path.split(file)[0]
    output = os.path.join(file_dir, basename)

    if os.path.exists(output + '.mp4'):
        os.remove(output + '.mp4')
    cmd = "ffmpeg" + " -i \"" + file + "\" -c copy \"" + output + "\".mp4"
    os.system(cmd)
    # subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    os.remove(file)

def get_cookies_dic_list():
    str = ''
    a = str.split('; ')
    a = list(map(lambda l: (l[0], l[1]), [str.split('=', 1) for str in a]))
    return a
