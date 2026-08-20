---
title: "Debian 13 NFS挂载群晖NAS共享文件夹"
published: 2026-05-08
description: ""
image: "/assets/images/article-covers/study-desk.jpg"
tags: ["工具", "网络"]
category: "技术分享"
draft: false
---

环境信息
- **Linux Server**: Debian 13 — `172.16.1.67`
- **群晖 NAS**: `172.16.180.99`
- **共享文件夹**: `OpenClaw_StickMan`
- **本地挂载点**: `/mnt/Synology`
## 背景

在Debian 13安装了openclaw，为了openclaw可以访问nas共享文件夹以实现内网的文件共享管理，但是通过 SMB/CIFS 协议挂载群晖共享文件夹时，在持续报 `STATUS_LOGON_FAILURE (0xc000006d)` 认证失败错误，即使凭证正确也无法连接，在同网段的windows server通过SMB协议挂载也没有问题。最终改用 **NFS 协议** 成功解决。

---

## 第一步：群晖 DSM 端配置

1. 进入 **控制面板 → 文件服务 → NFS**，启用 NFS 服务
1. 进入 **控制面板 → 共享文件夹**，选择 `OpenClaw_StickMan` → **编辑 → NFS 权限**
1. 点击 **新增**，填写规则：
  - 服务器名称或 IP：`172.16.1.67`
  - 权限：**读写**
  - Squash：**映射为 admin**

---

## 第二步：Linux 安装 NFS 客户端

```bash
sudo apt install -y nfs-common
```

---

## 第三步：创建挂载点并挂载

```bash
# 创建挂载目录
sudo mkdir -p /mnt/Synology

# 执行挂载
sudo mount -t nfs 172.16.180.99:/volume1/OpenClaw_StickMan /mnt/Synology
```

没有输出就是成功

---

## 第四步：验证挂载

```bash
# 查看挂载信息
df -h /mnt/Synology

# 查看文件列表
ls -la /mnt/Synology
```

预期输出示例：
```
文件系统                                  大小  已用  可用 已用% 挂载点
172.16.180.99:/volume1/OpenClaw_StickMan   21T  5.2T   16T   25% /mnt/Synology
```

---

## 第五步：配置开机自动挂载

将挂载信息写入 `/etc/fstab`：
```bash
echo '172.16.180.99:/volume1/OpenClaw_StickMan /mnt/Synology nfs defaults,_netdev 0 0' | sudo tee -a /etc/fstab
```

验证 fstab 配置是否正确：
```bash
sudo mount -a
```

无输出即表示配置正确，重启后会自动挂载。

---

## 常用命令速查

| 操作 | 命令 |
|------|------|
| 手动挂载 | `sudo mount -t nfs 172.16.180.99:/volume1/OpenClaw_StickMan /mnt/Synology` |
| 手动卸载 | `sudo umount /mnt/Synology` |
| 查看挂载状态 | `df -h /mnt/Synology` |
| 查看所有 NFS 挂载 | `mount -t nfs4` |

以上就是本次debian 13挂载nfs的操作，特别感谢claude，相关指令基本基于claude的指导，但是SMB无法挂载的问题目前还是无法定位
