from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time


char_id = 9
# 注册插件
msg_i = ''
turns = 1
data = {}
def browser_gen():
    options = webdriver.EdgeOptions() # 创建一个配置对象
    options.add_argument("--headless") # 开启无界面模式
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1000")
    options.add_experimental_option("detach", True)

    browser = webdriver.Edge(options=options)
    browser.set_window_size(1920, 1000)
    browser.get("http://127.0.0.1:8000/")
    time.sleep(60)
    element = browser.find_element(By.ID, "rightNavHolder")
    ActionChains(browser).move_to_element(element).click().perform()
    time.sleep(1)
    elm2 =browser.find_element(By.ID,"CharID9")
    ActionChains(browser).move_to_element(elm2).click().perform()
    return browser


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



def get_date(num):
    global headers,browser
    url = 'http://127.0.0.1:8000/api/characters/all'

    data = {
                '':''
            }

    res = requests.post(url = url, headers = headers,json=data)
    msg = { 
        'avatar_url':res.json()[num]['avatar'],
        'file_name':res.json()[num]['chat'],
        'ch_name':res.json()[num]['name']
    }
    return msg



data = {}


def get_msg(num):
        global data
        url = 'http://127.0.0.1:8000/api/chats/get'
        if turns == 1:
            data = get_date(num)
        res = requests.post(url = url, headers = headers,json=data)
        msg = res.json()[-1]['mes']
        return msg


def del_msg():
    global browser
    elm5 = browser.find_element(By.ID,'options_button')
    ActionChains(browser).move_to_element(elm5).click().perform()
    elm6 = browser.find_element(By.ID,'option_start_new_chat')
    ActionChains(browser).move_to_element(elm6).click().perform()
    time.sleep(1)
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
        ActionChains(browser).move_to_element(elm1).click().perform()

    except:
        xpath_expression = "//div[@class='flex-container swipeRightBlock flexFlowColumn flexNoGap']/div[@class='swipe_right fa-solid fa-chevron-right interactable' and @style='display: flex; opacity: 0.7;' and @tabindex='0']"
        elm1 = browser.find_element(By.XPATH,xpath_expression)
        ActionChains(browser).move_to_element(elm1).click().perform()
    turns = 1

    

if turns != 1:
    msg_i = get_msg(char_id)  



api_used = 0


api_keys = ['sk-EePwZTnKw1wGr9tU53ihERFra0YGibsRWsJSCcr8UAoe5zkp',
            'sk-RwZRrDET9C8gA1wwMoBHNWDKw28q6POvnZKHLhpV5lRW9o6T',
            'sk-4tHsNjc10139AyxcBl6z3UCpBK70CvRp4Cxd0imfDxDuLfkk',
            'sk-6ukMiAeQFEyMkNLO9Xvc6O31YXaoMmaByvCm9w7WkJE1vqNy',
            'sk-yJGPAR2MKK2tgHtEygCpSTr49r9hFGF61tYtwTEpc8glomQO',
            'sk-8ICNHRtRdTkw3JUm2H7ZKSRRiQExCGWBsrl6Xv2nfofiynB0',
            'sk-kK5Sr5ntsSBcFuvlf58mOLmftWyRMyfXg06UnAFXhFA1tKLQ',
            'sk-DMB602xu0ShoAl3h9O3SWIJKfxGsj0RUw25C88sbcMajCBJO',
            'sk-PBzedeCFGMeoMIHiKZzAnvlQE4xMscwKXmPEuWpGrPTjwdnf',
            'sk-bM3PUmHL5MOAl72dWhgCW3Rd6NIn3brpxX9JXJCwRfFhSk4h'
            ]


def change_api(num):
    global api_keys,api_used
    if num > len(api_keys)-1:
        num = num % ((len(api_keys))-1)
        
    element = browser.find_element(By.ID, "sys-settings-button")
    ActionChains(browser).move_to_element(element).click().perform()
    element2 = browser.find_element(By.ID, "api_key_custom")
    ActionChains(browser).move_to_element(element2).click().perform()
    element2.send_keys(api_keys[num])
    element3 = browser.find_element(By.ID, "api_button_openai")
    ActionChains(browser).move_to_element(element3).click().perform()
    element4 = browser.find_element(By.ID, "leftNavDrawerIcon")
    ActionChains(browser).move_to_element(element4).click().perform()



