def isafter1445(timestr):
    h=int(timestr[0:2])
    m=int(timestr[3:5])
    #print(f'Timestr being tested is {timestr}')
    if (h == 14 and m >= 45) or h == 15:
        return 1
    else:
        return 0

def getsignal(open_pos_prop, mychart, prev_close, current_row):
    signal = open_pos_prop[0]
    pos_open = open_pos_prop[1]
    trade_open = open_pos_prop[2]
    sl = open_pos_prop[3]
    risk = open_pos_prop[4]
    
    if isafter1445(current_row[0][11:19]) == 0:
        if prev_close != 0:
            if float(current_row[1]) > (1.0025 * prev_close):
                signal = 1
                pos_open = float(current_row[1])
                trade_open = current_row[0]
                print(f'0.25 percent above prev_close is {1.0025 * prev_close}. Open of current row is {float(current_row[1])}')
                print(f'1. SIGNAL to go long at {pos_open} at {trade_open}')
                sl = pos_open - 100
                risk = pos_open - sl
                print(f'SL at {sl}. Risk is {risk}')
            elif float(current_row[2]) > (1.0025 * prev_close):
                signal = 1
                pos_open = float(current_row[2])
                trade_open = current_row[0]
                print(f'0.25 percent above prev_close is {1.0025 * prev_close}. High of current row is {float(current_row[2])}')
                print(f'2. SIGNAL to go long at {pos_open} at {trade_open}')
                sl = pos_open - 100
                risk = pos_open - sl
                print(f'SL at {sl}. Risk is {risk}')
        
    open_pos_prop = [signal, pos_open, trade_open, sl, risk]
    return open_pos_prop
        