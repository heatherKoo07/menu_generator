import datetime
import mmh3
import pprint


def get_number_of_days(date_obj):
    return (date_obj.replace(month=date_obj.month % 12 + 1, day=1) - datetime.timedelta(days=1)).day


def get_window_index(day, window, num_of_days, menu_list):
    window_index = (day - 1) // window
    day_index = (day - 1) % window

    if window * (window_index + 1) > num_of_days:
        window_index -= 1
    if window * (window_index + 2) > num_of_days:
        window = num_of_days - window * window_index
    if len(menu_list) < window * 2:
        raise ValueError(f"You should have at least {window * 2} menus")
    return window_index, window, day_index


def shuffle(epoch, menu_list, num_of_days):
    num_of_menus = num_of_days * 2  # lunch + dinner
    epoch = str(epoch)
    seed = 0
    for _ in range(num_of_menus):
        hash_value0 = mmh3.hash(epoch, seed)
        hash_value1 = mmh3.hash(epoch, hash_value0)
        seed = hash_value1
        # swap
        i0 = hash_value0 % len(menu_list)
        i1 = hash_value1 % len(menu_list)
        menu_list[i0], menu_list[i1] = menu_list[i1], menu_list[i0]
    return menu_list[:num_of_menus]


def dedup(this_window_menu, last_dedup_menu, dedup_days):
    i = 0
    j = 1
    while i < dedup_days * 2:
        if this_window_menu[i] in last_dedup_menu:
            while this_window_menu[j] in last_dedup_menu:
                j += 1
            this_window_menu[i], this_window_menu[j] = this_window_menu[j], this_window_menu[i]
        i += 1
        j += 1


def zip_lunch_dinner(menu):
    return [{'lunch': menu[i], 'dinner': menu[i+1]} for i in range(len(menu)) if i % 2 == 0]


def get_date_list(from_date_obj, length):
    dates = []
    for i in range(length):
        dates.append(from_date_obj.strftime("%Y-%m-%d"))
        from_date_obj = from_date_obj + datetime.timedelta(days=1)
    return dates


def generate_menu(from_date_str, length, menu_list, dedup_days=5):
    """Requirements:

        Assume menu_list is sorted and loaded from db.
        if you change the dedup_days, the menu changes

        because the epoch changes.
    """
    window = dedup_days * 3
    if len(menu_list) < window * 2:
        raise ValueError(f"You should have at least {window * 2} menus")

    from_date_obj = datetime.datetime.strptime(from_date_str, "%Y-%m-%d")
    this_month_year, this_month = from_date_obj.year, from_date_obj.month

    last_month_year = this_month_year
    last_month = this_month - 1
    if this_month == 1:
        last_month_year -= 1
        last_month = 12
    last_month_obj = datetime.datetime(last_month_year, last_month, 1)

    this_month_num_of_days = get_number_of_days(from_date_obj)
    last_month_num_of_days = get_number_of_days(last_month_obj)

    this_window_index, this_window, begin_index = get_window_index(
        from_date_obj.day, window, this_month_num_of_days, menu_list)
    this_epoch = datetime.datetime(this_month_year, this_month,
                                   this_window_index * window + 1).timestamp()
    last_epoch = None
    last_window = window
    if this_window_index > 0:
        last_epoch = datetime.datetime(this_month_year, this_month,
                                       (this_window_index - 1) * window + 1).timestamp()
    else:
        last_window_index, last_window, _ = get_window_index(
            last_month_num_of_days, window, last_month_num_of_days, menu_list)
        last_epoch = datetime.datetime(last_month_year, last_month,
                                       last_window_index * window + 1).timestamp()

    final_menu = []
    last_window_menu = shuffle(last_epoch, menu_list.copy(), last_window)

    while len(final_menu) < (begin_index + length) * 2:
        this_window_menu = shuffle(this_epoch, menu_list.copy(), this_window)
        dedup(this_window_menu, last_window_menu[-dedup_days * 2:], dedup_days)
        final_menu += this_window_menu

        last_window_menu = this_window_menu
        next_possible_window_day = (this_window_index + 1) * window + 1

        if this_window > window or next_possible_window_day > this_month_num_of_days:
            next_month_year, next_month = this_month_year, this_month + 1
            if this_month == 12:
                next_month_year += 1
                next_month = 1
            next_month_obj = datetime.datetime(next_month_year, next_month, 1)
            this_epoch = next_month_obj.timestamp()
            this_window_index, this_window = 0, window
            this_month_num_of_days = get_number_of_days(next_month_obj)
            this_month_year, this_month = next_month_year, next_month
        else:
            this_epoch = datetime.datetime(this_month_year, this_month,
                                           next_possible_window_day).timestamp()
            this_window_index, this_window, _ = get_window_index(
                next_possible_window_day, window, this_month_num_of_days, menu_list)

    final_menu = zip_lunch_dinner(final_menu)[begin_index:begin_index + length]
    dates = get_date_list(from_date_obj, length)
    return dict(zip(dates, final_menu))


menu_list = [
    '카레', '떡볶이', '짜장', '김치볶음밥', '미역국', '라면', '된장찌개', '김치찌개', '계란찜', '멸치볶음', '북어국', '비빔국수', '미트볼',
    '삼겹살', '소고기무국', '두부조림', '계란말이', '소고기볶음밥', '콩나물불고기', '오뎅볶음', '파스타', '칠리새우', '순두부찌개', '김밥']


if __name__ == "__main__":
    result = generate_menu('2022-06-22', 31, menu_list, 4)
    pprint.pprint(result)
