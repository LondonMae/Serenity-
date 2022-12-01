import time
import datetime
td = time.strptime("08:08",'%H:%M')
td = datetime.timedelta(hours=td.tm_hour,minutes=td.tm_min,seconds=td.tm_sec).total_seconds()
print(td/3600)
