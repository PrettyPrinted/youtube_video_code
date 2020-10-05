from datetime import datetime 
#from pytz import timezone
from zoneinfo import ZoneInfo

current_time = datetime.now()
print(current_time)
current_time_amsterdam = datetime.now()
print(current_time.astimezone(ZoneInfo('Europe/Amsterdam')))

