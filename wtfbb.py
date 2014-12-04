import requests, getpass, json

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

Proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "https://127.0.0.1:8080"
}

session = requests.session()

def parse_header(src):
    header_lines = (line.split(": ") for line in src.split("\n"))
    return { name: value for name, value in header_lines }

headers_get = parse_header("""Host: elearning.ntust.edu.tw
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0
Accept: */*
Accept-Language: zh-tw,zh;q=0.8,en-us;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
X-Requested-With: XMLHttpRequest
X-Prototype-Version: 1.7
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache""")

login_data = {
    "user_id": "b10315005",
    "password": getpass.getpass(),
    "login": "登入",
    "action": "login",
    "new_loc": ""
}

def generate_stream_post_data(stream_name):
    return {
        "cmd": "loadStream",
        "streamName": stream_name,
        "providers": "{}",
        "forOverview": "false"
    }

session.get("https://elearning.ntust.edu.tw",
            proxies = Proxies, verify = False)

session.post("https://elearning.ntust.edu.tw/webapps/login/",
             headers = headers_get, data = login_data,
             proxies = Proxies, verify = False)

response = session.post(("https://elearning.ntust.edu.tw/webapps/streamViewer/"
                         "streamViewer"),
                        headers = headers_get,
                        data = generate_stream_post_data("mygrades"),
                        proxies = Proxies, verify = False)

data = response.json()["sv_extras"]["sx_filters"]
data = [ obj for obj in data if obj["attribute"] == "se_courseId" ]
data = data[0]["choices"]
courses = data

def get_course_name(course_id):
    if course_id == "general": return "系統通告"
    return courses[course_id] if course_id in courses else "[%s]" % course_id

# open("output_courses.json", "w").write(json.dumps(data, indent = 2))

data = {
    "cmd": "loadStream",
    "streamName": "alerts",
    "providers": "{}",
    "forOverview": "false"
}

session.get(("https://elearning.ntust.edu.tw/webapps/streamViewer/streamViewer"
             "?cmd=view&streamName=alerts&globalNavigation=false"),
            headers = headers_get,
            proxies = Proxies, verify = False)

response = session.post(("https://elearning.ntust.edu.tw/webapps/streamViewer/"
                         "streamViewer"),
                        headers = headers_get,
                        data = data,
                        proxies = Proxies, verify = False)

data = response.json()["sv_streamEntries"]
data = [{"context": obj["se_context"],
         "course_id": obj["se_courseId"] if obj["se_filterName"] else "general"
        } for obj in data ]
for obj in data:
    obj["course_name"] = get_course_name(obj["course_id"])
open("output.json", "w").write(json.dumps(data, indent = 2))
