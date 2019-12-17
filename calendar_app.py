import tkinter
import datetime
import calendar
from workalendar.europe import Poland


class Calendar:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    days_list = [day[:3] for day in days]

    months = ["January", "February", "March", "April",
              "May", "June", "July", "August",
              "September", "October", "November", "December"
              ]

    def __init__(self):
        self.main_window = tkinter.Tk()
        self.month_text = tkinter.StringVar()
        self.year_text = tkinter.IntVar()
        self.description_frame = tkinter.LabelFrame(self.main_window, text="Date Details", borderwidth=1)
        self.description_date = None
        self.description_text = None
        self.current_date = datetime.date.today()
        self.buttons = []

    def setup_window(self):
        self._general_setup()
        self._declare_range_for_holidays()
        today_button = tkinter.Button(self.main_window, text=self.get_date_string(self.current_date),
                                      font="arial 10 italic",
                                      command=self.default_start, background="#E0E0E0")
        today_button.grid(row=0, column=0, columnspan=7, sticky="snew")
        self._set_arrows(1, 'year')
        self._set_arrows(2, 'month')
        for i in range(7):
            day_name = tkinter.Label(self.main_window, text=self.days_list[i], background="#C0C0C0")
            day_name.grid(row=3, column=i, sticky="news")

    def default_start(self):
        date = datetime.date.today()
        self.month_text.set(self._get_month_name(date))
        self.year_text.set(date.year)
        self._set_date_related_elements(date)
        self._create_calendar(date)
        self._start_calendar()

    def _get_month_name(self, date_in_time):
        return self.months[date_in_time.month - 1]

    def _set_date_related_elements(self, date):
        self.description_frame.grid(row=10, column=0, columnspan=7, rowspan=4, sticky="we")
        self.description_date = tkinter.StringVar(self.description_frame)
        date_label = tkinter.Label(
            self.description_frame,
            textvariable=self.description_date,
            font="arial 13 italic",
            anchor="w")
        date_label.grid(row=0, column=0, rowspan=2, sticky='news')
        self.description_date.set(self.get_date_string(date))
        self.description_text = tkinter.StringVar(self.description_frame)
        description_label = tkinter.Label(
            self.description_frame,
            textvariable=self.description_text,
            height=3,
            anchor="w")
        description_label.grid(row=2, column=0, rowspan=2, sticky='news')
        self.description_text.set("   Current day")

    def _start_calendar(self):
        self.main_window.mainloop()

    @staticmethod
    def get_day_background(column):
        if column / 5 == 1 or column / 6 == 1:
            return "#FFFFFF"
        else:
            return "#d9d9d9"

    @staticmethod
    def get_day_foreground(column):
        if column / 5 == 1 or column / 6 == 1:
            return "#404040"
        else:
            return "black"

    @staticmethod
    def get_day_font(column):
        weekend_condition = (column / 5 == 1 or column / 6 == 1)
        if weekend_condition:
            return 'arial 10 bold'
        else:
            return 'arial 10'

    @staticmethod
    def get_first_day_of_month_number(date_in_time):
        return datetime.date(date_in_time.year, date_in_time.month, 1).isoweekday()

    @staticmethod
    def get_days_in_month(date_in_time):
        return max(calendar.monthrange(date_in_time.year, date_in_time.month))

    def _set_arrows(self, row, block_type):
        left_arrow_method = self.__getattribute__(f"get_last_{block_type}")
        right_arrow_method = self.__getattribute__(f"get_next_{block_type}")
        text_method = self.__getattribute__(f"{block_type}_text")
        left_arrow = tkinter.Button(self.main_window, text="<",
                                    command=left_arrow_method, background="#E0E0E0")
        left_arrow.grid(row=row, column=0)
        right_arrow = tkinter.Button(self.main_window, text=">",
                                     command=right_arrow_method, background="#E0E0E0")
        right_arrow.grid(row=row, column=6)
        label = tkinter.Label(self.main_window, textvariable=text_method, font="arial 12")
        label.grid(row=row, column=1, columnspan=5, sticky="news")

    def _general_setup(self):
        self.main_window.title("Calendar")
        self.main_window.geometry("601x381")
        self.main_window["padx"] = 4
        self.main_window["pady"] = 10
        self.main_window.minsize(301, 391)
        self.main_window.maxsize(301, 391)

    @staticmethod
    def _format_holidays_key(day, month, year):
        return f'{day}/{month}/{year}'

    def _declare_range_for_holidays(self):
        current_day = self._format_holidays_key(
            day=self.current_date.day,
            month=self.current_date.month,
            year=self.current_date.year)
        HOLIDAYS[current_day] = "Current day"
        for x in range(self.current_date.year - 20, self.current_date.year + 20):
            holidays = Poland().holidays(x)
            for holiday in holidays:
                dictionary_key = self._format_holidays_key(
                    day=holiday[0].day,
                    month=holiday[0].month,
                    year=holiday[0].year)
                HOLIDAYS[dictionary_key] = holiday[1]

    def get_date_string(self, date_in_time):
        today = self.days[date_in_time.isoweekday() - 1]
        return f"{today}, {self.months[date_in_time.month-1]} {date_in_time.day}, {date_in_time.year}"

    def get_days_of_last_month(self, date_in_time):
        if date_in_time.month == 1:
            year = date_in_time.year - 1
            month = 12
            last_month_date = datetime.date(year, month, 1)
        else:
            month = date_in_time.month - 1
            last_month_date = datetime.date(date_in_time.year, month, 1)
        return self.get_days_in_month(last_month_date)

    def get_last_month(self):
        if self.months.index(self.month_text.get()) + 1 == 1:
            self.month_text.set(self.months[11])
            month = 12
            year = self.year_text.get() - 1
        else:
            self.month_text.set(self.months[self.months.index(self.month_text.get()) - 1])
            month = self.months.index(self.month_text.get()) + 1
            year = self.year_text.get()
        self._create_calendar(datetime.date(year, month, 1))

    def get_next_month(self):
        if self.months.index(self.month_text.get()) + 1 == 12:
            self.month_text.set(self.months[0])
            month = 1
            year = self.year_text.get() + 1
            self.year_text.set(self.year_text.get() + 1)
        else:
            self.month_text.set(self.months[self.months.index(self.month_text.get()) + 1])
            month = self.months.index(self.month_text.get()) + 1
            year = self.year_text.get()
        self._create_calendar(datetime.date(year, month, 1))

    def get_last_year(self):
        self._create_calendar(datetime.date((self.year_text.get() - 1),
                                            (self.months.index(self.month_text.get()) + 1), 1))
        self.year_text.set(self.year_text.get() - 1)

    def get_next_year(self):
        self._create_calendar(datetime.date((self.year_text.get() + 1),
                                            (self.months.index(self.month_text.get()) + 1), 1))
        self.year_text.set(self.year_text.get() + 1)

    def get_day_description(self, day_button):
        day_of_month = day_button["text"]
        date_string = self.get_date_string(datetime.date((self.year_text.get()),
                                                         (self.months.index(self.month_text.get()) + 1),
                                                         day_of_month))
        self.description_date.set(date_string)
        day_key = self._format_holidays_key(
            day=day_of_month,
            month=self.months.index(self.month_text.get())+1,
            year=self.year_text.get())
        description = HOLIDAYS.get(day_key, "(...)")
        self.description_text.set('   ' + description)

    def _create_calendar(self, date):
        [instance.destroy() for instance in self.buttons]
        current_month_day = 1
        next_month_day = 1

        days_of_last_month = self.get_days_of_last_month(
            datetime.date((self.year_text.get()), date.month, 1))
        last_month_number = (date - datetime.timedelta(days=5)).month
        next_month_number = (date + datetime.timedelta(days=35)).month
        remaining_last_month_day = days_of_last_month - (self.get_first_day_of_month_number(date) - 2)
        for row in range(4, 10):
            for column in range(7):
                calendar_button = CalendarButton(column)
                if remaining_last_month_day <= days_of_last_month:
                    button_number = remaining_last_month_day
                    calendar_button.fg = "grey"
                    month = last_month_number
                    remaining_last_month_day += 1
                elif not current_month_day > self.get_days_in_month(date):
                    button_number = current_month_day
                    calendar_button.state = "normal"
                    month = date.month
                    current_month_day += 1
                else:
                    button_number = next_month_day
                    calendar_button.fg = "grey"
                    month = next_month_number
                    next_month_day += 1

                day_key = self._format_holidays_key(day=button_number, month=month, year=date.year)
                calendar_button.set_if_holiday(day_key)
                day_button = tkinter.Button(
                    self.main_window,
                    bg=calendar_button.bg,
                    fg=calendar_button.fg,
                    font=calendar_button.font,
                    state=calendar_button.state,
                    text=button_number)
                day_button.configure(command=lambda button=day_button: self.get_day_description(button))
                day_button.grid(row=row, column=column, sticky="news")
                self.buttons.append(day_button)


HOLIDAYS = {}


class CalendarButton:
    def __init__(self, column):
        self.state = "disabled"
        self.is_weekend = column / 5 == 1 or column / 6 == 1
        self.font = "arial 10 bold" if self.is_weekend else "arial 10"
        self.bg = None
        self.fg = None

    def set_if_holiday(self, day_key):
        if day_key in HOLIDAYS:
            self.bg = "#A0A0A0" if HOLIDAYS[day_key] == "Current day" else "#C0C0C0"
            self.fg = "#FFFFFF"
        else:
            self.bg = "#FFFFFF" if self.is_weekend else "#d9d9d9"
            self.fg = "#404040" if self.is_weekend else "black"


if __name__ == "__main__":
    calendar_runner = Calendar()
    calendar_runner.setup_window()
    calendar_runner.default_start()
