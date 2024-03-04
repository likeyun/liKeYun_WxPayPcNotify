# liKeYun_WxPayPcNotify
微信电脑版微信支付收款监听，技术原理：通过Python实时解析微信电脑版控件的文本内容来获取信息。不需要Hook和抓包，也不是走任何的协议，就是非常简单的界面信息获取和解析。

# 如何使用？

1. 登录电脑版微信；<br/>
2. 找到微信支付公众号；<br/>
3. 双击，让微信支付公众号单独显示，如下图；<br/>
4. WxPayPcNotify.py修改你的接收通知的Url；<br/>
5. cmd运行WxPayPcNotify.py即可开启监听。<br/><br/>

<img src="https://ice.frostsky.com/2024/03/04/720b2d8b81e15bb9b32f85a290af7093.png" />

# 接收通知后端编写

WxPayPcNotify.py监听到收款通知后，会向你服务器POST三个参数：
```
amount：收款金额
sender：微信昵称
timestamp：到账时间
```
PHP接收示例：<br/>
nitify.php
```
<?php
	
	// 收款金额
	$amount = trim($_POST['amount']);

	// 微信昵称
	$sender = trim($_POST['sender']);

	// 到账时间
	$timestamp = trim($_POST['timestamp']);

	// 编写你的逻辑

?>
```



