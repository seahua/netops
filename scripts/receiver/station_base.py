from ..modules.station import Station


def hostmonitor_script(input_file):
    s = Station(input_file)
    file = s.get_hostmonitor_script(FW=1)
    return file


def switch_script(input_file):
    s = Station(input_file)
    file = s.get_switch_script()
    return file
