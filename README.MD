# Splakook喷崽
A  KOOK-Bot for Splatoon3 stage information search
用于Splatoon3当前和下一时段舞台信息查询的KOOK bot



打开"config.json"输入机器人token

机器人token获取方式：https://developer.kookapp.cn/app/index
点击右上角"新建应用"=>填写"应用名称"和"应用简介"=>进入创建好的应用界面
在左边侧边栏选择"机器人"=>会看见"机器人链接模式"=>下方有一串"Token"


频道id的获取方式：先打开"KOOK"点击个人设置=>"高级设置"=>打开"开发者模式"选项
在你需要用以机器人回复的频道上右键单击=>选择"复制ID"


=========================================================
# 如何运行机器人

浏览器打开 https://replit.com/ 网站，注册并登录
点击左边侧边栏上方的"+ Create"创建一个新的程式
将我编写的所有文件拖拽进"Files"列表
点击正上方的"RUN"=>此时右侧会新建一个窗口"Webview"=>复制地址栏中的URL

浏览器打开 https://uptimerobot.com/ 注册并登录
点击左上方"+ Add New Monitor"=>
{
	Monitor选择"HTTP(s)"
	Friendly Name:随便输入
	URL(or IP):填写刚才在replit中复制的URL
	勾选右边的邮箱(在机器人掉线的时候会以邮件的方式通知你)
}
最后点击右下角的"Save Changes"保存设置就可以了

=========================================================
# relate
Splatoon3 api：https://spla3.yuu26.com/
KOOK sdk：https://github.com/TWT233/khl.py