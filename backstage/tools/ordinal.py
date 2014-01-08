def ordinal(num):
    num = int(num)
    return '%d%s' % (num, { 11: 'th', 12: 'th', 13: 'th' }.get(num % 100, { 1: 'st',2: 'nd',3: 'rd',}.get(num % 10, 'th')))
