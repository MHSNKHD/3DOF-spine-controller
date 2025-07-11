# calibration.py
# oliverwigger

import numpy as np
import statistics as sta
import logging as log
import traceback

#get peaks
def _get_peaks(data, window_size):
    try:
        maxima_indices = []
        n = len(data)
        for i in range(n):
            is_local_max = True
            for j in range(1, window_size + 1):
                if i - j >= 0 and data[i - j] >= data[i]:
                    is_local_max = False
                    break
                if i + j < n and data[i + j] > data[i]:
                    is_local_max = False
                    break
            if is_local_max:
                maxima_indices.append(i)
        return np.array(maxima_indices)

    except Exception as e:
        log.error("_get_peaks")
        log.error(e)


#sync angle with torque signal
def _sync(angle, torque):
    try:
        index_a = _get_peaks(angle, 30)
        index_t = _get_peaks(torque, 30)
        
        #index_a = next(i for i in range(1, len(angle)-1) if angle[i] > angle[i-1] and angle[i] > angle[i+1])
        #index_t = next(i for i in range(index_a, len(torque)-1) if torque[i] > torque[i-1] and torque[i] > torque[i+1])
        
        try: 
            diff = index_t-index_a
            shift = int(sta.median(diff))
            #print(f"shift: {shift}")
        except:
            shift = 0
            print('Shift error')
        
        torque = torque[shift:]
        angle = angle[:-shift]
        
        return (angle, torque)
    
    except Exception as e:
        log.error("_sync")
        log.error(e)
    
    


#fit polynom to data and return fitted values
def _polyfit(angle, torque, degree):
    try:
        z = np.polyfit(angle, torque, degree)
        f = np.poly1d(z)

        max_a = max(angle)
        min_a = min(angle)

        #print(f"max_a: {max_a}, min_a: {min_a}")
        #print(f"middle: {round(min_a+(max_a-min_a)/2,2)}")

        x_fit = np.linspace(min_a, max_a, 1000) #len(buckets)+1
        y_fit = f(x_fit)
        
        cut_amount = int(len(y_fit) * 0.2)  # Calculate 20% of the length
        x_fit = x_fit[cut_amount:len(x_fit) - cut_amount]
        y_fit = y_fit[cut_amount:len(y_fit) - cut_amount]
        
        return(x_fit, y_fit)
    
    except Exception as e:
        log.error("_polyfit")
        log.error(e)
        traceback.print_exc()


#return the zeropoint of the sample
def _get_zeropoint(x_fit, y_fit):
    diff = [(y_fit[i] - y_fit[i - 1])*50 for i in range(1, len(y_fit))]
    angle0 = x_fit[np.where(diff == min(diff))[0]]
    torque0 = y_fit[np.where(diff == min(diff))[0]]

    return (angle0, torque0)


#MAIN
def calibrate(angle, torque):
    angle, torque = _sync(angle, torque)
    x_fit, y_fit = _polyfit(angle, torque, 3)
    angle0, torque0 = _get_zeropoint(x_fit, y_fit)
    
    return(angle0, torque0)
    #return(angle0, 0)