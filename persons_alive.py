import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

# first page 24
# second page 49
# third page 12
# total 24 + 49 + 12 = 85

# '05/11/1770' discharged, no death
# '25/12/1770' deserted, no death
# '26/08/1768' start date
dates = ['25/03/1771','15/04/1771','04/02/1771','06/02/1771','05/11/1770',
         '04/02/1770','12/02/1770','31/01/1770','14/09/1768','29/08/1768',
         '31/01/1769','27/01/1771','01/08/1771','02/12/1768','24/12/1770',
         '01/02/1771','31/01/1771','30/04/1770','31/01/1771','31/01/1771',
         '21/02/1771','07/04/1771','24/12/1770','27/02/1771','30/06/1771',
         '02/02/1771','03/02/1771','24/01/1771','16/02/1771','06/04/1769',
         '26/01/1771','29/01/1771','18/12/1770','26/01/1770','17/04/1770',
         '24/01/1771','16/01/1769','16/01/1769','26/08/1768'
]
dates = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in dates]


start_persons = 86
sorted_dates = sorted(dates)
final_entries = {}

# counting down when people died
for date in sorted_dates:
    if date not in final_entries.keys():
        start_persons -= 1
        final_entries[date] = start_persons
    else :
        start_persons -= 1
        final_entries[date] = start_persons

x = list(final_entries.keys())
y = list(final_entries.values())

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))

locator = mdates.DayLocator(interval=60)
locator.MAXTICKS = 1200

plt.gca().xaxis.set_major_locator(locator)
plt.plot(x,y)
plt.gcf().autofmt_xdate()
plt.xlabel("Date")
plt.ylabel("No. of people alive")
plt.show()



