# plex-desktop-skipper
使用 plex-desktop-skipper 可以让您在使用 Plex for Win/Mac 播放媒体时自动跳过片头和片尾标记。该脚本会使用 plexapi、time 和 pyautogui 模块连接到 Plex 服务器，监控当前会话并模拟键盘按键以跳过标记。

## 运行条件
- 安装了 Python 3.0 或更高版本。
- 安装了必要的第三方库：plexapi 和 pyautogui。

## 使用方法
1. 将脚本下载到计算机上的一个目录中。
2. 在脚本中设置您的 Plex 服务器的 URL 和令牌，将 `PLEX_URL` 和 `PLEX_TOKEN` 变量的值更改为您的 Plex 服务器的 URL 和令牌。例如：
```
# 设置 Plex 服务器的 URL 和令牌
PLEX_URL = 'http://127.0.0.1:32400'
PLEX_TOKEN = 'xxxxxxxxxxxxxxxxxxxx'
```
3. 修改 `start.command (Mac)` 或 `start.bat (Win)` 中的路径，以指向您存放 `plex-desktop-skipper.py` 脚本的目录。
4. 双击运行 `start.command` 或 `start.bat` 脚本以执行 `plex-desktop-skipper.py` 脚本。
5. 脚本将开始监控您的 Plex 服务器，当检测到正在播放的媒体包含片头或片尾标记时，脚本将模拟按下回车键以跳过标记。您可以在控制台中查看已播放媒体的标记信息和跳过信息。

## 注意事项
- 由于此脚本使用了模拟键盘按键的方法来跳过标记，因此它只能在桌面（Win/Mac）环境下运行，并且需要您保持 Plex 播放器窗口处于活动状态。
- 只有当前播放的媒体包含片头或片尾标记时，此脚本才能生效，要使用自动跳过功能请确保您的媒体已经进行了片头或片尾分析，并生成了标记。
- 由于脚本使用了 pyautogui 模块来模拟键盘按键，因此它可能会与其他正在运行的程序产生冲突。在使用此脚本时，请谨慎操作。

## 已知问题
由于网络原因，当跳过标记出现后，可能会延迟几秒才会自动跳过。
<br>
<br>

# plex-desktop-skipper
plex-desktop-skipper is a script that allows you to automatically skip intro and credits markers when playing media on Plex for Win/Mac. The script uses the plexapi, time, and pyautogui modules to connect to a Plex server, monitor the current sessions, and simulate keyboard presses to skip markers.

## Requirements
- Python 3.0 or higher installed.
- Required third-party libraries: plexapi and pyautogui.

## Usage
1. Clone or download the repository to a directory on your computer.
2. Set the URL and token for your Plex server in the script by changing the values of the `PLEX_URL` and `PLEX_TOKEN` variables. For example:
```
# Set the URL and token for the Plex server
PLEX_URL = 'http://127.0.0.1:32400'
PLEX_TOKEN = 'xxxxxxxxxxxxxxxxxxxx'
```
3. Modify the path in `start.command (Mac)` or `start.bat (Win)` to point to the directory where you store the `plex-desktop-skipper.py` script.
4. Double-click `start.command` or `start.bat` to execute the `plex-desktop-skipper.py` script.
5. The script will start monitoring your Plex server, and when it detects that media being played contains intro or credits markers, it will simulate pressing the enter key to skip them. You can view marker information and skip information for played media in the console.

## Notes
- Since this script uses simulated keyboard presses to skip markers, it can only be run in a desktop (Win/Mac) environment and requires that the Plex player window be active.
- The script will only work if the media being played contains intro or credits markers, so make sure your media has been analyzed for intros or credits and has generated markers if you want to use the automatic skipping feature.
- Since the script uses the pyautogui module to simulate keyboard presses, it may conflict with other programs that are running. Use caution when using this script.

## Known Issues
Due to network issues, there may be a slight delay of a few seconds before the marker is automatically skipped.
