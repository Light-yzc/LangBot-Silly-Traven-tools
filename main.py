from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time


# 注册插件
msg_i = ''
turns = 1
data = {}
def browser_gen():
    options = webdriver.EdgeOptions() # 创建一个配置对象
    # options.add_argument("--headless") # 开启无界面模式
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1000")
    options.add_experimental_option("detach", True)

    browser = webdriver.Edge(options=options)
    browser.set_window_size(1920, 1000)
    browser.get("http://127.0.0.1:8000/")
    time.sleep(3)
    element = browser.find_element(By.ID, "rightNavHolder")
    ActionChains(browser).move_to_element(element).click().perform()
    time.sleep(1)
    elm2 =browser.find_element(By.ID,"CharID1")
    ActionChains(browser).move_to_element(elm2).click().perform()
    return browser


browser  = browser_gen()
# if turns == 1:
#     global browser
#     browser  = browser_gen()
#     # <div class="flex-container swipeRightBlock flexFlowColumn flexNoGap">
#     #                 <div class="swipe_right fa-solid fa-chevron-right interactable" style="display: flex; opacity: 0.7;" tabindex="0"></div>
#     #                 <div class="swipes-counter" style="opacity: 0.7;">1&ZeroWidthSpace;/&ZeroWidthSpace;1</div>
#     #             </div>
#     try:
#         xpath_expression = "//div[@class='flex-container swipeRightBlock flexFlowColumn flexNoGap']/div[@class='swipe_right fa-solid fa-chevron-right interactable' and @style='display: flex; opacity: 0.3;' and @tabindex='0']"
#         elm1 = browser.find_element(By.XPATH,xpath_expression)
#     except:
#         xpath_expression = "//div[@class='flex-container swipeRightBlock flexFlowColumn flexNoGap']/div[@class='swipe_right fa-solid fa-chevron-right interactable' and @style='display: flex; opacity: 0.7;' and @tabindex='0']"
#         elm1 = browser.find_element(By.XPATH,xpath_expression)
#     ActionChains(browser).move_to_element(elm1).click().perform()


def get_date():
    global headers,browser
    url = 'http://127.0.0.1:8000/api/characters/all'
    headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Content-Length": "7",
    "Content-Type": "application/json",
    "Cookie": "X-CSRF-Token=da785b9567f95bfb0433bab6b12a8223cd31d35c790072eccc14b980a7700a09",
    "Host": "127.0.0.1:8000",
    "Origin": "http://127.0.0.1:8000",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
    "X-CSRF-Token": "061db89ac91586253bdaf53787066c1ed8e7f85e0d231319157bf3985f5801de9f055eb7458c2cd6592d7d44c4d47d4777c6e8b2174b776b6cafe9d6001f6836",
    "sec-ch-ua": '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"'
    }
    data = {
                '':''
            }

    res = requests.post(url = url, headers = headers,json=data)
    msg = {
        'avatar_url':res.json()[1]['avatar'],
        'file_name':res.json()[1]['chat'],
        'ch_name':res.json()[1]['name']
    }
    return msg
print('test')
def get_msg():
        global data
        url = 'http://127.0.0.1:8000/api/chats/get'
        if turns == 1:
            data = get_date()
        res = requests.post(url = url, headers = headers,json=data)
        msg = res.json()[-1]['mes']
        return msg

def del_msg():
    global browser
    elm5 = browser.find_element(By.ID,'options_button')
    ActionChains(browser).move_to_element(elm5).click().perform()
    elm6 = browser.find_element(By.ID,'option_start_new_chat')
    ActionChains(browser).move_to_element(elm6).click().perform()
    try:
        elm7 = browser.find_element(By.ID,'del_chat_checkbox')
    except:
        elm7 = browser.find_element(By.ID,"//input[@id='del_chat_checkbox']")
    ActionChains(browser).move_to_element(elm7).click().perform()
    xpath_expression = "//div[contains(@class, 'popup-button-ok') and contains(@class, 'menu_button') and contains(@class, 'result-control') and contains(@class, 'menu_button_default') and contains(@class, 'interactable')]"
    elm8 = browser.find_element(By.XPATH,xpath_expression)
    ActionChains(browser).move_to_element(elm8).click().perform()

