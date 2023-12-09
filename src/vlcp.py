
URLS = [
    "https://www.youtube.com/watch?v=yXQViqx6GMY",
]

import yt_dlp

# ydl_opts = {
#     'format': 'm4a/bestaudio/best',
#     # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
#     'postprocessors': [{  # Extract audio using ffmpeg
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'm4a',
#     }],
#     # 'outtmpl': '/path/to/your/directory/%(title)s.%(ext)s'  # 保存パスとファイル名
# }

# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     info_dict = ydl.extract_info(URLS[0], download=False)
#     file_name = ydl.prepare_filename(info_dict)
#     ydl.download(URLS)

# print(file_name)  # ダウンロードしたファイルの名前を表示


class YoutubeDonloader:
    def __init__(self, urls, outdir):
        self.urls = urls
        self.outdir = outdir
        self.name_dict = {}

    def download(self):
        for url in self.urls:
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
