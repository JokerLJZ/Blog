---
title: "小米路由器局域网科学上网"
published: 2025-12-12
description: "小米路由器配置 ShellClash（ShellCrash）实现全屋透明代理的折腾记录"
tags: ["工具", "网络"]
category: "技术分享"
draft: false
---

## 硬件与工具

路由器：小米路由器AX3000，固件版本1.0.46

小米路由器SSH一键开启工具：[xmir-patcher](https://github.com/openwrt-xiaomi/xmir-patcher)

ShellClash(VPN工具)：[ShellCrash](https://github.com/juewuy/ShellCrash)

Putty(ssh)：[Putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)

Winscp(ftp)：[WinSCP](https://winscp.net/eng/index.php)

VPN：[VPN](https://xn--gmq396grzd.com/)

---

## 操作步骤

### 解锁路由器SSH

小米路由器的系统也是基于OpenWRT，属于linux系统，但是锁了SSH，查了一下主要有三种解锁SSH的方式

- 刷小米官方的开发版rom，然后用官方提供的开通SSH工具，但是开发版已经不太维护了，不建议这样操作
- 通过算号工具通过设备的SN计算出root密码，然后通过telnet使用root权限登录后打开SSH，参考教程[用路由器实现全屋科学上网 | CGArtLab](https://cgartlab.com/posts/how-to-setup-full-home-science-internet/)
- 通过 [xmir-patcher](https://github.com/openwrt-xiaomi/xmir-patcher) 一键解锁SSH，小米路由器默认已经有python环境，win和mac分别运行run.bat和run.sh，过一会就自动解锁成功，密码也是root

### SSH安装Shellclash

win可以用putty ssh登录到路由器，账户root，密码root，mac可以直接用terminal登录，一般小米路由器的地址默认是192.168.31.1

```shell
#mac终端SSH登录指令
ssh root@192.168.31.1
```

![](/posts/Router-VPN/img-001.png)

出现以上界面就是SSH登录成功，下一步就可以安装shellclash了，[ShellCrash](https://github.com/juewuy/ShellCrash)提供了一键安装的脚本，直接粘贴运行即可，如因网络问题安装失败多试几次即可，我大概试了十几次 🤣

```shell
#jsDelivrCDN源
export url='https://testingcf.jsdelivr.net/gh/juewuy/ShellCrash@master' && sh -c "$(curl -kfsSl $url/install.sh)" && source /etc/profile &> /dev/null
```

安装完成后会有提示，只需要输入crash就可以进入配置，你没看错，就是crash而不是clash因为clash被设置为屏蔽词了，曲线救国，运行后如下界面就可以开始配置了

![](/posts/Router-VPN/img-002.png)

### Shellclash配置

正常可以通过在线获取完整配置文件进行网络配置，但是不知道为什么我的clash订阅地址生成配置文件不成功，没办法只能手动下载VPN服务商提供的配置文件，使用winscp通过SCP协议上传config.yaml到/tmp，选择本地上传配置文件后脚本可以自动识别并生成配置文件，其他的我全部都设置默认启动服务就完成了配置并启动服务

![](/posts/Router-VPN/img-003.png)

启动服务后可以安装一个本地的dashboard，方便webui进行clash的配置，操作方式是进入crash后选9→4，随便选一个安装，建议安装YACD-meta，安装完成后就可以从[192.168.31.1/ui](http://192.168.31.1:9999/ui)进入面板进行crash的配置，可以根据实际需要配置代理规则以及选择服务器

![](/posts/Router-VPN/img-004.png)

## 使用感受

科学上网会方便很多不用去终端安装shadowsocks，但是不知道是路由器性能问题还是代理模式的问题，开了shellclash会出现wifi信号断连的情况，这个问题原因还有待研究，目前看想稳定的在路由器使用代理最好还是直接刷openwrt，现在日常使用我还是关了clash，所以感觉白折腾了一遭
