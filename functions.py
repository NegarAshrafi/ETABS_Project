
def filtering(list, prefix: tuple) -> list:
    """
    give a list of strings and a tuple of prefix, filtered the list
    by items started with prefix
    """
    filtered_loads = filter(lambda x:  x.startswith(prefix), list)
    return filtered_loads


def num_to_chr_cell(num: int) -> str:

    chrnum = num + 96
    if num < 27:
        return chr(chrnum)
    elif num <= 52:
        return chr(97) + chr(chrnum - 26)
    elif num <= 52 + 26:
        return chr(97 + 1)+chr(chrnum - 26 - 26)
    else:
        return None


def rowcol_to_xlsxcell(first_col: int, first_row: int, last_col: int, last_row: int) -> str:
    """
    get first and last column and rows and return excel cell name
    """
    a = num_to_chr_cell(first_col)
    n1 = first_row
    b = num_to_chr_cell(last_col)
    n2 = last_row
    cell = f'{a}{n1}:{b}{n2}'
    return cell


def strlist_to_floatlist(listobj: list) -> list:

    newlist = []
    for i in listobj:
        try:
            tmp = float(i)
            newlist.append(tmp)

        except ValueError:
            newlist.append(i)
    return newlist
