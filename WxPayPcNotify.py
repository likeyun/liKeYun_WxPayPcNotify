import re
import time
import uiautomation as automation
import requests

last_matched_info = None

def explore_control(control, depth, target_depth):
    global last_matched_info
    try:
        name = control.Name
        if name:
            if depth == target_depth:
                # 匹配收款金额信息
                match = re.search(r'收款金额￥([\d.]+)', name)
                if match:
                    global amount
                    amount = match.group(1)
                    last_matched_info = f"收款金额: ￥{amount}, "

                # 匹配来自、到账时间信息
                match = re.search(r'来自(.+?)到账时间(.+?)备注', name)
                if match:
                    global sender
                    sender = match.group(1)
                    global timestamp
                    timestamp = match.group(2)
                    last_matched_info += f"来自: {sender}, 到账时间: {timestamp}"
                return
        # 递归处理子控件
        for child in control.GetChildren():
            explore_control(child, depth + 4, target_depth)
    except Exception as e:
        print(f"发生错误: {str(e)}")

def process_wechat_window(wechat_window, prev_info):
    global last_matched_info
    if wechat_window.Exists(0):
        explore_control(wechat_window, 0, 60)
        if last_matched_info and last_matched_info != prev_info:
            print(last_matched_info)
            print("-----------------------------------------------------------------")
            print("持续监听中...")
            print("-----------------------------------------------------------------")
            prev_info = last_matched_info
            
            # 向服务器发送请求
            send_http_request(last_matched_info,amount,sender,timestamp)

    else:
        print("无法获取到窗口，请保持微信支付窗口显示...")
    return prev_info

def send_http_request(info,amount,sender,timestamp):

    # 接收通知的Url
    server_url = 'https://www.yourdomain.com/notify.php'
    try:
        # 将金额、来自、到账时间POST给服务器
        response = requests.post(server_url, data={'amount': amount,'sender': sender,'timestamp': timestamp})
        # 通知成功
        # print("通知成功")
    except Exception as e:
        # 通知失败
        print(f"通知服务器失败...: {str(e)}")

def main():
    global last_matched_info
    prev_info = None
    try:
        # 获取微信窗口
        wechat_window = automation.WindowControl(searchDepth=1, ClassName='ChatWnd')
        prev_info = process_wechat_window(wechat_window, prev_info)
    except Exception as e:
        print(f"发生错误: {str(e)}")

    while True:
        try:
            # 持续监听微信窗口
            wechat_window = automation.WindowControl(searchDepth=1, ClassName='ChatWnd')
            prev_info = process_wechat_window(wechat_window, prev_info)
        except Exception as e:
            print(f"发生错误: {str(e)}")

        time.sleep(2)

if __name__ == "__main__":
    print("-----------------------------------------------------------------")
    print("欢迎使用liKeYun_ZsmPay微信电脑版收款监控脚本...")
    print("-----------------------------------------------------------------")
    main()
