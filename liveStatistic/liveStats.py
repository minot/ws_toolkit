# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import liveData as ld

ACCT_XLS="C:\\Users\\Min Wang\\Desktop\\账号.xlsx"
LIVE_STATS = "C:\\Users\\Min Wang\\Desktop\\STATS.xlsx"
COL_ORDER = ['人气峰值', '礼物金豆', '直播时长', '新增订阅', '获得分享', '直播时长（分）']


def get_accounts():
    accounts = pd.read_excel(ACCT_XLS, sheet_name="account")
    return accounts


def get_data(accounts):
    data = {}

    for index, row in accounts.iterrows():
        live_data = ld.get_live_data(str(row[1]), str(row[2]))
        data[str(row[0])] = live_data

    return data


def gen_date_range_index():
    td = datetime.date.today()
    delta = datetime.timedelta(days=31)
    start_day = td - delta
    date_rng = pd.date_range(start_day, periods=30, freq='D')

    return date_rng


def to_data_frame(live_data, date_rng):
    live_data['直播时长'] = [0] * 30
    df = pd.DataFrame(live_data, columns=COL_ORDER, index=date_rng)

    return df


def process():
    accounts = get_accounts()
    data = get_data(accounts)

    date_rng = gen_date_range_index()

    for key, value in data.items():
        df = to_data_frame(value, date_rng)
        df.to_excel(LIVE_STATS, sheet_name=key)


process()
