## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from os import path

def is_cpufreq_configured():
    return path.exists("/sys/devices/system/cpu/cpu0/cpufreq/")

def sys_get_cpu_max_freq():
    with open("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq") as f:
        data = f.read()
        return data[:-1]

def sys_get_cpu_min_freq():
    with open("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_min_freq") as f:
        data = f.read()
        return data[:-1]

def sys_get_cpu_current_freq():
    with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq") as f:
        data = f.read()
        return data[:-1]

def sys_get_cpu_max_scaling_freq():
    with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq") as f:
        data = f.read()
        return data[:-1]


def sys_set_cpu_max_scaling_freq(freq):
    i=0
    while True:
        filename="/sys/devices/system/cpu/cpu{}/cpufreq/scaling_max_freq".format(i)
        if path.exists(filename)==True:
            with open(filename,"w") as f:
                f.write(str(freq))
            i=i+1
        else:
            break



def sys_set_cpu_turbo(boolean):
    if boolean==True:
        s="0"
    else:
        s="1"
    filename="/sys/devices/system/cpu/intel_pstate/no_turbo"
    with open(filename,"w") as f:
        f.write(s)


if __name__ == '__main__':
    sleeptime=2
    from time import sleep
    
    print("Is kernel cpufreq configured?:", is_cpufreq_configured())

    print("Max cpu freq is {}".format(sys_get_cpu_max_freq()))

    print("Min cpu freq is {}".format(sys_get_cpu_min_freq()))

    print("Current cpu freq is {}".format(sys_get_cpu_current_freq()))

    print("Changing cpu to maximum scaling freq")
    sys_set_cpu_max_scaling_freq(sys_get_cpu_max_freq())
    sleep(sleeptime)
    print("Current cpu max scaling freq is {}".format(sys_get_cpu_max_scaling_freq()))

    print("Disabling turbo")
    sys_set_cpu_turbo(False)
    sleep(sleeptime)
    print("Current cpu max scaling freq is {}".format(sys_get_cpu_max_scaling_freq()))

    print("Enabling turbo")
    sys_set_cpu_turbo(True)
    sleep(sleeptime)
    print("Current cpu max scaling freq is {}".format(sys_get_cpu_max_scaling_freq()))


    print("Changing cpu to minimum scaling freq")
    sys_set_cpu_max_scaling_freq(sys_get_cpu_min_freq())
    sleep(sleeptime)
    print("Current cpu max scaling freq is {}".format(sys_get_cpu_max_scaling_freq()))

