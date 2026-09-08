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
love_messages = [
    # 温暖关心型（不依赖天气/事件，任何时候都成立）
    "记得按时吃饭，别总是忙到忘了吃。",
    "晚上别熬太晚，早点休息。",
    "工作再忙也要照顾好自己。",
    "出门前记得检查有没有忘带东西。",
    "别总是坐着不动，隔段时间起来活动一下。",
    "有什么不开心的事，记得跟我说。",
    "别太拼了，累了就歇会儿。",
    "早饭一定要吃，别空着肚子出门。",
    "别总低头看手机，对颈椎不好。",
    "少喝点咖啡，对睡眠不好。",
    "有什么事别一个人闷着，还有我呢。",
    "坐久了站起来走走，别老弯着腰。",
    "眼睛累了就闭会儿，别老盯着屏幕。",
    "你有空的话出去走走，别老在屋里待着。",
    "别总点外卖，有时间自己做点吃的。",

    # 真诚表白型
    "今天突然很想你，没什么特别的理由。",
    "想到下班就能见到你，一整天都有盼头。",
    "跟你在一起之后，日子好像过得特别快。",
    "你不在我身边的时候，总觉得少了点什么。",
    "喜欢看你笑的样子，比什么都好看。",
    "有时候什么也不做，就静静待在你旁边，就挺好的。",
    "你说话的时候我可能没回，但我都有在听。",
    "跟你在一起，连发呆都变得有意思了。",
    "看到好看的东西，第一反应就是想拍给你看。",
    "你不在的时候，我连说话的人都没有。",
    "总觉得你比你自己认为的要好得多。",
    "跟你聊完天之后，心情会好很久。",
    "其实每天都想你，只是今天忍不住说了出来。",
    "你笑起来的声音，是我最想反复听到的。",
    "有你在的日子，我觉得生活特别踏实。",

    # 俏皮幽默型
    "你是不是偷偷给我施了什么法术？不然怎么老想你。",
    "今天的我也很喜欢你，明天的我应该也是。",
    "你要是再这么可爱下去，我可就管不住自己了。",
    "跟你说，我今天又想你了一遍，不用谢。",
    "我算了一下，今天喜欢你的程度比昨天多了0.01%。",
    "如果你是好吃的，我一定舍不得吃，但会一直看着你。",
    "今天的我依然是你的，不接受退货。",
    "我觉得你应该赔我精神损失费，害我一天到晚走神想你。",
    "你属于哪种类型？我喜欢的类型。",
    "我把你的名字写在了心里，擦不掉了，你说怎么办吧。",
    "如果想你算加班的话，我已经严重超时了。",
    "你是不是会读心术？不然怎么每次都让我心动。",
    "我今天做了一个决定，继续喜欢你。",
    "我怀疑你喜欢我，不然我为什么这么喜欢你。",
    "如果喜欢你是种病，那我打算一直不治了。",

    # 走心文艺型
    "你在身边的时候，连空气都变得温柔了。",
    "和你走过的那条路，我后来一个人走的时候，觉得变长了。",
    "你说过的有些话，我其实一直记着。",
    "有些话当面说不出口，但确实是真的。",
    "看见好看的晚霞会想拍给你看，这就是喜欢吧。",
    "你在的时候，时间好像都慢了下来。",
    "我不是很会说好听的话，但我的心是真的。",
    "以前觉得一个人也挺好的，后来遇见了你，就不觉得了。",
    "你是我所有不期而遇里，最想留下来的那一个。",
    "有些感情说不清楚，但我知道它一直在那儿。",

    # 深情承诺型
    "以后不管怎样，我都在。",
    "你不用什么都自己扛着，还有我呢。",
    "不管发生什么，先跟我说，我们一起想办法。",
    "你开心的时候我陪你笑，难过的时候我陪你待着。",
    "有些事不用急，我们慢慢来，日子长着呢。",
    "你做的决定我都支持你，哪怕我不完全懂。",
    "我不会说什么甜言蜜语，但我会一直在你身边。",
    "你要是想休息，就歇着，有我在。",
    "你不用特意为我改变什么，现在的你就挺好。",
    "有什么委屈跟我说，别憋在心里。",
    "不管多晚，你回来就行，我给你留灯。",
    "你往前走就行，我在后面跟着，哪儿也不去。",
    "你要是累了就靠靠我，反正我也跑不了。",
    "我这人没什么优点，但对你，还算靠谱。",
    "往后的日子，我陪你一起过。",

    # 平淡生活型
    "我在学做菜了，等学会了做给你吃。",
    "我看到一家店感觉你会喜欢，下次带你去。",
    "我想好了，周末带你出去走走。",
    "我最近发现了一部好看的剧，想和你一起追。",
    "我把你之前说想吃的那几样都记着呢，慢慢做给你。",
    "我在学做你爱吃的菜了，就是还不太成功。",
    "以后家里的碗我来洗，你就负责坐着就行。",
    "我最近在研究怎么做甜点，做好了第一个给你尝。",
    "以后咱们有空就去逛超市，买一堆零食回来。",
    "我已经想好了，下次一起去那个你说想去的地方。",
    "等有空了，我们一起去爬山吧，就当锻炼身体。",
    "我在攒假，到时候带你出去玩几天。",
    "以后周末就别加班了，留给我吧。",
    "我想好了，以后做饭的事我来，你打下手就行。",
    "我把你想看的电影都加进收藏夹了，有空一起看。",

    # 随性自然型
    "我就是想跟你说一声，我喜欢你。",
    "没什么事，就是想你了。",
    "今天也是喜欢你的一天。",
    "你不在，我连话都不知道跟谁说。",
    "有你在的时候，我觉得什么都不难。",
    "你是我每天最想见到的人。",
    "想跟你一起过每一个普通的日子。",
    "你在，就够了。",
    "有你在我身边，我什么都不怕。",
    "我只想跟你待在一起，做什么都行。",
    "跟你在一起的时候，什么烦恼都忘了。",
    "你是我平淡日子里最特别的那一个。",
    "没有什么特别的，就是想跟你说说话。",
    "每天最开心的事，就是见到你。",
    "你在身边，就是最好的日子。",
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
    <div class="greeting">亲爱的甜甜姐姐，</div>
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
