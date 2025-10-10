from datetime import datetime
from dateutil.relativedelta import relativedelta
import drawsvg as svg

class Cursor:
    def __init__(self, pos=(0,0), jump=(0,20)):
        self.__og_x, self.__og_y = pos
        self._x, self._y = pos
        self._jump = jump[1]
    
    def set_y(self, y):
        self._y = y
    
    def set_x(self, x):
        self._x = x
    
    def set_pos(self, pos):
        self._x, self._y = pos
 
    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def jump_line(self):
        self._y += self._jump
        return self._y - self._jump

    def reset(self):
        self._x = self.__og_x
        self._y = self.__og_y


def plural(num):
    return "s" if num != 1 else ""

def get_time_since(date):
    time_delta = relativedelta(datetime.today(), date)

    years = time_delta.years
    months = time_delta.months
    days = time_delta.days

    return f"{years} year{plural(years)}, {months} month{plural(months)}, {days} day{plural(days)}"

def get_separation_dots(total_size: int, str1: str, str2: str):
    return "."*(total_size-len(str1)-len(str2))

def format_line(cursor, str1, str2, size=55):
    str1, str2 = str(str1), str(str2)
    line = svg.Text('', 16, x=cursor.get_x(), y=cursor.jump_line())
    line.append(svg.TSpan(f" {str1}:", class_="key"))
    #line.append(svg.TSpan(f":"))
    line.append(svg.TSpan(f" {get_separation_dots(size, str1, str2)} ", class_="dots"))
    line.append(svg.TSpan(str2, class_="value"))
    
    return line