import random
import xlrd
import xlsxwriter


def coupon_generator():
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*"
    sa = []
    for i in range(8):
        sa.append(random.choice(seed))
    coupon = ''.join(sa)
    return coupon


def excel_generator(li):
    """none"""
    path = '/Users/huaqiang/Downloads'
    workbook = xlsxwriter.Workbook(path + '/coupon_list.xlsx')
    table = workbook.add_worksheet('coupon')
    table.write(0, 0, '优惠码')
    table.write(1, 0, '姓名')
    table.write(2, 0, '手机号')
    row = 1
    for item in li:
        table.write(row, 0, item)
        row = row + 1

    workbook.close()


def main():
    coupon_list = []

    for i in range(10000):
        coupon_list.append(coupon_generator())

    for i in range(10000):
        if coupon_list[i] in coupon_list[i+1:]:
            print(i)
    excel_generator(coupon_list)



if __name__ == '__main__':
    main()
