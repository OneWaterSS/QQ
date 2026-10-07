import smtplib
import json
import random
import datetime
import urllib.request
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header


def get_random_image():
    """获取一张随机彩色图片，返回图片二进制数据"""
    # 每次运行随机一个ID，picsum有0-1084号图片
    image_id = random.randint(0, 1084)
    url = f"https://picsum.photos/id/{image_id}/800/500"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read()
    except Exception:
        # 备用：完全随机
        try:
            req = urllib.request.Request("https://picsum.photos/800/500", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read()
        except Exception as e:
            print(f"图片获取失败：{e}")
            return None


def get_weather():
    """获取贵阳天气，返回天气描述和温馨提醒"""
    # Open-Meteo免费天气API，贵阳坐标
    url = ("https://api.open-meteo.com/v1/forecast"
           "?latitude=26.65&longitude=106.72&current=temperature_2m,weather_code")

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        temp = data["current"]["temperature_2m"]
        code = data["current"]["weather_code"]

        # 天气码对照：https://open-meteo.com/en/docs
        weather_map = {
            0: "晴天",
            1: "多云", 2: "多云", 3: "阴天",
            45: "有雾", 48: "有雾凇",
            51: "小毛毛雨", 53: "毛毛雨", 55: "大毛毛雨",
            61: "小雨", 63: "中雨", 65: "大雨",
            66: "冻雨", 67: "大冻雨",
            71: "小雪", 73: "中雪", 75: "大雪",
            77: "小雪粒",
            80: "小阵雨", 81: "阵雨", 82: "大阵雨",
            85: "小阵雪", 86: "大阵雪",
            95: "雷阵雨", 96: "雷阵雨夹冰雹", 99: "大雷阵雨夹冰雹",
        }

        weather_desc = weather_map.get(code, "天气良好")
        temp_str = f"{temp:.0f}°C"

        # 根据天气给出温馨提醒
        reminder = ""
        if code in (0, 1, 2):
            if temp >= 30:
                reminder = "今天出太阳，外面挺晒的，出门记得涂防晒，带把伞遮阳。"
            elif temp >= 20:
                reminder = "天气不错，有空出去晒晒太阳，心情会好。"
            elif temp >= 10:
                reminder = "今天天气挺好的，温度适宜，适合出门走走。"
            else:
                reminder = "虽然有太阳，但温度不高，出门多穿一件。"
        elif code == 3:
            reminder = "今天阴天，看着有点闷，别忘了通风透气。"
        elif code in (45, 48):
            reminder = "今天有雾，出门注意安全，能见度低的话慢点走。"
        elif code in (51, 53, 55):
            reminder = "外面在下毛毛雨，出门带把伞，不用太大也行。"
        elif code in (61, 80):
            reminder = "今天有小雨，记得带伞，鞋子别穿容易湿的。"
        elif code in (63, 81):
            reminder = "今天有雨，雨势不小，带好伞，尽量少在外头跑。"
        elif code in (65, 82):
            reminder = "今天雨很大，能不出去就别出去了，非得出去注意安全。"
        elif code in (66, 67):
            reminder = "今天有冻雨，路面可能结冰，出门特别小心。"
        elif code in (71, 77, 85):
            reminder = "今天下雪了，注意保暖，走路小心别滑倒。"
        elif code in (73, 75, 86):
            reminder = "今天雪挺大的，尽量少出门，注意保暖别冻着。"
        elif code in (95, 96, 99):
            reminder = "今天有雷阵雨，打雷的时候别在空旷地方待着，注意安全。"

        # 温度提醒
        if temp >= 35:
            reminder += " 温度很高，注意防暑，多喝水。"
        elif temp <= 0:
            reminder += " 天气很冷，出门穿厚点，帽子围巾手套都带上。"
        elif temp <= 5:
            reminder += " 外面挺冷的，出门多穿点。"

        return f"贵阳今天{weather_desc}，{temp_str}。{reminder}"
    except Exception as e:
        return f"天气获取失败：{e}"

# ===== 邮件配置（支持环境变量，GitHub Actions用 / 本地用默认值）=====
from_addr = os.environ.get("FROM_ADDR", "2031911770@qq.com")
auth_code = os.environ.get("AUTH_CODE", "opylvsiejazofchi")
to_addr = os.environ.get("TO_ADDR", "1273289785@qq.com")

# ===== 100句情话 =====
# 原则：每一句都"确定成立"——只写我的感受、我的习惯、我对你的了解、叮嘱和打算，
# 不虚构任何具体刚发生的事件（刷视频/路过/打喷嚏/发奖金这类一律不要）。
love_messages = [
    # 日常惦记型（感受，任何时候都成立）
    "在干嘛呢，没什么事，就是问问。",
    "也没什么特别的事，就是有点想你。",
    "一闲下来，脑子里全是你。",
    "人多的地方，总会下意识地找你。",
    "不管在做什么，都能顺便想你一下。",
    "忙也好闲也好，反正都惦记着你。",
    "一天下来，最放松的时刻就是找你聊两句。",
    "有时候看着手机，就是在等你的消息弹出来。",
    "别人跟我说话我听着，心里其实在想你。",
    "想你这件事，不分场合，也不挑时间。",
    "今天也是普普通通的一天，普普通通地想你。",
    "不管几点，看到好玩的第一反应都是发给你。",
    "你的消息，我永远都想秒回。",
    "只要一停下来，就开始想你。",
    "不知道你在干嘛，所以来问问。",
    # 干饭搭子型
    "你吃东西的样子，挺下饭的。",
    "想吃火锅了，你什么时候有空。",
    "遇到好吃的，总想着下次带你来。",
    "西瓜最中间那一勺，永远是你的。",
    "好吃的总想给你留一份，这习惯改不掉了。",
    "你挑的餐厅就没踩过雷，以后还你挑。",
    "剥好的虾才好吃，我给你剥。",
    "等我学会新菜，第一个做给你吃。",
    "奶茶第二杯半价这种事，我只想跟你凑。",
    "你爱吃的那几样，我都记着呢。",
    "跟你吃饭，吃什么都香。",
    "饿不饿？饿了我陪你吃点。",
    "以后想吃什么直接报菜名，我来安排。",
    "你负责吃，我负责买单和夹菜。",
    "两个人吃饭的好处，就是可以多点一个菜。",
    # 俏皮互怼型
    "我掐指一算，你命里缺我。",
    "警告你一次，不许再这么可爱了。",
    "你这个人吧，越看越觉得捡到宝了。",
    "别对我笑，我定力不太好。",
    "你是不是故意的？故意让我这么喜欢你。",
    "想你是会上瘾的，我已经戒不掉了。",
    "你今天不理我，明天我还是会想你，真没出息。",
    "你赢了，我满脑子都是你。",
    "举报你，偷走我心还不还。",
    "你这人挺过分的，过分让我喜欢。",
    "我生气了，要你哄才能好的那种。",
    "说吧，你到底给我下了什么蛊。",
    "我觉得咱俩挺合适的，你觉得呢？反正我觉得了。",
    "跟你待着，时间总是过得飞快，我怀疑有猫腻。",
    "你长这么好看，是要负责任的。",
    # 习惯使然型（长久的状态，不是某次具体事件）
    "遇到好听的歌，第一反应是分享给你。",
    "看到好看的风景，第一个想叫上你。",
    "遇到好玩的事，都攒着等你来了一起看。",
    "买东西的时候，总会顺手看看有没有适合你的。",
    "看到甜甜的东西就想到你，大概是条件反射。",
    "好用的东西，总想给你也备一份。",
    "听到别人夸你，比夸我自己还高兴。",
    "你的喜好，我记得比自己的还清楚。",
    "聊起你来，我能说上好半天。",
    "看到情侣款的东西，总会多看两眼。",
    "你随口说过的话，我好多都记着呢。",
    "想给你拍好多好多照片，存满整个相册。",
    "你一笑，我看什么都顺眼了。",
    "关于你的事，我都挺上心的。",
    "跟你有关的决定，我都想先听听你怎么想。",
    # 想你报备型
    "报告，今天也想你了，汇报完毕。",
    "想你了，不用回，就是通知你一声。",
    "我的日常状态：人在忙，心在你那儿。",
    "你忙你的，我在旁边想你就行。",
    "想你这件事，我从不迟到，也不请假。",
    "见你之前的每一分钟，都在想你。",
    "见完你之后，想你这件事还得继续。",
    "我把想你安排进了每天的日程，全勤。",
    "想你不需要理由，硬要一个的话，就是你。",
    "我最近怎么样？老样子，想你。",
    # 往后打算型（邀约和打算，说到就能做到）
    "周末没什么安排的话，留给我吧。",
    "等有空了，带你出去走走，地方你挑。",
    "想去哪儿玩跟我说，攻略我来做。",
    "以后想看的电影，咱们一部一部看完。",
    "你想去的地方，我都记在小本本上了。",
    "等我攒够假期，带你出去转几天。",
    "以后的周末，都想跟你一起浪费。",
    "你想学的东西，我陪你一起学。",
    "等天气好了去野餐吧，东西我来准备。",
    "以后家里的零食柜，归你管。",
    "你说了算的事，我都听你的。",
    "往后的节日我都预定了，跟你过。",
    "你想过什么样的日子，跟我说，咱们慢慢来。",
    "下次见面，先抱一下再说别的。",
    "以后吵架了，我先服软，说好了。",
    # 随口短消息型（一两句话，日常随便发）
    "在吗？想你了，没了。",
    "今天也辛苦啦，早点休息。",
    "晚安，明天见。",
    "早，今天也要开开心心的。",
    "吃饭了吗？没吃赶紧去吃。",
    "忙完了跟我说一声。",
    "到家了没？到了报个平安。",
    "今天过得怎么样？想听听。",
    "看到消息回我一下，不然我会瞎想。",
    "没什么事，就是想听听你的声音。",
    "今天累不累？累就靠一会儿。",
    "新的一天开始了，我还是喜欢你。",
    "你在忙吧？那我等你。",
    "睡了没？没睡聊会儿。",
    "就到这儿吧，明天继续喜欢你。",
]


def get_today_message():
    """随机获取一句情话"""
    msg = random.choice(love_messages)
    day_num = random.randint(1, 100)
    return msg, day_num


def get_days_together():
    """计算认识的天数"""
    start_date = datetime.date(2026, 8, 26)
    today = datetime.date.today()
    days = (today - start_date).days
    return days


def send_email():
    """发送每日情话邮件"""
    smtp_server = "smtp.qq.com"
    smtp_port = 465

    message, day_num = get_today_message()
    days = get_days_together()
    weather = get_weather()
    image_data = get_random_image()
    today_str = datetime.datetime.now().strftime('%Y年%m月%d日')
    subject = f"今日情话 认识你的第{days}天"

    # HTML邮件内容
    html = f"""\
<html>
<head>
<style>
  body {{ margin: 0; padding: 0; background: #f5f0eb; }}
  .container {{ max-width: 580px; margin: 0 auto; background: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.08); }}
  .header {{ background: linear-gradient(135deg, #f6d6d8, #e8a4ad, #d9a7b5); padding: 40px 30px; text-align: center; }}
  .header h1 {{ font-family: 'Georgia', 'Microsoft YaHei', serif; font-size: 22px; color: #fff; margin: 0; letter-spacing: 2px; text-shadow: 0 1px 4px rgba(0,0,0,0.15); }}
  .content {{ padding: 36px 30px 24px; }}
  .greeting {{ font-size: 16px; color: #8b6b6b; font-weight: bold; margin-bottom: 8px; }}
  .message {{ font-size: 17px; color: #4a4a4a; line-height: 2; margin: 16px 0; padding: 20px 24px; background: #faf5f3; border-left: 3px solid #e8a4ad; border-radius: 0 8px 8px 0; }}
  .days-box {{ text-align: center; margin: 28px 0; }}
  .days-box .num {{ font-family: 'Georgia', serif; font-size: 42px; color: #e8747f; font-weight: bold; }}
  .days-box .text {{ font-size: 14px; color: #b0a0a0; margin-top: 4px; }}
  .weather {{ font-size: 14px; color: #7a7a7a; line-height: 1.9; padding: 16px 20px; background: #f9f6f4; border-radius: 10px; margin: 20px 0; }}
  .weather-icon {{ font-size: 20px; }}
  .image-wrap {{ text-align: center; margin: 24px 0; }}
  .image-wrap img {{ max-width: 100%; border-radius: 12px; }}
  .footer {{ text-align: right; padding: 20px 30px 30px; }}
  .signature {{ font-size: 16px; color: #8b6b6b; font-weight: bold; }}
  .date {{ font-size: 13px; color: #c4b8b8; margin-top: 4px; }}
  .divider {{ border: none; border-top: 1px solid #f0e8e8; margin: 20px 0; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>每 日 情 话</h1>
  </div>
  <div class="content">
    <div class="greeting">姐姐</div>
    <div class="message">{message}</div>
    <div class="days-box">
      <div class="num">{days}</div>
      <div class="text">我 们 认 识 的 天 数</div>
    </div>
    <div class="weather">
      <span class="weather-icon">&#127780;</span> {weather}
    </div>
"""

    if image_data:
        html += '    <div class="image-wrap"><img src="cid:daily_image" /></div>'

    html += f"""\
    <hr class="divider">
    <div class="footer">
      <div class="signature">—— 你的小江</div>
      <div class="date">{today_str}</div>
    </div>
  </div>
</div>
</body>
</html>
"""

    msg = MIMEMultipart("related")
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = Header(subject, "utf-8")

    msg.attach(MIMEText(html, "html", "utf-8"))

    # 附加图片
    if image_data:
        img = MIMEImage(image_data)
        img.add_header("Content-ID", "<daily_image>")
        msg.attach(img)

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(from_addr, auth_code)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
        print(f"[{datetime.datetime.now()}] 邮件发送成功！第{day_num}天情话：{message}")
    except Exception as e:
        print(f"[{datetime.datetime.now()}] 邮件发送失败：{e}")


if __name__ == "__main__":
    send_email()
