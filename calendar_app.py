import tkinter
import datetime
import calendar
from workalendar.europe import Poland


class Calendar:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    months = ["January", "February", "March", "April",
              "May", "June", "July", "August",
              "September", "October", "November", "December"
              ]

    days_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    def __init__(self):
        self.main_window = tkinter.Tk()
        self.month_text = tkinter.StringVar()
        self.year_text = tkinter.IntVar()
        self.display_frame = tkinter.LabelFrame(self.main_window, text="Date Details", borderwidth=1)
        self.display_date_variable = tkinter.StringVar(self.display_frame)
        self.current_date = datetime.date.today()
        self.holiday_dict = {}
        self.display_description_variable = tkinter.StringVar(self.display_frame)
        self.button_list = []

    def setup_calendar(self):
        self.main_window.title("Calendar")
        self.main_window.geometry("601x381")
        self.main_window["padx"] = 4
        self.main_window["pady"] = 10
        self.main_window.minsize(301, 381)
        self.main_window.maxsize(301, 381)

        current_day = f"{self.current_date.day}/{self.current_date.month}/{self.current_date.year }"
        self.holiday_dict[current_day] = "Current day"

        for x in range(self.current_date.year - 20, self.current_date.year + 20):
            holidays = Poland().holidays(x)
            for holiday in holidays:
                dictionary_key = f"{holiday[0].day}/{holiday[0].month}/{holiday[0].year}"
                self.holiday_dict[dictionary_key] = holiday[1]

        today_label = tkinter.Label(self.main_window, text=self.display_date_string(self.current_date),
                                    font="arial 10 italic", background="#E0E0E0")
        today_label.grid(row=0, column=0, columnspan=7, sticky="snew")

        year_left_arrow = tkinter.Button(self.main_window, text="<",
                                         command=self.left_arrow_year, background="#E0E0E0")
        year_left_arrow.grid(row=1, column=0)
        year_right_arrow = tkinter.Button(self.main_window, text=">",
                                          command=self.right_arrow_year, background="#E0E0E0")
        year_right_arrow.grid(row=1, column=6)

        self.year_text.set(self.get_year(self.current_date))
        year_label = tkinter.Label(self.main_window, textvariable=self.year_text, font="arial 12")
        year_label.grid(row=1, column=1, columnspan=5, sticky="news")

        month_left_arrow = tkinter.Button(self.main_window, text="<",
                                          command=self.left_arrow_month, background="#E0E0E0")
        month_left_arrow.grid(row=2, column=0)
        month_right_arrow = tkinter.Button(self.main_window, text=">",
                                           command=self.right_arrow_month, background="#E0E0E0")
        month_right_arrow.grid(row=2, column=6)

        self.month_text.set(self.get_month_name(self.current_date))
        month_label = tkinter.Label(self.main_window, textvariable=self.month_text, font="arial 12")
        month_label.grid(row=2, column=1, columnspan=5, sticky="news")

        for i in range(7):
            day_name = tkinter.Label(self.main_window, text=self.days_list[i], background="#C0C0C0")
            day_name.grid(row=3, column=i, sticky="news")

        self.display_frame.grid(row=10, column=0, columnspan=7, rowspan=4, sticky="we")

        self.display_date_variable = tkinter.StringVar(self.display_frame)
        self.display_date_variable.set(self.display_date_string(self.current_date))
        display_date = tkinter.Label(self.display_frame, textvariable=self.display_date_variable,
                                     font="arial 13 italic", anchor="w")
        display_date.grid(row=0, column=0, rowspan=2, sticky='news')

        self.display_description_variable = tkinter.StringVar(self.display_frame)
        self.display_description_variable.set("Current day")
        display_description = tkinter.Label(self.display_frame, textvariable=self.display_description_variable,
                                            height=3, anchor="w")
        display_description.grid(row=2, column=0, rowspan=2, sticky='news')

    def create_calendar(self, date_in_time):
        if self.button_list:
            for instance in self.button_list:
                instance.destroy()
        day_number = 1
        first_days = 1
        next_month_days = 1
        days_of_last_month = self.get_first_day_of_month(date_in_time) - 2
        last_month_days = self.get_last_month(datetime.date((self.year_text.get()),
                                                            (self.months.index(self.month_text.get()) + 1),
                                                            1)) - days_of_last_month
        for row in range(4, 10):
            for column in range(7):
                next_month_days_condition = day_number > self.get_days_in_month(date_in_time)
                day_button = tkinter.Button(self.main_window,
                                            bg=self.calendar_background_weekend_checker(column),
                                            fg=self.calendar_foreground_weekend_checker(column),
                                            font=self.calendar_bold_weekend_checker(column))
                self.button_list.append(day_button)
                day_button.configure(command=lambda button=day_button: self.check_day(button))
                day_button.grid(row=row, column=column, sticky="news")
                day_key = f"{day_number}/{date_in_time.month}/{date_in_time.year}"
                if first_days < self.get_first_day_of_month(date_in_time):
                    day_button.config(text=last_month_days, fg="grey", state="disabled")
                    last_month_days += 1
                    first_days += 1
                elif not next_month_days_condition:
                    if day_key in self.holiday_dict:
                        if self.holiday_dict[day_key] == "Current day":
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

    def display_date_string(self, date_in_time):
        today = self.days[date_in_time.isoweekday() - 1]
        return f"{today}, {self.months[date_in_time.month-1]} {date_in_time.day}, {date_in_time.year}"

    def get_month_name(self, date_in_time):
        current_month = date_in_time.month
        return self.months[current_month - 1]

    def get_first_day_of_month(self, date_in_time):
        return datetime.date(self.get_year(date_in_time), self.get_month(date_in_time), 1).isoweekday()

    def get_days_in_month(self, date_in_time):
        return max(calendar.monthrange(self.get_year(date_in_time), self.get_month(date_in_time)))

    def get_last_month(self, date_in_time):
        if date_in_time.month == 1:
            year = date_in_time.year - 1
            month = 12
            last_month_date = datetime.date(year, month, 1)
            return self.get_days_in_month(last_month_date)
        else:
            month = date_in_time.month - 1
            last_month_date = datetime.date(date_in_time.year, month, 1)
            return self.get_days_in_month(last_month_date)

    def left_arrow_month(self):
        if self.months.index(self.month_text.get()) + 1 == 1:
            self.month_text.set(self.months[11])
            month = 12
            year = self.year_text.get() - 1
            self.create_calendar(datetime.date(year, month, 1))
            self.year_text.set(self.year_text.get() - 1)
        else:
            self.month_text.set(self.months[self.months.index(self.month_text.get()) - 1])
            month = self.months.index(self.month_text.get()) + 1
            year = self.year_text.get()
            self.create_calendar(datetime.date(year, month, 1))

    def right_arrow_month(self):
        if self.months.index(self.month_text.get()) + 1 == 12:
            self.month_text.set(self.months[0])
            month = 1
            year = self.year_text.get() + 1
            self.create_calendar(datetime.date(year, month, 1))
            self.year_text.set(self.year_text.get() + 1)
        else:
            self.month_text.set(self.months[self.months.index(self.month_text.get()) + 1])
            month = self.months.index(self.month_text.get()) + 1
            year = self.year_text.get()
            self.create_calendar(datetime.date(year, month, 1))

    def left_arrow_year(self):
        self.create_calendar(datetime.date((self.year_text.get() - 1),
                                           (self.months.index(self.month_text.get()) + 1), 1))
        self.year_text.set(self.year_text.get() - 1)

    def right_arrow_year(self):
        self.create_calendar(datetime.date((self.year_text.get() + 1),
                                           (self.months.index(self.month_text.get()) + 1), 1))
        self.year_text.set(self.year_text.get() + 1)

    def check_day(self, day_button):
        day_of_month = day_button["text"]
        date_string = self.display_date_string(datetime.date((self.year_text.get()),
                                                             (self.months.index(self.month_text.get()) + 1),
                                                             day_of_month))
        self.display_date_variable.set(date_string)
        day_key = f"{day_of_month}/{self.months.index(self.month_text.get())+1}/{self.year_text.get()}"
        if day_key in self.holiday_dict:
            self.display_description_variable.set('   ' + self.holiday_dict[day_key])
        else:
            self.display_description_variable.set('   ' + "(...)")

    @staticmethod
    def get_year(date_in_time):
        return date_in_time.year

    @staticmethod
    def get_month(date_in_time):
        return date_in_time.month

    @staticmethod
    def calendar_background_weekend_checker(column):
        if column / 5 == 1 or column / 6 == 1:
            return "#FFFFFF"

    @staticmethod
    def calendar_foreground_weekend_checker(column):
        if column / 5 == 1 or column / 6 == 1:
            return "#404040"

    @staticmethod
    def calendar_bold_weekend_checker(column):
        weekend_condition = (column / 5 == 1 or column / 6 == 1)
        if weekend_condition:
            return 'arial 10 bold'
        else:
            return 'arial 10'

    def start_calendar(self):
        self.main_window.mainloop()


if __name__ == "__main__":
    calendar_runner = Calendar()
    calendar_runner.setup_calendar()
    calendar_runner.create_calendar(datetime.date.today())
    calendar_runner.start_calendar()
