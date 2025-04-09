import time

def bpm_to_cc(bpm):
    data1 = 0

    if bpm > 127:
        data1 = 1

        data2 =  bpm - 128
    else:
        data2 = bpm

    return [data1, min(data2, 127)]

print(bpm_to_cc(251))