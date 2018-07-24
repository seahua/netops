from ..modules.station import Station


def test7():
    input_file = '/Users/huaqiang/Downloads/ceshi/template-2.xlsx'

    s = Station(input_file)
    file = s.get_hostmonitor_script(FW=0)
    # s.get_switch_script()
    # s.get_dir()
    print(file)

def test7_1():
    input_file = '/Users/huaqiang/Downloads/ceshi/template-2.xlsx'

    s = Station(input_file)
    site_list = s.get_site_list()
    print(site_list)

