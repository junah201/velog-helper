import datetime

TZ_KST = datetime.timezone(datetime.timedelta(hours=9))


def UTC_to_KST(utc_time: datetime.datetime) -> datetime.datetime:
    kst_time = utc_time + datetime.timedelta(hours=9)
    #kst_time = kst_time.replace(tzinfo=TZ_KST)
    return kst_time
