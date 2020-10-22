def isafter1520(timestr):
    h=int(timestr[0:2])
    m=int(timestr[3:5])
    if (h == 15 and m >= 20):
        return 1
    else:
        return 0



def managetrade(all_positions, mychart, current_row):

    open_pos_prop = all_positions[0]
    closed_trades = all_positions[1]
    
    signal = open_pos_prop[0]
    pos_open = open_pos_prop[1]
    trade_open = open_pos_prop[2]
    sl = open_pos_prop[3]
    risk = open_pos_prop[4]
    
    if signal == 1:
        if float(current_row[1]) <= sl:
            print('*********')
            reward = float(current_row[1]) - pos_open
            trade_exit = current_row[0]
            reward2risk = reward/risk
            print(f'Position exited at {current_row[1]} due to SL hit at {current_row[0]}')
            print(f'Reward is {reward}. R2R is {reward2risk}')
            print('-------------------------------------------------------------------------------------------')
            closed_trades.append([current_row[0][0:4], current_row[0][5:7], current_row[0][8:10], pos_open, trade_open, risk, float(current_row[1]), trade_exit , reward, reward2risk])
            signal = 0
            pos_open = 0
            trade_open = 0
            sl = 0
            risk = 0        
        elif float(current_row[3]) <= sl:
            print('*********')
            reward = float(current_row[3]) - pos_open
            trade_exit = current_row[0]
            reward2risk = reward/risk
            print(f'Position exited at {current_row[3]} due to SL hit at {current_row[0]}')
            print(f'Reward is {reward}. R2R is {reward2risk}')
            print('-------------------------------------------------------------------------------------------')
            closed_trades.append([current_row[0][0:4], current_row[0][5:7], current_row[0][8:10], pos_open, trade_open, risk, float(current_row[3]), trade_exit , reward, reward2risk])
            signal = 0
            pos_open = 0
            trade_open = 0
            sl = 0
            risk = 0        
        elif isafter1520(current_row[0][11:19]):
            print('*********')
            reward = float(current_row[1]) - pos_open
            trade_exit = current_row[0]
            reward2risk = reward/risk
            print(f'Position exited at {current_row[1]} due to eod at {current_row[0]}')
            print(f'Reward is {reward}. R2R is {reward2risk}')
            print('-------------------------------------------------------------------------------------------')
            closed_trades.append([current_row[0][0:4], current_row[0][5:7], current_row[0][8:10], pos_open, trade_open, risk, float(current_row[3]), trade_exit , reward, reward2risk])
            signal = 0
            pos_open = 0
            trade_open = 0
            sl = 0
            risk = 0

    open_pos_prop = [signal, pos_open, trade_open, sl, risk]
    all_positions = [open_pos_prop, closed_trades]
    return all_positions