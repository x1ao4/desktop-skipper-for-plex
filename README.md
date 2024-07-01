# Desktop Skipper for Plex <a name="desktop-skipper-for-plex-zh"></a>
<a href="#desktop-skipper-for-plex-en">Switch to English</a>

Plex 在 2023 年 10 月为部分播放端增加了自动跳过片头、自动跳过片尾及自定义播放下一个倒计时时长等[功能](https://forums.plex.tv/t/player-experience/857990)，遗憾的是桌面端的 Plex for Windows/Mac 至今依然没有增加这些功能，你依然需要手动点击跳过按钮，并且需要等待 10 秒的倒计时才会自动播放下一个项目。

由于 Plex for Windows/Mac 的远程控制功能在很久之前就被[移除](https://forums.plex.tv/t/plex-for-mac-windows-and-linux/446435/63)了，所以我们也无法通过 API 或其他方式来远程控制这些播放器。我没有找到任何支持 Plex for Windows 或 Plex for Mac 的自动化工具，于是自己编写了这个脚本。

当你在 Plex for Windows/Mac 上观看视频时，使用 Desktop Skipper for Plex（下文简称 DSP）可以通过模拟键盘操作的方式，在播放进度到达片头标记（若存在）、片尾标记（若存在）或播放下一个倒计时后，通过模拟按下 `回车` 或 `空格` 键来实现自动跳过片头、自动跳过片尾和自动播放下一个（支持自定义播放下一个倒计时时长）功能。

## 运行说明
- DSP 仅对指定服务器上的视频播放生效。
- DSP 仅对运行 DSP 的设备上的视频播放生效。
- DSP 仅在 Plex for Windows/Mac 窗口处于活动状态时生效（包括全屏状态）。
- DSP 仅对 Plex for Windows/Mac 生效。

## 配置说明
在使用 DSP 前，请先参考以下提示（示例）对 `/config/config.ini` 进行配置。
```
[server]
# Plex 服务器的地址，格式为 http://服务器 IP 地址:32400 或 http(s)://域名:端口号
address = http://127.0.0.1:32400
# Plex 服务器的 token，用于身份验证
token = xxxxxxxxxxxxxxxxxxxx
# 语言设置，zh 代表中文，en 代表英文
language = zh

[preferences]
# 设置播放下一个倒计时的时长，范围为 1 到 8 秒，支持小数
countdown_seconds = 1.5
# 设置 DSP 对哪些用户的播放生效，格式为用户甲；用户乙；用户丙，如果希望 DSP 对所有用户生效，可以留空
users = 用户甲；用户乙；用户丙
```
DSP 在连接到你的服务器后，会实时监控服务器上的所有播放活动，并筛选出 Plex for Windows/Mac 上的播放活动，然后跟踪这些播放。当播放进度到达片头、片尾标记时（若存在），会模拟键盘按下 `回车` 键来实现自动跳过标记；当视频播放结束后，会根据你设置的倒计时时长，等待对应的秒数后模拟键盘按下 `空格` 键来实现自动播放下一个项目（前提是开启了自动播放功能）。

由于网络连接情况的差异，模拟按键的操作在某些情况下可能发生延迟。目前没有找到更好的方案来判断播放是否来自本机，若希望 DSP 工作的更加精准，建议在 `preferences` 里设置本机 Plex for Windows/Mac 的常用用户（在 `users` 处填写常用用户的用户名），这样，就只有这些常用用户的播放活动会被监控，DSP 将仅对这些指定的用户生效。

## 运行条件
- 安装了 Python 3.6 或更高版本。
- 使用命令 `pip3 install -r requirements.txt` 安装了必要的第三方库。

## 使用方法
1. 通过 [Releases](https://github.com/x1ao4/desktop-skipper-for-plex/releases) 下载最新版本的压缩包并解压到本地目录中。
2. 用记事本或文本编辑打开目录中的 `/config/config.ini` 文件，填写你的 Plex 服务器地址（`address`）和 [X-Plex-Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)（`token`），按照需要选填其他配置选项。
3. 双击 `dsp.bat (Win)` 或 `dsp.command (Mac)` 即可启动 DSP。
4. DSP 将在启动后持续监控服务器上的所有播放活动，并在满足条件时通过模拟键盘按键的方式实现自动跳过片头、自动跳过片尾和自动播放下一个功能。同时也会在控制台显示对应播放活动的信息和处理结果。

## 自动运行
为了便于使用，你也可以通过 crontab 或其他任务工具，将 DSP 设置为开机启动任务，实现开机自动运行。Mac 用户可参考以下步骤进行设置：

1. 用文本编辑打开 `dsp.command` 文件，在第二行输入 `sleep 10` 保存更改并关闭文件。
2. 在终端使用命令 `crontab -e` 打开 crontab 文件。
3. 按 `i` 进入插入模式，添加行 `@reboot /path/to/dsp.command`（请把 `/path/to/dsp.command` 替换为脚本的实际路径）。
4. 按 `Esc` 退出插入模式，输入 `:wq`，按 `Enter` 保存更改并退出编辑器。

这样我们就将 DSP 设置为了 Mac 的开机启动任务，DSP 会在开机 10 秒后自动运行，延迟 10 秒是为了保证 Plex 服务器比脚本先启动，否则脚本将无法连接到 Plex 服务器（脚本将在后台运行）。

若设置为开机启动任务后脚本运行失败，你可能需要将 command 脚本中的 `python3` 替换为 `python3` 的实际路径。你可以在 Mac 终端内通过命令 `which python3` 找到 `python3` 的实际路径。

## 注意事项
- 请确保你提供了正确的 Plex 服务器地址和正确的 X-Plex-Token。
- 请确保你提供了正确的用户名，并按要求进行了填写。
- 如果无法连接到 Plex 服务器，请检查你的网络连接，并确保服务器可以访问。
- 修改配置文件后，需要重启脚本，新的配置信息才会生效。
- 在同一次播放中，每个标记只会被自动跳过一次。
- 自动跳过片头和自动跳过片尾功能仅在项目存在标记时生效。
- Windows 用户运行脚本后，若没有任何反应，请将启动脚本中的 `python3` 替换为 `python` 再运行。

## 赞赏
如果你觉得这个项目对你有用，可以请我喝杯咖啡。如果你喜欢这个项目，可以给我一个⭐️。谢谢你的支持！

<img width="399" alt="赞赏" src="https://github.com/x1ao4/desktop-skipper-for-plex/assets/112841659/73b7f053-570e-48c0-8136-3895eabaa2ba">
<br><br>
<a href="#desktop-skipper-for-plex-zh">回到顶部</a>
<br>
<br>
<br>

# Desktop Skipper for Plex <a name="desktop-skipper-for-plex-en"></a>
<a href="#desktop-skipper-for-plex-zh">切换至中文</a>

In October 2023, Plex added [features](https://forums.plex.tv/t/player-experience/857990) such as automatic intro skipping, automatic credits skipping, and customizable auto play countdown time to some of its playback clients. Unfortunately, Plex for Windows/Mac still lacks these features. You still need to manually click the skip button and wait for the 10-second countdown to auto-play the next item.

Since the remote control (Advertise as Player) feature for Plex for Windows/Mac was [removed](https://forums.plex.tv/t/plex-for-mac-windows-and-linux/446435/63) a long time ago, we cannot remotely control these players via API or other means. I couldn’t find any automation tool supporting Plex for Windows or Plex for Mac, so I wrote this script myself.

When watching videos on Plex for Windows/Mac, you can use Desktop Skipper for Plex (hereinafter referred to as DSP) to simulate keyboard actions. When the playback reaches the intro marker (if present), the credits marker (if present), or the auto play countdown, DSP simulates pressing the `Enter` or `Space` key to automatically skip the intro, skip the credits, and auto-play the next item (with customizable auto play countdown times).

## Instructions
- DSP only works for video playback on the specified server.
- DSP only works for video playback on the device running DSP.
- DSP only works when the Plex for Windows/Mac window is active (including fullscreen mode).
- DSP only works for Plex for Windows/Mac.

## Configuration
Before using DSP, please configure the `/config/config.ini` file according to the following tips (example).
```
[server]
# Address of the Plex server, formatted as http://server IP address:32400 or http(s)://domain:port
address = http://127.0.0.1:32400
# Token of the Plex server for authentication
token = xxxxxxxxxxxxxxxxxxxx
# Language setting, zh for Chinese, en for English
language = en

[preferences]
# Set the duration of the auto play countdown time, range from 1 to 8 seconds, supports decimals
countdown_seconds = 1.5
# Set which users’ playback DSP applies to, format as UserA;UserB;UserC. Leave blank to apply to all users
users = UserA;UserB;UserC
```
After connecting to your server, DSP will monitor all playback sessions on the server in real-time and filter out playback sessions on Plex for Windows/Mac. When the playback reaches the intro or credits markers (if present), DSP simulates pressing the `Enter` key to skip the markers. After the video ends, DSP waits for the set countdown duration and simulates pressing the `Space` key to auto-play the next item (provided the auto-play feature is enabled).

Due to differences in network conditions, simulated keystrokes might be delayed in some cases. Currently, there is no better way to determine if playback originates from the local machine. To make DSP more accurate, it is recommended to set the usual users of Plex for Windows/Mac in the `preferences` section (fill in the usual usernames under `users`). This way, only playback sessions of these specified users will be monitored, and DSP will only apply to these users.

## Requirements
- Python 3.6 or higher installed.
- Necessary third-party libraries installed using the command `pip3 install -r requirements.txt`.

## Usage
1. Download the latest release package from [Releases](https://github.com/x1ao4/desktop-skipper-for-plex/releases) and extract it to a local directory.
2. Open the `/config/config.ini` file in the directory using a text editor, fill in your Plex server address (`address`) and [X-Plex-Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) (`token`), and fill in other configuration options as needed.
3. Double-click `dsp.bat (Win)` or `dsp.command (Mac)` to start DSP.
4. Once started, DSP will continuously monitor all playback sessions on the server and simulate keystrokes to auto-skip intros, auto-skip credits, and auto-play the next item when conditions are met. Corresponding playback session information and results will also be displayed in the console.

## Automation
For convenience, you can set DSP to run automatically at startup using crontab or other task tools. Mac users can follow these steps:

1. Open the `dsp.command` file with a text editor, add `sleep 10` on the second line, save the changes, and close the file.
2. Open the crontab file in the terminal with the command `crontab -e`.
3. Press `i` to enter insert mode and add the line `@reboot /path/to/dsp.command` (replace `/path/to/dsp.command` with the actual path to your script).
4. Press `Esc` to exit insert mode, type `:wq`, and press `Enter` to save changes and exit the editor.

Now, DSP is set to run automatically at Mac startup, and DSP will run 10 seconds after startup. The 10-second delay ensures that the Plex server starts before the script; otherwise, the script will fail to connect to the Plex server (the script will run in the background).

If the script fails to run after being set as a startup task, you may need to replace `python3` in the command script with the actual path of `python3`. You can find the actual path of `python3` in the Mac terminal by using the command `which python3`.

## Notes
- Ensure you provide the correct Plex server address and the correct X-Plex-Token.
- Ensure you provide the correct usernames and fill them in as required.
- If you cannot connect to the Plex server, check your network connection and ensure the server is accessible.
- After modifying the configuration file, restart the script for the new settings to take effect.
- During the same playback session, each marker will only be skipped automatically once.
- The automatic intro skipping and automatic credits skipping functions only take effect when there are markers present in the item.
- If Windows users see no response after running the script, try replacing `python3` with `python` in the startup script.

## Support
If you found this helpful, consider buying me a coffee or giving it a ⭐️. Thanks for your support!

<img width="399" alt="Support" src="https://github.com/x1ao4/desktop-skipper-for-plex/assets/112841659/73b7f053-570e-48c0-8136-3895eabaa2ba">
<br><br>
<a href="#desktop-skipper-for-plex-en">Back to Top</a>
