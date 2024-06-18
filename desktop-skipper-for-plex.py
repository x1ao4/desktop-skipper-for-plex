import time
import logging
import requests
import pyautogui
from pathlib import Path
from configparser import ConfigParser
from plexapi.server import PlexServer

# 设置 pyautogui 函数之间的延迟
pyautogui.PAUSE = 0.1

# 初始化设置
def initialize_settings():
    # 设置日志记录器
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    # 读取配置文件
    config_file = Path(__file__).parent / 'config' / 'config.ini'
    config = ConfigParser()
    config.read(config_file)

    server_address = config.get('server', 'address')
    token = config.get('server', 'token')
    language = config.get('server', 'language')

    try:
        # 连接到 Plex 服务器
        headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
        response = requests.get(server_address, headers=headers)
        response.raise_for_status()
        server_name = response.json()['MediaContainer']['friendlyName']
        logger.info(f"已成功连接到服务器：{server_name}" if language == 'zh' else f"Successfully connected to server: {server_name}")
        return server_address, token, language
    except requests.exceptions.RequestException as err:
        logger.error("服务器连接失败，请检查配置文件的设置是否有误。如需帮助，请访问 https://github.com/x1ao4/desktop-skipper-for-plex 查看使用说明。\n" if language == 'zh' else "Server connection failed, please check the settings in the configuration file. For help, please visit https://github.com/x1ao4/desktop-skipper-for-plex for instructions.\n")
        time.sleep(10)
        raise SystemExit(err)

# 获取初始化设置
PLEX_URL, PLEX_TOKEN, LANGUAGE = initialize_settings()

# 连接到 Plex 服务器
plex = PlexServer(PLEX_URL, PLEX_TOKEN)

# 创建一个集合来存储已经打印过的会话
printed_sessions = set()

# 创建一个字典来存储标记时间
marker_times = {}

# 创建一个字典来存储每个会话的最后检查时间
last_check_times = {}

# 初始化日志记录器
logger = logging.getLogger(__name__)

# 无限循环运行脚本
while True:
    # 获取当前会话
    sessions = plex.sessions()

    # 检查是否有任何会话
    if sessions:
        # 遍历所有会话
        for session in sessions:
            # 检查会话是否已经被打印过
            if session.ratingKey not in printed_sessions:
                # 将会话添加到已打印会话集合中
                printed_sessions.add(session.ratingKey)

                # 获取正在播放的媒体
                media = session.media[0]

                # 检查媒体类型
                if session.type == 'episode':
                    # 打印电视剧标题
                    logger.info(f'\n正在播放：{session.grandparentTitle} - {session.title}' if LANGUAGE == 'zh' else f'\nNow playing: {session.grandparentTitle} - {session.title}')
                elif session.type == 'movie':
                    # 打印电影标题
                    logger.info(f'\n正在播放：{session.title}' if LANGUAGE == 'zh' else f'\nNow playing: {session.title}')
                else:
                    # 未知媒体类型，不执行任何操作
                    pass

                try:
                    # 根据媒体类型获取标记
                    if session.type == 'episode':
                        # 获取剧集对象
                        episode = plex.fetchItem(session.ratingKey)

                        # 从剧集对象中获取标记
                        markers = episode.markers
                    elif session.type == 'movie':
                        # 获取电影对象
                        movie = plex.fetchItem(session.ratingKey)

                        # 从电影对象中获取标记
                        markers = movie.markers
                    else:
                        markers = []

                    # 获取片头和片尾标记
                    intro_marker = [marker for marker in markers if marker.type == 'intro']
                    credits_marker = [marker for marker in markers if marker.type == 'credits']

                    # 打印标记信息
                    if intro_marker:
                        intro_times = []
                        for marker in intro_marker:
                            start_time = marker.start / 1000
                            end_time = marker.end / 1000
                            intro_times.append(f'{time.strftime("%H:%M:%S", time.gmtime(start_time))}-{time.strftime("%H:%M:%S", time.gmtime(end_time))}')
                        logger.info(f'片头标记：{", ".join(intro_times)}' if LANGUAGE == 'zh' else f'Intro markers: {", ".join(intro_times)}')
                    else:
                        logger.info('片头标记：无' if LANGUAGE == 'zh' else 'Intro markers: None')

                    if credits_marker:
                        credits_times = []
                        for marker in credits_marker:
                            start_time = marker.start / 1000
                            end_time = marker.end / 1000
                            credits_times.append(f'{time.strftime("%H:%M:%S", time.gmtime(start_time))}-{time.strftime("%H:%M:%S", time.gmtime(end_time))}')
                        logger.info(f'片尾标记：{", ".join(credits_times)}\n' if LANGUAGE == 'zh' else f'Credits markers: {", ".join(credits_times)}\n')
                    else:
                        logger.info('片尾标记：无\n' if LANGUAGE == 'zh' else 'Credits markers: None\n')

                    # 在字典中存储标记时间
                    marker_times[session.ratingKey] = {
                        'intro': [(marker.start, marker.end) for marker in intro_marker],
                        'credits': [(marker.start, marker.end) for marker in credits_marker]
                    }
                except Exception as e:
                    # 发生错误，打印错误消息
                    logger.error(f"发生错误：{e}" if LANGUAGE == 'zh' else f"Error: {e}")

            else:
                # 会话已经被打印过，检查是否需要跳过任何标记

                # 获取会话的当前播放时间（以毫秒为单位）
                current_time = session.viewOffset

                # 检查我们是否有任何标记对于这个会话
                if session.ratingKey in marker_times:
                    # 获取这个会话的片头和片尾标记时间（以毫秒为单位）
                    intro_times = marker_times[session.ratingKey]['intro']
                    credits_times = marker_times[session.ratingKey]['credits']

                    # 检查是否需要跳过任何片头标记
                    for intro_time in intro_times:
                        if current_time >= intro_time[0] and current_time <= intro_time[1]:
                            # 我们已经到达了一个片头标记，按回车键跳过它
                            pyautogui.press('enter')
                            logger.info('已跳过片头' if LANGUAGE == 'zh' else 'Intro skipped')

                            # 从列表中删除这个片头时间，以便我们不再跳过它
                            intro_times.remove(intro_time)

                            break

                    # 检查是否需要跳过任何片尾标记
                    for credits_time in credits_times:
                        if current_time >= credits_time[0] and current_time <= credits_time[1]:
                            # 我们已经到达了一个片尾标记，按回车键跳过它
                            pyautogui.press('enter')
                            logger.info('已跳过片尾' if LANGUAGE == 'zh' else 'Credits skipped')

                            # 从列表中删除这个片尾时间，以便我们不再跳过它
                            credits_times.remove(credits_time)

                            break

            # 更新会话的最后检查时间
            last_check_times[session.ratingKey] = time.time()

    else:
        # 没有会话，不执行任何操作
        pass

    # 检查是否有任何会话已经停止播放
    for rating_key, last_check_time in list(last_check_times.items()):
        if time.time() - last_check_time > 5:
            # 会话已经超过 5 秒没有被检查，认为它已经停止播放
            del last_check_times[rating_key]
            printed_sessions.discard(rating_key)

    # 等待一段时间再次检查
    time.sleep(0.5)