def excut_msg(message):
    global msg_i,turns,api_used
    if turns == 1:
        init_msg = get_msg(char_id)
        msg_i = init_msg
        turns += 1
        return '------------------初始信息-------（你看到这条消息就意味着你发的消息不管用，要再发一条才算正式开始对话，这条只是对对话背景的补充）\n' + init_msg
    i = 1
    # browser = open_broser()
    elm3 = browser.find_element(By.ID,'send_textarea')
    elm3.send_keys(message)
    elm4 = browser.find_element(By.ID,'send_but')
    ActionChains(browser).move_to_element(elm4).click().perform()
    msg = get_msg(char_id)
    turns += 1
    while msg_i == msg or msg == message:
        i += 1
        time.sleep(2)
        msg = get_msg(char_id)
        if i > 90:
            api_used += 1
            change_api(api_used)
            return '<content>酒馆未响应，可能是因为Api路线问题或者额度没了</content>'
    msg_i = msg
    # browser.close()
    if i > 50:
        return msg + '\n当前Api请求过慢，可能因为供应商服务器负载过大\n请过一会重新初始化后再次尝试'
    return msg
msg_to_change_char = 'CharID0  名称：两只亡灵少女   描述：无\nCharID1  名称：Freya   描述：雨中坠落的天使…….\nCharID2  名称：Miki   描述：文风比较独特\nCharID3  名称：Saber   描述：解决Saber泛滥的社会问题的Saber\nCharID4  名称：Queen   描述：异.....异形？\nCharID5 名称：Tiche   描述：抢走你牛至的魔法少女！\nCharID6  名称：伊蕾娜   描述：欢迎来到魔女的世界！\nCharID7  名称：呕吐内心的少女   描述：无\nCharID8  名称：娘化生物世界   描述：无\nCharID9  名称：帝国拷问官   描述：无\nCharID10  名称：扫一扫   描述：扫一扫更改数据\nCharID11  名称：末世孤雄RPG   描述：无\nCharID12  砂狼白子   描述：欢迎来到碧蓝档案！\nCharID13  名称：芙蕾雅   描述：雨中坠落的天使…….\nCharID14  名称：虚拟色色体验馆   描述：无\n如果报错请重新切换角色或者初始化'



def change_character(ch_id):
    global turns
    element = browser.find_element(By.ID, "rightNavHolder")
    ActionChains(browser).move_to_element(element).click().perform()
    time.sleep(1)
    elm2 = browser.find_element(By.XPATH,"//div[@title='选择/创建角色']")
    ActionChains(browser).move_to_element(elm2).click().perform()
    elm2 =browser.find_element(By.ID,ch_id)
    ActionChains(browser).move_to_element(elm2).click().perform()
    turns = 2


def format_str(text):
    index = text.find('</thinking>')
    return text[index+11:]




    

element = browser.find_element(By.ID, "ai-config-button")
ActionChains(browser).move_to_element(element).click().perform()


