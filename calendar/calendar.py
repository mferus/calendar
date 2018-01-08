import tkinter
import datetime
import calendar
from workalendar.europe import Poland

main_window = tkinter.Tk()
main_window.title("Calendar")
main_window.geometry("601x381")
main_window["padx"] = 4
main_window["pady"] = 10

main_window.minsize(301, 381)
main_window.maxsize(301, 381)

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

months = ["January", "February", "March", "April",
          "May", "June", "July", "August",
          "September", "October", "November", "December"
          ]

days_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


def display_date_string(date_in_time):
    today = days[date_in_time.isoweekday()-1]
    return f"{today}, {months[date_in_time.month-1]} {date_in_time.day}, {date_in_time.year}"


def get_year(date_in_time):
    return date_in_time.year


def get_month(date_in_time):
    return date_in_time.month


def get_month_name(date_in_time):
    current_month = date_in_time.month
    return months[current_month - 1]


def get_first_day_of_month(date_in_time):
    return datetime.date(get_year(date_in_time), get_month(date_in_time), 1).isoweekday()


def get_days_in_month(date_in_time):
    return max(calendar.monthrange(get_year(date_in_time), get_month(date_in_time)))


def get_last_month(date_in_time):
    if date_in_time.month == 1:
        year = date_in_time.year - 1
        month = 12
        last_month_date = datetime.date(year, month, 1)
        return get_days_in_month(last_month_date)
    else:
        month = date_in_time.month - 1
        last_month_date = datetime.date(date_in_time.year, month, 1)
        return get_days_in_month(last_month_date)


def left_arrow_month():
    if months.index(month_text.get())+1 == 1:
        month_text.set(months[11])
        month = 12
        year = year_text.get()-1
        create_calendar(datetime.date(year, month, 1))
        year_text.set(year_text.get() - 1)
    else:
        month_text.set(months[months.index(month_text.get())-1])
        month = months.index(month_text.get())+1
        year = year_text.get()
        create_calendar(datetime.date(year, month, 1))


def right_arrow_month():
    if months.index(month_text.get())+1 == 12:
        month_text.set(months[0])
        month = 1
        year = year_text.get()+1
        create_calendar(datetime.date(year, month, 1))
        year_text.set(year_text.get() + 1)
    else:
        month_text.set(months[months.index(month_text.get())+1])
        month = months.index(month_text.get())+1
        year = year_text.get()
        create_calendar(datetime.date(year, month, 1))


def left_arrow_year():
    create_calendar(datetime.date((year_text.get()-1), (months.index(month_text.get())+1), 1))
    year_text.set(year_text.get()-1)


def right_arrow_year():
    create_calendar(datetime.date((year_text.get()+1), (months.index(month_text.get())+1), 1))
    year_text.set(year_text.get()+1)


def check_day(day_button):
    day_of_month = day_button["text"]
    date_string = display_date_string(datetime.date((year_text.get()),
                                                    (months.index(month_text.get())+1),
                                                    day_of_month))
    display_date_variable.set(date_string)
    day_key = f"{day_of_month}/{months.index(month_text.get())+1}/{year_text.get()}"
    if day_key in holiday_dict:
        display_description_variable.set('   ' + holiday_dict[day_key])
    else:
        display_description_variable.set('   ' + "(...)")


