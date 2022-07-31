import datetime
import mmh3
import pprint

AS_OF = datetime.datetime(2000, 1, 1)


def get_window_index(date_obj, window):
    daydelta = (date_obj - AS_OF).days
    window_index = daydelta // window
    index_within_window = daydelta % window
    return window_index, index_within_window


def shuffle(date_obj, menu_list, window):
    num_of_menus = window * 2  # lunch + dinner
    epoch = str(date_obj.timestamp())
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
    this_window_index, begin_index = get_window_index(from_date_obj, window)

    this_window_obj = AS_OF + datetime.timedelta(days=this_window_index * window)
    last_window_obj = this_window_obj - datetime.timedelta(days=window)

    final_menu = []
    last_window_menu = shuffle(last_window_obj, menu_list.copy(), window)

    while len(final_menu) < (begin_index + length) * 2:
        this_window_menu = shuffle(this_window_obj, menu_list.copy(), window)
        dedup(this_window_menu, last_window_menu[-dedup_days * 2:], dedup_days)
        final_menu += this_window_menu

        last_window_menu = this_window_menu
        this_window_obj += datetime.timedelta(days=window)

    final_menu = zip_lunch_dinner(final_menu)[begin_index:begin_index + length]
    dates = get_date_list(from_date_obj, length)
    return dict(zip(dates, final_menu))


menu_list = [
    '카레', '떡볶이', '짜장', '김치볶음밥', '미역국', '라면', '된장찌개', '김치찌개', '계란찜', '멸치볶음', '북어국', '비빔국수', '미트볼',
    '삼겹살', '소고기무국', '두부조림', '계란말이', '소고기볶음밥', '콩나물불고기', '오뎅볶음', '파스타', '칠리새우', '순두부찌개', '김밥']


if __name__ == "__main__":
    result = generate_menu('2022-06-22', 31, menu_list, 4)
    pprint.pprint(result)
