def strZero(int):
    """Returns a string from an int, if it's < 10,
    It will add a zero in front of it.

    :param int: the integer you want to convert
    :type int: int
    :rtype: string
    """
    if int < 10:
        return "0"+str(int)
    return str(int)

def int2month(num):
    """Convert a int to a month (number between 0-11)

    :param num: number given
    :type num: int
    :return: month between 0 and 11
    :rtype: int
    """
    if num<0:
        return 12+num
    elif num>11:
        return num-12
    return num