def create_calendar(date_in_time):
    day_number = 1
    first_days = 1
    next_month_days = 1
    days_of_last_month = get_first_day_of_month(date_in_time) - 2
    last_month_days = get_last_month(datetime.date((year_text.get()),
                                                   (months.index(month_text.get())+1),
                                                   1)) - days_of_last_month
    for row in range(4, 10):
        for column in range(7):
            next_month_days_condition = day_number > get_days_in_month(date_in_time)
            day_button = tkinter.Button(main_window,
                                        bg=calendar_background_weekend_checker(column),
                                        fg=calendar_foreground_weekend_checker(column),
                                        font=calendar_bold_weekend_checker(column))
            day_button.configure(command=lambda button=day_button: check_day(button))
            day_button.grid(row=row, column=column, sticky="news")
            day_key = f"{day_number}/{date_in_time.month}/{date_in_time.year}"
            if first_days < get_first_day_of_month(date_in_time):
                day_button.config(text=last_month_days, fg="grey", state="disabled")
                last_month_days += 1
                first_days += 1
            elif not next_month_days_condition:
                if day_key in holiday_dict:
                    if holiday_dict[day_key] == "Current day":
                        day_button.config(text=day_number, bg="#A0A0A0", fg="#FFFFFF")
                        day_number += 1
                    else:
                        day_button.config(text=day_number, bg="#C0C0C0", fg="#FFFFFF")
                        day_number += 1
                else:
                    day_button.config(text=day_number)
                    day_number += 1
            elif next_month_days_condition:
                day_button.config(text=next_month_days, fg="grey", state="disabled")
                next_month_days += 1


def calendar_background_weekend_checker(column):
    if column / 5 == 1 or column / 6 == 1:
        return "#FFFFFF"
    # else:
    #     return "#CCFFFF"


def calendar_foreground_weekend_checker(column):
    if column / 5 == 1 or column / 6 == 1:
        return "#404040"


def calendar_bold_weekend_checker(column):
    weekend_condition = (column / 5 == 1 or column / 6 == 1)
    if weekend_condition:
        return 'arial 10 bold'
    else:
        return 'arial 10'


current_date = datetime.date.today()
holiday_dict = {}
current_day = f"{current_date.day}/{current_date.month}/{current_date.year }"
holiday_dict[current_day] = "Current day"

for x in range(current_date.year-20, current_date.year+20):
    holidays = Poland().holidays(x)
    for holiday in holidays:
        dictionary_key = f"{holiday[0].day}/{holiday[0].month}/{holiday[0].year}"
        holiday_dict[dictionary_key] = holiday[1]

today_label = tkinter.Label(main_window, text=display_date_string(current_date),
                            font="arial 10 italic", background="#E0E0E0")
today_label.grid(row=0, column=0, columnspan=7, sticky="snew")

year_left_arrow = tkinter.Button(main_window, text="<", command=left_arrow_year, background="#E0E0E0")
year_left_arrow.grid(row=1, column=0)
year_right_arrow = tkinter.Button(main_window, text=">", command=right_arrow_year, background="#E0E0E0")
year_right_arrow.grid(row=1, column=6)

year_text = tkinter.IntVar()
year_text.set(get_year(current_date))
year_label = tkinter.Label(main_window, textvariable=year_text, font="arial 12")
year_label.grid(row=1, column=1, columnspan=5, sticky="news")

month_left_arrow = tkinter.Button(main_window, text="<", command=left_arrow_month, background="#E0E0E0")
month_left_arrow.grid(row=2, column=0)
month_right_arrow = tkinter.Button(main_window, text=">", command=right_arrow_month, background="#E0E0E0")
month_right_arrow.grid(row=2, column=6)

month_text = tkinter.StringVar()
month_text.set(get_month_name(current_date))
month_label = tkinter.Label(main_window, textvariable=month_text, font="arial 12")
month_label.grid(row=2, column=1, columnspan=5, sticky="news")

for i in range(7):
    day_name = tkinter.Label(main_window, text=days_list[i], background="#C0C0C0")
    day_name.grid(row=3, column=i, sticky="news")

display_frame = tkinter.LabelFrame(main_window, text="Date Details", borderwidth=1)
display_frame.grid(row=10, column=0, columnspan=7, rowspan=4, sticky="we")

display_date_variable = tkinter.StringVar(display_frame)
display_date_variable.set(display_date_string(current_date))
display_date = tkinter.Label(display_frame, textvariable=display_date_variable, font="arial 13 italic", anchor="w")
display_date.grid(row=0, column=0, rowspan=2, sticky='news')


display_description_variable = tkinter.StringVar(display_frame)
display_description_variable.set("Current day")
display_description = tkinter.Label(display_frame, textvariable=display_description_variable, height=3, anchor="w")
display_description.grid(row=2, column=0, rowspan=2, sticky='news')


create_calendar(current_date)

main_window.mainloop()
