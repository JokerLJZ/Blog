---
title: "群晖配置Flexget套件"
published: 2025-12-04
description: "群晖的Flexget套件安装配置教程"
tags: ["工具", "推荐"]
category: "技术分享"
draft: false
---

>  因为玩PT所以还是需要通过flexget来进行种子管理，本文是群晖安装flexget套件与配置的教程，主要分为安装flexget套件，获取root权限，修改webui密码，configuration几个步骤

# flexget安装

通过群晖的社区套件直接安装即可，套件版本有webui，但是目前没有webui的密码，基本上社区套件的使用都卡在这步了，配置起来没有docker方便，所以还是推荐docker安装
![](/posts/DSM-Flexget/img-001.jpg)

## 获取群晖root权限

首先在群晖的终端设置中打开SSH功能，默认的22端口无需修改，这里不再截图，教程很多，然后就是ssh登录群晖系统，windows使用putty，mac可以使用terminal直接ssh登录，指令如下：
```shell
ssh admin@"your_ip"
```

ssh的账号密码就是你在群晖设置的管理员账号密码，登录后通过以下指令获取root操作权限，密码还是管理员的密码，如果想修改root密码，可以参考该教程：[群晖 | 最新获取root权限设置root密码方法-VUM星球](https://www.vumstar.com/1264/)
```shell
sudo -i
```

![](/posts/DSM-Flexget/img-002.png)

## 修改webui密码

根据flexget的官方教程是给了配置指令，但是相关文件的路径我发现跟指令的不一致，通过查询定位到了配置文件的目录，config.yml是在@appdata下的flexget目录下，具体指令修订如下，volumex是你的存储池编号，根据实际情况修改，我是在volume2，大多数应该是在volume1
```shell
 /volume1/@appstore/flexget/env/bin/flexget -c /volume1/@appdata/flexget/config.yml web passwd "your_password"
```

修改完成后会显示updated password，而且会同时初始化配置文件，可以查到新增了sqlite等文件
![](/posts/DSM-Flexget/img-003.png)

## configuration

配置的话通过webui就可以直接配置config.yml，甚至还有语法校验，非常方便，现在有schedule等功能，不像十几年前还需要通过crontab去做定时任务，配置好config后可以直接在webui execute验证，也可以查log
# 🤗 总结归纳

如果会用docker推荐用docker安装flexget，就是国内源经常有问题，所以提供一个套件的配置教程，有问题可以留言~
