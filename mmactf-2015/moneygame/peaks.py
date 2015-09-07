stock1 = [10000, 9033, 8051, 8435, 9318, 10244, 11037, 10801, 10118, 10114, 10473, 11097, 11462, 10501, 11127, 10513, 9655, 9707, 9601, 10583, 10751, 10796, 11045, 10183, 10524, 11243, 12040, 11141, 10378, 10183, 10823, 10302, 9772, 8845, 8076, 7900, 7793, 7465, 7833, 8803, 9276, 9956, 9840, 10176, 9366, 8994, 9474, 10033, 9834, 10492, 10718, 11275, 11086, 10322, 10851]

stock2 = [10000, 9770, 9455, 9210, 8943, 8086, 7756, 7029, 6461, 5728, 5175, 5000, 5613, 5167, 5000, 5000, 5000, 5000, 5000, 5345, 5000, 5884, 5689, 5534, 5000, 5971, 5083, 5247, 5862, 6459, 6223, 6589, 5760, 6628, 6836, 6762, 6041, 6979, 6153, 6132, 5751, 5406, 5531, 5729, 5715, 6083, 5343, 5275, 6132, 6516, 6372, 5464, 5440, 6310, 5369]
stock3 = [10000, 9184, 8859, 9445, 9649, 8847, 9200, 10043, 10574, 11203, 12081, 11285, 11175, 11820, 11198, 10276, 10024, 9602, 9613, 9448, 9287, 8721, 7767, 6924, 6517, 6028, 5250, 5000, 5045, 5992, 5198, 5846, 5298, 5595, 5476, 5328, 5000, 5243, 5100, 5000, 5000, 5697, 6123, 6416, 5916, 5899, 5718, 5474, 5405, 6315, 5400, 5000, 5000, 5735, 5455]


#a = [0, 5, 6, 7, 1, 0]

def get_peaks(nums):
    start = nums[0]
    points = [('start', start, 0)]

    looking_for = ''

    curr = start

    for index,num in enumerate(nums[1:]):
        if not looking_for:
            if num < curr:
                looking_for = 'Valley'
            else:
                looking_for = 'Peak'

        if index == (len(nums)-2):
            last_value_index = points[-1][2]
            last_value = abs(nums[last_value_index]-num)
            points.append((looking_for, last_value_index, index+1, last_value))

        elif looking_for == 'Valley':
            if num > curr:
                last_value_index = points[-1][2]
                last_value = abs(nums[last_value_index]-curr)
                points.append(('Valley', last_value_index, index, last_value))
                looking_for = 'Peak'

        elif looking_for == 'Peak':
            if num < curr:
                last_value_index = points[-1][2]
                last_value = abs(nums[last_value_index]-curr)
                points.append(('Peak', last_value_index, index, last_value))
                looking_for = 'Valley'

        curr = num

    peaks = [item for item in points if item[0] == 'Peak']
    return peaks

peaks = [list(item) + ['1'] for item in get_peaks(stock1)]
peaks += [list(item) + ['2'] for item in get_peaks(stock2)]
peaks += [list(item) + ['3'] for item in get_peaks(stock3)]

peaks = sorted(peaks, key=lambda x: x[3])[::-1]

actions = [''] * 54
print actions

for peak in peaks:
    _, start, stop, _, stock_num = peak
    # Action already happening on this day, don't overwrite it
    if actions[start]:
        continue

    print peak
    actions[start] = ('Buy', str(stock_num))
    for index in xrange(start+1, stop):
        if actions[index]:
            actions[index-1] = ('Sell', str(stock_num))
            break
        else:
            actions[index] = ('Rest', str(stock_num))
    else:
        try:
            actions[stop] = ('Sell', str(stock_num))
        except:
            actions[stop-1] = ('Sell', str(stock_num))


final = []
for action in actions:
    if not action:
        final.append(('Rest', '0'))
        continue
    final.append(action)

print final
