

import datetime



def time_molding(p1):
    _time = datetime.datetime.strptime(p1, '%Y-%m-%dT%H:%M:%S%z')
    time = _time.strftime('%m/%d %H:%M')
    return time
def common_molding(f):
    is_fest = f["is_fest"]
    st = f["start_time"]
    et = f["end_time"]
    rule_name = f["rule"]["name"]
    if f["rule"]["name"] =='ガチエリア':
        rule_name ="区域模式"
    elif f["rule"]["name"] =="ガチヤグラ":
        rule_name = "推塔模式"
    elif f["rule"]["name"] == "ガチホコバトル":
        rule_name ="鱼虎模式"
    elif f["rule"]["name"] =="ガチアサリ":
        rule_name="蛤蜊模式"
    else:
        rule_name ="打工崽"
    stages = []
    imgs = []
    for stage in f["stages"]:
        stages.append(stage["name"])
        imgs.append(stage["image"])

    start_time = time_molding(st)
    end_time = time_molding(et)

    return [is_fest, start_time, end_time, rule_name, stages, imgs]

def common_coop_molding(f):
    st = f["start_time"]
    et = f["end_time"]
    stage = f["stage"]["name"]
    image = f["stage"]["image"]

    start_time = time_molding(st)
    end_time = time_molding(et)

    weapons = []
    for weapon in f["weapons"]:
        weapons.append(weapon["name"])
        weapons.append(weapon["image"])
    return[start_time, end_time, stage, image, weapons]
def get_rule_image(p1):
    rule_images = {
        "ナワバリバトル": "https://images-ext-1.discordapp.net/external/sNH8hPsRSuUYU7eMhUebaL7v8I3q82OepAd-vN_5sWE/https/www.nintendo.co.jp/switch/aab6a/assets/images/battle-sec01_logo.png",
        "バンカラマッチ": "https://media.discordapp.net/attachments/808221718106603540/812571951872081920/battle-sec02_logo.png",
        "打工崽": "https://cdn.wikimg.net/en/splatoonwiki/images/8/84/SplatNet_2_icon_Salmon_Run.png",
        "区域模式": "https://cdn.wikimg.net/en/splatoonwiki/images/3/38/S3_icon_Splat_Zones.png",
        "推塔模式": "https://cdn.wikimg.net/en/splatoonwiki/images/b/bc/S3_icon_Tower_Control.png",
        "鱼虎模式": "https://cdn.wikimg.net/en/splatoonwiki/images/1/12/S3_icon_Rainmaker.png",
        "蛤蜊模式": "https://cdn.wikimg.net/en/splatoonwiki/images/e/e3/S3_icon_Clam_Blitz.png"
    }
    return rule_images.get(p1)