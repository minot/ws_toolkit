# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import liveData as lD
import lsConfig
import logging
import logging.config


OUTPUT_CONFIG = lsConfig.config()['OUTPUT']
logging.config.fileConfig("logger.conf")


def get_accounts():
    accounts = pd.read_excel(OUTPUT_CONFIG['acct_xls'], sheet_name="account")
    return accounts


def get_data(accounts):
    data = {}

    for index, row in accounts.iterrows():
        user = row[1]
        passwd = row[2]
        cookies = row[3]
        logging.info("Start to get live data for user: " + str(user))

        try:
            live_data = lD.get_live_data(user, passwd, cookies)
        except Exception as err:
            logging.error("Got exception: " + err)
        else:
            logging.info("Retrieved live data: " + str(live_data))

        data[user] = live_data

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

def to_decimal(data_frame):
    data_frame[OUTPUT_CONFIG['decimal_column']] = pd.to_numeric(data_frame[OUTPUT_CONFIG['decimal_column']], errors='coerce') / 1000
    #data_frame.round({OUTPUT_CONFIG['decimal_column']: 3})


def process():
    logging.info("Start to process live statistic.")
    accounts = get_accounts()
    data_dic = get_data(accounts)

    date_rng = gen_date_range_index()

    writer = pd.ExcelWriter(OUTPUT_CONFIG['live_stats_output_xls'])
    for user, data in data_dic.items():
        data_frame = to_data_frame(data, date_rng)
        to_decimal(data_frame)
        logging.info("Going to write live data to sheet: " + str(user))
        print(data_frame)
        data_frame.to_excel(writer, sheet_name=str(user))
    writer.save()
    logging.info("All sheets are written to excel [" + OUTPUT_CONFIG['live_stats_output_xls'] + "].")

    logging.info("Live statistic processed.")

process()