def init_chat():
    global turns
    del_msg()
    time.sleep(2)
    try:
        xpath_expression = "//div[@class='flex-container swipeRightBlock flexFlowColumn flexNoGap']/div[@class='swipe_right fa-solid fa-chevron-right interactable' and @style='display: flex; opacity: 0.3;' and @tabindex='0']"
        elm1 = browser.find_element(By.XPATH,xpath_expression)
    except:
        xpath_expression = "//div[@class='flex-container swipeRightBlock flexFlowColumn flexNoGap']/div[@class='swipe_right fa-solid fa-chevron-right interactable' and @style='display: flex; opacity: 0.7;' and @tabindex='0']"
        elm1 = browser.find_element(By.XPATH,xpath_expression)
    ActionChains(browser).move_to_element(elm1).click().perform()
    turns = 1

    
print('test')


if turns != 1:
    msg_i = get_msg()  
def excut_msg(message):
    global msg_i,turns
    if turns == 1:
        init_msg = get_msg()
        msg_i = init_msg
        turns += 1
        return '------------------初始信息-------\n' + init_msg
    i = 1
    # browser = open_broser()
    elm3 = browser.find_element(By.ID,'send_textarea')
    elm3.send_keys(message)
    elm4 = browser.find_element(By.ID,'send_but')
    ActionChains(browser).move_to_element(elm4).click().perform()
    msg = get_msg()
    turns += 1
    while msg_i == msg or msg == message:
        i += 1
        time.sleep(2)
        msg = get_msg()
        if i > 90:
            return '<content>酒馆未响应，可能是因为Api路线问题或者额度没了</content>'
    msg_i = msg
    # browser.close()
    if i > 50:
        return msg + '\n当前Api请求过慢，可能因为供应商服务器负载过大'
    return msg

def format_str(text):
    start_index = text.find("<content>") + len("<content>")
    end_index = text.find("</content>")
    content = text[start_index:end_index].strip()
    return content

print('test')

@register(name="St", description="ST插件", version="0.1", author="Regenin")
class HelloPlugin(BasePlugin):
    global msg_i
    # 插件加载时触发
    def __init__(self, host: APIHost):
        pass

    # 异步初始化
    async def initialize(self):
        pass
    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        print('test_f')
        msg = ctx.event.text_message  # 这里的 event 即为 PersonNormalMessageReceived 的对象
        if msg == '初始化':
            init_chat()
            # 输出调试信息
            self.ap.logger.debug("ok".format(ctx.event.sender_id))

            # 回复消息 
            ctx.add_return("reply", ['初始化成功'])

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()
        elif len(msg) != 0:  
            content = msg
            out_put = format_str(excut_msg(content))
            # 输出调试信息
            self.ap.logger.debug("ok".format(ctx.event.sender_id))

            # 回复消息 
            ctx.add_return("reply", ['@'+str(ctx.event.sender_id)+'\n'+out_put])

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()

    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message  # 这里的 event 即为 GroupNormalMessageReceived 的对象
        if msg == '初始化':
            del_msg()
            self.ap.logger.debug("ok".format(ctx.event.sender_id))
            ctx.add_return("reply", ['初始化成功'])
            ctx.prevent_default()
        elif len(msg) != 0:  
            content = msg
            out_put = format_str(excut_msg(content))
            # 输出调试信息
            self.ap.logger.debug("ok, {}".format(ctx.event.sender_id))

            # 回复消息
            ctx.add_return("reply", [out_put])

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()

    # 插件卸载时触发
    def __del__(self):
        pass