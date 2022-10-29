import io
import json
from keep_alive import keep_alive
from datetime import datetime, timedelta

import aiohttp

from molding import common_molding,get_rule_image,common_coop_molding

from khl import Bot, Message, EventTypes, Event
from khl.card import CardMessage, Card, Module, Element, Types, Struct

from serverinfo import get_schedule
from PIL import Image
import requests
from io import BytesIO

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

async def img_requestor(img_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(img_url) as r:
            return await r.read()
# init Bot
bot = Bot(token=config['token'])


@bot.command()
async def card(msg: Message):
    c = Card(Module.Header('CardMessage'), Module.Section('convenient to convey structured information'))
    cm = CardMessage(c)  # Card can not be sent directly, need to wrapped with a CardMessage
    await msg.reply(cm)


# @bot.command()
# async def countdown(msg: Message):
#     cm = CardMessage()
#
#     c1 = Card(Module.Header('Countdown example'), color='#5A3BD7')  # color=(90,59,215) is another available form
#     c1.append(Module.Divider())
#     c1.append(Module.Countdown(datetime.now() + timedelta(hours=1), mode=Types.CountdownMode.SECOND))
#     cm.append(c1)
#
#     c2 = Card(theme=Types.Theme.DANGER)  # priority: color > theme, default: Type.Theme.PRIMARY
#     c2.append(Module.Section('the DAY style countdown'))
#     c2.append(Module.Countdown(datetime.now() + timedelta(hours=1), mode=Types.CountdownMode.DAY))
#     cm.append(c2)  # A CardMessage can contain up to 5 Cards
#
#     await msg.reply(cm)


# button example, build a card in a single statement
# btw, short code without readability is not recommended
@bot.command('查询')
async def button(msg: Message):
    P1=CardMessage()
    cr1 =Card(color='7eff00',theme=Types.Theme.INFO)
    cr1.append(Module.Context(Element.Image(src='https://cdn.wikimg.net/en/splatoonwiki/images/a/a3/S3_logo_JP_alt.png'),Element.Text('喷崽')))
    # cr1.append(Module.Context(Element.Text('喷崽')))




    cr2=Card(

            Module.Header('当前时段舞台信息查询'),
            Module.Context('点击下方按钮'),
            Module.ActionGroup(
                # RETURN_VAL type(default): send an event when clicked, see print_btn_value() defined at L58
                Element.Button('排排', 'now_op', Types.Click.RETURN_VAL),
                Element.Button('工工', 'now_sr', Types.Click.RETURN_VAL, theme=Types.Theme.DANGER)),
            Module.Divider(),
            Module.Header('下一时段舞台信息查询'),
            Module.Context('点击下方按钮'),
            Module.ActionGroup(
                # RETURN_VAL type(default): send an event when clicked, see print_btn_value() defined at L58
                Element.Button('排排', 'next_op', Types.Click.RETURN_VAL),
                Element.Button('工工', 'next_sr', Types.Click.RETURN_VAL, theme=Types.Theme.DANGER)),
            Module.Section(
                '享受游戏，快乐喷喷~',
                # LINK type: user will open the link in browser when clicked
                Element.Button('安利视频',
                               'https://www.bilibili.com/video/BV11T4y1r7ix/?spm_id_from=333.337.search-card.all.click',
                               Types.Click.LINK)))
    P1.append(cr1)
    P1.append(cr2)

    await msg.reply(P1)





@bot.on_event(EventTypes.MESSAGE_BTN_CLICK)

async def print_btn_value(b: Bot, e: Event):

    print(str(e.body))
    print(f'''{e.body['user_info']['nickname']} 点击了 {e.body['value']} 按钮''')
    val = e.body['value']


    if val == 'now_op':
        info = get_schedule('bankara-open', 'now')
        com_info = common_molding(info)


        # 地图1
        stages_img_1 = Image.open(io.BytesIO(await img_requestor(com_info[5][0])))
        imgByteArr1 = io.BytesIO()
        stages_img_1.save(imgByteArr1, format='PNG')
        imgByte = imgByteArr1.getvalue()
        stages_img_1_src = await  bot.client.create_asset(imgByte)
        # 地图2
        stages_img_2 = Image.open(io.BytesIO(await img_requestor(com_info[5][1])))
        imgByteArr2 = io.BytesIO()
        stages_img_2.save(imgByteArr2, format='PNG')
        imgByte = imgByteArr2.getvalue()
        stages_img_2_src = await  bot.client.create_asset(imgByte)
        # 模式图
        rule_img_temp=get_rule_image(com_info[3])
        rule_img=Image.open(io.BytesIO(await img_requestor(rule_img_temp)))
        imgByteArr3 = io.BytesIO()
        rule_img.save(imgByteArr3, format='PNG')
        imgByte = imgByteArr3.getvalue()
        rule_img_src = await  bot.client.create_asset(imgByte)
        # info_text= f'''时段：{com_info['strat-time']}\n地图{com_info['stages']}\n'''


        cmr = CardMessage()
        cr = Card(theme=Types.Theme.INFO,color='A281B7')
        cr.append(Module.Header('当前时段'))
        cr.append(Module.Context(Element.Text(f"{com_info[1]}~{com_info[2]}")))
        cr.append( Module.Divider())
        cr2 =Card(theme=Types.Theme.INFO,color='ff7213')

        cr2.append(Module.Section(text="真格（开放）\n\n"
                                  '模式 :     'f'''{com_info[3]}\n\n'''
                                  f'''{com_info[4][0]}   /   {com_info[4][1]}'''


                                  ,accessory= Element.Image(src=rule_img_src,size=Types.Size.SM),mode=Types.SectionMode.RIGHT))
        cr2.append(Module.Divider())
        cr2.append( Module.ImageGroup(Element.Image(src=stages_img_1_src),Element.Image(src=stages_img_2_src)))
        cmr.append(cr)
        cmr.append(cr2)






        channel = await bot.client.fetch_public_channel(e.body['target_id'])
        await b.client.send (channel, cmr)
    if val == 'next_op':
        info = get_schedule('bankara-open', 'next')
        com_info = common_molding(info)

        # 地图1
        stages_img_1 = Image.open(io.BytesIO(await img_requestor(com_info[5][0])))
        imgByteArr1 = io.BytesIO()
        stages_img_1.save(imgByteArr1, format='PNG')
        imgByte2 = imgByteArr1.getvalue()
        stages_img_1_src = await  bot.client.create_asset(imgByte2)
        print(stages_img_1_src)
        # 地图2
        stages_img_2 = Image.open(io.BytesIO(await img_requestor(com_info[5][1])))
        imgByteArr2 = io.BytesIO()
        stages_img_2.save(imgByteArr2, format='PNG')
        imgByte2 = imgByteArr2.getvalue()
        stages_img_2_src = await  bot.client.create_asset(imgByte2)
        print(stages_img_2_src)
        # 模式图
        rule_img_temp = get_rule_image(com_info[3])
        print(rule_img_temp)
        print(com_info[3])
        rule_img = Image.open(io.BytesIO(await img_requestor(rule_img_temp)))
        imgByteArr3 = io.BytesIO()
        rule_img.save(imgByteArr3, format='PNG')
        imgByte2 = imgByteArr3.getvalue()
        rule_img_src = await  bot.client.create_asset(imgByte2)
        # info_text= f'''时段：{com_info['strat-time']}\n地图{com_info['stages']}\n'''

        cmb = CardMessage()
        cb = Card(theme=Types.Theme.INFO, color='A281B7')
        cb.append(Module.Header('下一时段'))
        cb.append(Module.Context(Element.Text(f"{com_info[1]}~{com_info[2]}")))
        cb.append(Module.Divider())
        cb2 = Card(theme=Types.Theme.INFO, color='ff7213')

        cb2.append(Module.Section(text="真格（开放）\n\n"
                                       '模式 :     'f'''{com_info[3]}\n\n'''
                                       f'''{com_info[4][0]}   /   {com_info[4][1]}'''

                                  , accessory=Element.Image(src=rule_img_src, size=Types.Size.SM),
                                  mode=Types.SectionMode.RIGHT))
        cb2.append(Module.Divider())
        cb2.append(Module.ImageGroup(Element.Image(src=stages_img_1_src), Element.Image(src=stages_img_2_src)))
        cmb.append(cb)
        cmb.append(cb2)

        channel = await bot.client.fetch_public_channel(e.body['target_id'])
        await b.client.send(channel, cmb)



    if val == 'now_sr':
        info = get_schedule('coop-grouping-regular', 'now')
        com_info = common_coop_molding(info)
        print(f'''{com_info}''')
        # 地图1
        stages_img_1 = Image.open(io.BytesIO(await img_requestor(com_info[3])))
        imgByteArr1 = io.BytesIO()
        stages_img_1.save(imgByteArr1, format='PNG')
        imgByte2 = imgByteArr1.getvalue()
        stages_img_1_src = await  bot.client.create_asset(imgByte2)
        print(stages_img_1_src)
        print(com_info[4][3])
        # 武器图
        stages_img_2 = Image.open(io.BytesIO(await img_requestor(com_info[4][1])))
        imgByteArr2 = io.BytesIO()
        stages_img_2.save(imgByteArr2, format='PNG')
        weapon1 = imgByteArr2.getvalue()
        weap_img1 = await  bot.client.create_asset(weapon1)
        print(weap_img1)
        stages_img_2 = Image.open(io.BytesIO(await img_requestor(com_info[4][3])))
        imgByteArr2 = io.BytesIO()
        stages_img_2.save(imgByteArr2, format='PNG')
        weapon2 = imgByteArr2.getvalue()
        weap_img2 = await  bot.client.create_asset(weapon2)

        stages_img_2 = Image.open(io.BytesIO(await img_requestor(com_info[4][5])))
        imgByteArr2 = io.BytesIO()
        stages_img_2.save(imgByteArr2, format='PNG')
        weapon3 = imgByteArr2.getvalue()
        weap_img3 = await  bot.client.create_asset(weapon3)

        stages_img_2 = Image.open(io.BytesIO(await img_requestor(com_info[4][7])))
        imgByteArr2 = io.BytesIO()
        stages_img_2.save(imgByteArr2, format='PNG')
        weapon4 = imgByteArr2.getvalue()
        weap_img4 = await  bot.client.create_asset(weapon4)


        # 模式图

        rule_img = Image.open(io.BytesIO(await img_requestor("https://cdn.wikimg.net/en/splatoonwiki/images/2/21/S3_SRNW_logo.png")))
        imgByteArr3 = io.BytesIO()
        rule_img.save(imgByteArr3, format='PNG')
        imgByte2 = imgByteArr3.getvalue()
        rule_img_src = await  bot.client.create_asset(imgByte2)
        # info_text= f'''时段：{com_info['strat-time']}\n地图{com_info['stages']}\n'''

        cmb = CardMessage()
        cb = Card(theme=Types.Theme.INFO, color='A281B7')
        cb.append(Module.Header('当前时段'))
        cb.append(Module.Context(Element.Text(f"{com_info[0]}~{com_info[1]}")))
        cb.append(Module.Divider())
        cb2 = Card(theme=Types.Theme.INFO, color='f02c7d')

        cb2.append(Module.Section(text=f"地图 ： {com_info[2]}\n\n"
                                       '武器 :   'f'''{com_info[4][0]}   {com_info[4][2]}\n\n'''
                                                f'''{com_info[4][4]}    {com_info[4][6]}'''

                                  , accessory=Element.Image(src=rule_img_src, size=Types.Size.SM),
                                  mode=Types.SectionMode.RIGHT))
        cb2.append(Module.Divider())
        cb2.append(Module.Container(Element.Image(src=stages_img_1_src)))
        cb2.append(Module.ImageGroup(Element.Image(src=weap_img1), Element.Image(src=weap_img2),Element.Image(src=weap_img3),Element.Image(src=weap_img4)))
        cmb.append(cb)
        cmb.append(cb2)

        channel = await bot.client.fetch_public_channel(e.body['target_id'])
        await b.client.send(channel, cmb)
    if val == 'next_sr':
        info = get_schedule('coop-grouping-regular', 'next')
        com_info = common_coop_molding(info)
        print(f'''{com_info}''')
        # 地图1
        stages_img_1 = Image.open(io.BytesIO(await img_requestor(com_info[3])))
        imgByteArr1 = io.BytesIO()
        stages_img_1.save(imgByteArr1, format='PNG')
        imgByte2 = imgByteArr1.getvalue()
        stages_img_1_src = await  bot.client.create_asset(imgByte2)
        print(stages_img_1_src)
        print(com_info[4][3])
        # 武器图
        stages_img_2 = Image.open(io.BytesIO(await img_requestor(com_info[4][1])))
        imgByteArr2 = io.BytesIO()
        stages_img_2.save(imgByteArr2, format='PNG')
        weapon1 = imgByteArr2.getvalue()
        weap_img1 = await  bot.client.create_asset(weapon1)
        print(weap_img1)
        stages_img_2 = Image.open(io.BytesIO(await img_requestor(com_info[4][3])))
        imgByteArr2 = io.BytesIO()
        stages_img_2.save(imgByteArr2, format='PNG')
        weapon2 = imgByteArr2.getvalue()
        weap_img2 = await  bot.client.create_asset(weapon2)

        stages_img_2 = Image.open(io.BytesIO(await img_requestor(com_info[4][5])))
        imgByteArr2 = io.BytesIO()
        stages_img_2.save(imgByteArr2, format='PNG')
        weapon3 = imgByteArr2.getvalue()
        weap_img3 = await  bot.client.create_asset(weapon3)

        stages_img_2 = Image.open(io.BytesIO(await img_requestor(com_info[4][7])))
        imgByteArr2 = io.BytesIO()
        stages_img_2.save(imgByteArr2, format='PNG')
        weapon4 = imgByteArr2.getvalue()
        weap_img4 = await  bot.client.create_asset(weapon4)


        # 模式图

        rule_img = Image.open(io.BytesIO(await img_requestor("https://cdn.wikimg.net/en/splatoonwiki/images/2/21/S3_SRNW_logo.png")))
        imgByteArr3 = io.BytesIO()
        rule_img.save(imgByteArr3, format='PNG')
        imgByte2 = imgByteArr3.getvalue()
        rule_img_src = await  bot.client.create_asset(imgByte2)
        # info_text= f'''时段：{com_info['strat-time']}\n地图{com_info['stages']}\n'''

        cmb = CardMessage()
        cb = Card(theme=Types.Theme.INFO, color='A281B7')
        cb.append(Module.Header('下一时段'))
        cb.append(Module.Context(Element.Text(f"{com_info[0]}~{com_info[1]}")))
        cb.append(Module.Divider())
        cb2 = Card(theme=Types.Theme.INFO, color='f02c7d')

        cb2.append(Module.Section(text=f"地图 ： {com_info[2]}\n\n"
                                       '武器 :   'f'''{com_info[4][0]}   {com_info[4][2]}\n\n'''
                                                f'''{com_info[4][4]}    {com_info[4][6]}'''

                                  , accessory=Element.Image(src=rule_img_src, size=Types.Size.SM),
                                  mode=Types.SectionMode.RIGHT))
        cb2.append(Module.Divider())
        cb2.append(Module.Container(Element.Image(src=stages_img_1_src)))
        cb2.append(Module.ImageGroup(Element.Image(src=weap_img1), Element.Image(src=weap_img2),Element.Image(src=weap_img3),Element.Image(src=weap_img4)))
        cmb.append(cb)
        cmb.append(cb2)

        channel = await bot.client.fetch_public_channel(e.body['target_id'])
        await b.client.send(channel, cmb)

# struct example
@bot.command()
async def struct(msg: Message):
    await msg.reply(CardMessage(Card(Module.Section(Struct.Paragraph(3, 'a', 'b', 'c')))))


# @bot.on_event(EventTypes.MESSAGE_BTN_CLICK)
# async def print_btn_value(_: Bot, e: Event):
#     print(f'''{e.body['user_info']['nickname']} took the {e.body['value']} pill''')


# everything done, go ahead now!
keep_alive()
bot.run()
