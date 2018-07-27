# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import liveData as lD
import lsConfig


OUTPUT_CONFIG = lsConfig.config()['OUTPUT']


def get_accounts():
    accounts = pd.read_excel(OUTPUT_CONFIG['acct_xls'], sheet_name="account")
    return accounts


def get_data(accounts):
    data = {}

    for index, row in accounts.iterrows():
        live_data = lD.get_live_data(str(row[1]), str(row[2]))
        data[str(row[0])] = live_data

    return data


def gen_date_range_index():
    td = datetime.date.today()
    delta = datetime.timedelta(days=30)
    start_day = td - delta
    date_rng = pd.date_range(start_day, periods=30, freq='D')

    return date_rng


def to_data_frame(live_data, date_rng):
    full_live_data = gen_dummy_data(live_data)

    df = pd.DataFrame(full_live_data, columns=OUTPUT_CONFIG['column_order'], index=date_rng)

    return df


def gen_dummy_data(live_data):
    for key, value in OUTPUT_CONFIG['dummy_tags'].items():
        live_data[value] = [''] * 30

    return live_data


def process():
    accounts = get_accounts()
    data = get_data(accounts)

    date_rng = gen_date_range_index()

    writer = pd.ExcelWriter(OUTPUT_CONFIG['live_stats_output_xls'])
    for key, value in data.items():
        df = to_data_frame(value, date_rng)
        df.to_excel(writer, sheet_name=key)
    writer.save()


process()
