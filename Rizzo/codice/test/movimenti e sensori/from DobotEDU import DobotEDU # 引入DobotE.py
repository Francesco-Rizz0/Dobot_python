from DobotEDU import DobotEDU

dobotEdu = DobotEDU()  # DobotEDU类实例化，未传参时只可调用机械臂API，AI API不可用
# eg：dobotEdu = DobotEDU(account="xiaoming", password="123456")  如需调用AI API可询问技术支持拿到可用的账户名和密码


# 机械臂API演示
def main():
    res = dobotEdu.magician.search_dobot()  # 调用search_dobot接口，搜索机械臂接口，返回接口列表
    print("搜索到的接口结果：", res)
    port_name = res[0]["portName"]  # 选择可用机械臂接口，默认选择第一个，出现问题用户需要确认是否连接的是机械臂接口
    dobotEdu.magician.connect_dobot(
        port_name=port_name)  # 调用connect_dobot，连接机械臂，成功返回true
    while True:
        dobotEdu.magician.set_ptpcmd(port_name, 0, 230, 50, 0, 20, True,
                                     True)  # 调用set_ptpcmd接口，机械臂PTP运动
        dobotEdu.magicbox.set_homecmd(port_name, True, True)


if __name__ == '__main__':
    main()
'''
# AI API接口调用演示
result = dobotEdu.speech.synthesis(
    "你好，很高兴见到你",
    "zh",
    1,
    {
        "vol": 5,  # 音量
        "spd": 2,  # 音速
        "pit": 9,  # 语调
        "per": 0  # 0：女声  1：男声
    })
print(result)
'''