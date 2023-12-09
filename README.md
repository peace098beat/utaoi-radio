# Utaoi Radio

## About
タイムテーブルに従って、音楽を流すスクリプトです。

[time-table - Google スプレッドシート](https://docs.google.com/spreadsheets/d/1wRvMZKbgAKgaz8Pu1kd5Ii79iqUDvNgYtkY90u-REgk/edit#gid=0)

## Requirements

- Python 3.11.0


## Othre Requirements

 - vlc

```
brew install --cask vlc@3.0.20
```

## Google Spreadsheet API

GCPにて、サービスアカウントを作成し、サービスアカウントキーを取得してください。

## setup

```
pyenv install 3.11.0

pyenv local 3.11.0

python3 -m pip install poetry

python3 -m poetry install

python3 -m poetry shell
```