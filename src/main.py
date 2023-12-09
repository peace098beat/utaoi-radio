"""
# 常時動作するメインプロセス
# このプロセスは、以下の処理を行う
# 1. GoogleSpreadSheetから、曲リストを取得する
# 2. 曲リストを元に、曲を再生する
# 3. 曲が終了したら、1に戻る
# 詳細
# 曲の再生にはvlcを使用する
# 曲の再生はURLを指定して行う
# 曲のURLは、GoogleSpreadSheetから取得する
# ログは、logs/YYYYMMDD.logに出力する
# ログは、ログローテーションする
# ログは、google spread sheetにも出力する. 

# 再生の仕様
N分に一回、TimeTableを取得する.
TimeTableが更新されていた場合、再生を停止して、新しいTimeTableをsetし再生する.

"""
import sys
print(sys.version)
URL = "https://www.youtube.com/watch?v=U1sESciUsYk"

# logging
import logging
import logging.handlers
from pathlib import Path
from datetime import datetime

import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

import vlc
player = vlc.MediaListPlayer()

import yt_dlp

class YoutubeDonloader:
    def __init__(self, outdir):
        self.outdir = outdir
        self.name_dict = {}

        Path(outdir).mkdir(exist_ok=True, parents=True)

    def download(self, urls):
        for url in urls:
            ydl_opts = {
                'format': 'm4a/bestaudio/best',
                # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
                'postprocessors': [{  # Extract audio using ffmpeg
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                }],
                'outtmpl': f'{self.outdir}/%(title)s.%(ext)s'  # 保存パスとファイル名
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                file_name = ydl.prepare_filename(info_dict)
                ydl.download(url)
                self.name_dict[url] = file_name

            print(self.name_dict)  # ダウンロードしたファイルの名前を表示
    
    def filename(self, url):
        return self.name_dict[url]
    
yt_donloader = YoutubeDonloader("./cache")


def connect_gspread(jsonf, spread_sheet_id, sheet_name):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(spread_sheet_id)#.sheet1
    return sh.get_worksheet(sheet_name)

auth_json_path = "/Users/macmini2023/Dropbox/03_WORKSPACE/01_Codes/231209_utaoi_radio/neat-acre-318102-4f02b0e5b737.json"
spread_sheet_key = "1wRvMZKbgAKgaz8Pu1kd5Ii79iqUDvNgYtkY90u-REgk"
ws_log = connect_gspread(auth_json_path, spread_sheet_key, 1)
ws_timetable = connect_gspread(auth_json_path, spread_sheet_key, 0)

prev_hash_set = None
prev_time_table = None

def main():
    global prev_hash_set, prev_time_table

    # ログは、syslogに出力する

    LOG_DIR = "logs"
    Path(LOG_DIR).mkdir(exist_ok=True, parents=True)
    LOG_FILENAME = datetime.now().strftime("%Y%m%d") + ".log"
    logfile_path = Path(LOG_DIR) / LOG_FILENAME
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        filename=logfile_path,
        filemode='a'
    )
    logging.getLogger().addHandler(logging.StreamHandler())

    logging.info("start utaoi-radio")
    ws_log.append_row([datetime.now().strftime("%Y/%m/%d %H:%M:%S"), "start utaoi-radio"])

    # GoogleSpreadSheetから曲リストを取得する
    # 曲リストは、以下の形式
    # [
    #    ["start", "end", "url"],
    # ]

    # get time table for list
    list_of_lists = ws_timetable.get_all_values()
    # print(list_of_lists)

    # get current time for HH:MM.
    now_HHMM = datetime.now().strftime("%H:%M")

    # 現在時刻のTimeTableを取得する
    # get current time table.
    _temp_time_table = []
    _temp_hash_set = set()
    for row in list_of_lists:
        start, end, url = row[0], row[1], row[2]
        if start:
            if end:
                if url:
                    if url.startswith("https://www.youtube.com/watch?v="):
                        if start <= now_HHMM and now_HHMM <= end:
                            _temp_time_table.append([start, end, url])
                            _temp_hash_set.add(url[-10:])

    
    # compaire current time table and previous time table.
    if _temp_hash_set != prev_hash_set:
        # log
        logging.info("time table is updated.")
        ws_log.append_row([datetime.now().strftime("%Y/%m/%d %H:%M:%S"), "time table is updated."])

        url_list = [url for _, _, url in _temp_time_table]

        # download
        yt_donloader.download(url_list)

        music_files = [yt_donloader.filename(url) for url in url_list]
        print("music_files", music_files)

        # stop player
        if player:
            player.stop()

        if len(music_files) > 0:
            mediaList = vlc.MediaList(music_files)
            player.set_media_list(mediaList)
            player.set_playback_mode(vlc.PlaybackMode.loop)
            player.play()

        # update prev_time_table
        prev_hash_set = _temp_hash_set
        prev_time_table = _temp_time_table

    else:
        logging.info("time table is not updated.")
        ws_log.append_row([datetime.now().strftime("%Y/%m/%d %H:%M:%S"), "time table is not updated."])

if __name__ == "__main__":
    import time
    while True:
        main()

        time.sleep(10)

