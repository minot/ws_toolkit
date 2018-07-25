# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import liveData as ld

ACCT_XLS="C:\\Users\\Min Wang\\Desktop\\账号.xlsx"
LIVE_STATS = "C:\\Users\\Min Wang\\Desktop\\STATS.xlsx"
COL_ORDER = ['人气峰值', '礼物金豆', '直播时长', '新增订阅', '获得分享', '直播时长（分）']

def getAccount():
    accounts = pd.read_excel(ACCT_XLS, sheet_name="account")
    return accounts

def getData(accounts):
    data = {}

    for index, row in accounts.iterrows():
        live_data = ld.getLiveData(str(row[1]), str(row[2]))
        data[str(row[0])] = live_data

    return data

def genDateRangeIndex():
    td = datetime.date.today()
    delta = datetime.timedelta(days=31)
    start_day = td - delta
    date_rng = pd.date_range(start_day, periods=30, freq='D')

    return date_rng

def toDataFrame(live_data, date_rng):
    live_data['直播时长'] = [0] * 30
    df = pd.DataFrame(live_data, columns=COL_ORDER, index=date_rng)

    return df

def process():
    accounts = getAccount()
    data = getData(accounts)

    date_rng = genDateRangeIndex()

    for key, value in data.items():
        df = toDataFrame(value, date_rng)
        df.to_excel(LIVE_STATS, sheet_name=key)

process()