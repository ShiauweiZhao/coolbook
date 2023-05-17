from ics import Calendar, Event
import datetime
import pytz

# 定义班次类型
schedules = ["连班", "行政班", "夜班", "下班", "休息"]

# 定义开始日期和开始班次
start_date = datetime.date(2023, 5, 17)
start_schedule = "休息"

# 获取开始班次在列表中的位置
start_index = schedules.index(start_schedule)

# 调整班次列表，使开始班次在第一位
adjusted_schedules = schedules[start_index:] + schedules[:start_index]


def get_schedule(day):
    # 计算给定日期是循环中的哪一天
    day_in_cycle = day % len(adjusted_schedules)

    # 返回该天的班次类型
    return adjusted_schedules[day_in_cycle]


# 创建一个新的日历
c = Calendar()

# 获取北京时区
beijing_tz = pytz.timezone("Asia/Shanghai")

# 计算未来30天的班次类型，并将其存储在日历中
for i in range(30):
    future_date = start_date + datetime.timedelta(days=i)
    days_from_start = (future_date - start_date).days
    schedule = get_schedule(days_from_start)

    # 为每一天创建一个新的事件
    e = Event()
    e.name = schedule  # 将班次设为事件的标题
    e.begin = beijing_tz.localize(datetime.datetime.combine(future_date, datetime.time(0, 0)))  # 使用北京时区的午夜作为开始时间
    e.duration = datetime.timedelta(days=1)  # 设置事件持续一整天

    # 将事件添加到日历中
    c.events.add(e)

# 使用 "utf-8" 编码将日历写入到 .ics 文件中
with open('schedule.ics', 'w', encoding="utf-8") as my_file:
    my_file.writelines(c)

