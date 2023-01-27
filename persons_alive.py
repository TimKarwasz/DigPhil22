import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

# '05/11/1770' discharged, no death
# '25/12/1770' deserted, no death
# '26/08/1768' start date
# '02/12/1768' a seamen died in Rio but they got a portugese replacement , code it in

# these are the dates on which people died
dates = ['25/03/1771','15/04/1771','04/02/1771','06/02/1771','05/11/1770',
         '04/02/1771','12/02/1771','31/01/1771','14/09/1768','29/08/1769',
         '31/01/1771','27/01/1771','01/08/1771','02/12/1768','24/12/1770',
         '01/02/1771','31/01/1771','30/04/1770','31/01/1771','31/01/1771',
         '21/02/1771','07/04/1771','24/12/1770','27/02/1771','30/06/1771',
         '02/02/1771','03/02/1771','24/01/1771','16/02/1771','06/04/1769',
         '26/01/1771','29/01/1771','18/12/1770','26/01/1771','17/04/1769',
         '24/01/1771','16/01/1769','16/01/1769','26/08/1768','03/12/1768'
]

# convert them to datetime data type for easy plotting
dates = [dt.datetime.strptime(d,'%d/%m/%Y').date() for d in dates]

start_persons = 86
sorted_dates = sorted(dates)
final_entries = {}

# counting down when people died
for date in sorted_dates:
    if date not in final_entries.keys():
        if date == dt.datetime.strptime("03/12/1768",'%d/%m/%Y').date():
            start_persons += 1
            final_entries[date] = start_persons
        else:
            start_persons -= 1
            final_entries[date] = start_persons
    else :
        start_persons -= 1
        final_entries[date] = start_persons

x = list(final_entries.keys())
y = list(final_entries.values())

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))

locator = mdates.DayLocator(interval=60)
locator.MAXTICKS = 1200

# create the acutal plot
plt.gca().xaxis.set_major_locator(locator)
plt.plot(x,y, color ='maroon')
plt.gcf().autofmt_xdate()
plt.xlabel("Date")
plt.ylabel("No. of people alive")

# annotate some points of interest
# Seamen drowned, they a got a portugese replacement
ppl = 83
date = dt.datetime.strptime("03/12/1768",'%d/%m/%Y').date()

plt.scatter(x,y)

plt.annotate('Seamen drowned and they got a portugese replacement', xy =(date, ppl-2),
                xytext =(date, ppl -5), 
                arrowprops = dict(facecolor ='blue',
                                  shrink = 0.01),)

# a lot of people died of flux
ppl = 77
date = dt.datetime.strptime("05/11/1770",'%d/%m/%Y').date()

plt.scatter(x,y)

plt.annotate('Died of dysentery (Ruhr),aggravated by malaria', xy =(date, ppl +1),
                xytext =(date, ppl +4), 
                arrowprops = dict(facecolor ='blue',
                                  shrink = 0.01),)

plt.show()