@register(name="St", description="ST插件", version="0.1", author="Regenin")
class Tavern_Plugin(BasePlugin):
    global msg_i    # 插件加载时触发
    def __init__(self, host: APIHost):
        pass

    # 异步初始化
    async def initialize(self):
        pass
    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        global data,char_id,turns,api_used
        msg = ctx.event.text_message  # 这里的 event 即为 PersonNormalMessageReceived 的对象
        if msg == '初始化':
            init_chat()
            # 输出调试信息
            self.ap.logger.debug("ok".format(ctx.event.sender_id))
            time.sleep(2)
            # 回复消息 
            ctx.add_return("reply", ['初始化成功'])

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()
        elif msg == '更改角色':
            self.ap.logger.debug("ok".format(ctx.event.sender_id))
            ctx.add_return("reply", ['请输入"CharID"+角色ID更改角色。\n目前角色有：\n' + msg_to_change_char])
            ctx.prevent_default()
        elif msg == 'Api':
            api_used += 1
            change_api(api_used)
            self.ap.logger.debug("ok".format(ctx.event.sender_id))
            ctx.add_return("reply", ['目前Api已经使用了' + str(api_used) + '\n总共Api有' + str(len(api_keys)+1)])
            ctx.prevent_default()
        elif msg[0:8] == "更改CharID":
            char_id = int(msg[8:])
            try:
                change_character(msg[2:])
                # init_chat()
                data = get_date(char_id)
                turns = 1
                self.ap.logger.debug("ok".format(ctx.event.sender_id))
                ctx.add_return("reply", ['更改成功，若出现乱码请初始化'])
                ctx.prevent_default()
            except:
                element = browser.find_element(By.ID, "ai-config-button")
                ActionChains(browser).move_to_element(element).click().perform()
                self.ap.logger.debug("ok".format(ctx.event.sender_id))
                ctx.add_return("reply", ['错误，可能角色不存在，需要等bot反应过来再次切换角色直到切换成功'])
                ctx.prevent_default()
        elif msg[0:6] == "CharID":
            char_id = int(msg[6:])
            try:
                change_character(msg)
                init_chat()
                data = get_date(char_id)
                self.ap.logger.debug("ok".format(ctx.event.sender_id))
                ctx.add_return("reply", ['更改成功，若出现乱码请初始化'])
                ctx.prevent_default()
            except:
                element = browser.find_element(By.ID, "ai-config-button")
                ActionChains(browser).move_to_element(element).click().perform()
                self.ap.logger.debug("ok".format(ctx.event.sender_id))
                ctx.add_return("reply", ['错误，可能角色不存在，需要等bot反应过来再次切换角色直到切换成功'])
                ctx.prevent_default()
        elif len(msg) != 0:  
            content = msg
            out_put = format_str(excut_msg(content))
            # 输出调试信息
            self.ap.logger.debug("ok".format(ctx.event.sender_id))
            # 回复消息 
            ctx.add_return("reply", [out_put])
            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()


    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        global data,char_id,turns,api_used
        msg = ctx.event.text_message  # 这里的 event 即为 GroupNormalMessageReceived 的对象
        if msg == '初始化':
            init_chat()
            self.ap.logger.debug("ok".format(ctx.event.sender_id))
            ctx.add_return("reply", ['初始化成功\n=======================\n@机器人发送任意消息开始发送故事背景信息\n与机器人的对话将从第二次开始'])
            ctx.prevent_default()
        elif msg == '更改角色':
            self.ap.logger.debug("ok".format(ctx.event.sender_id))
            ctx.add_return("reply", ['请输入"CharID"+角色ID更改角色。\n目前角色有：\n' + msg_to_change_char])
            ctx.prevent_default()
        elif msg == 'Api':
            api_used += 1
            change_api(api_used)
            self.ap.logger.debug("ok".format(ctx.event.sender_id))
            ctx.add_return("reply", ['目前Api已经使用了' + str(api_used) + '\n总共Api有' + str(len(api_keys)+1)])
            ctx.prevent_default()
        elif msg[0:6] == "CharID":
            char_id = int(msg[6:])
            try:
                change_character(msg)
                init_chat()
                data = get_date(char_id)
                self.ap.logger.debug("ok".format(ctx.event.sender_id))
                ctx.add_return("reply", ['更改成功,若出现乱码请初始化'])
                ctx.prevent_default()
            except:
                element = browser.find_element(By.ID, "ai-config-button")
                ActionChains(browser).move_to_element(element).click().perform()
                self.ap.logger.debug("ok".format(ctx.event.sender_id))
                ctx.add_return("reply", ['错误，可能角色不存在，需要等bot反应过来再次切换角色直到切换成功'])
                ctx.prevent_default()
        elif len(msg) != 0:  
            content = msg
            out_put = format_str(excut_msg(content))
            # 输出调试信息
            self.ap.logger.debug("ok, {}".format(ctx.event.sender_id))
            # 回复消息
            ctx.add_return("reply", ['推进故事次数:===' + str(turns-1) + '===\n' + out_put])
            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()
    # 插件卸载时触发
    def __del__(self):
        pass