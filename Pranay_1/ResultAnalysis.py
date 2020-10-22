#import libraries

import sys
import csv
import statistics

def returnavgofcol(column, list_of_list):
    new_list = []
    for i in list_of_list:
        new_list.append(i[column])
    return statistics.mean(new_list)

def returnmedianofcol(column, list_of_list):
    new_list = []
    for i in list_of_list:
        new_list.append(i[column])
    return statistics.median(new_list)

starting_capital = 1000000
capital = starting_capital
risk_percent = 0.01

#Variable for streaks
win_streak_trade_no = 0
lose_streak_trade_no = 0
win_streak_per = 0
lose_streak_per = 0
win_streak_begin = 0
win_streak_end = 0
lose_streak_begin = 0
lose_streak_end = 0
win_streaks = []
lose_streaks = []

#Variable for equity high & low
equity_high = capital
equity_high_trade_open = 0
equity_low = 0
equity_low_trade_open = 0

#Variablesfordrawdowns
current_drdwn_begin = 0
current_drdwn_close = 0
current_drdwn_no_trades = 0
current_drdwn_no_of_days = 0
current_drdwn_per = 0
drdwn = []

#Win/LossRates
win_R2R = []
loss_R2R = []

#Variablesformax
max_equity_low = capital

charges_slippage = 0
trades_not_taken = 0

#Import Results
with open('Nifty_Pranay_1.csv') as csv_file, open('Nifty_Pranay_1_Analysis.csv','w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(["Year", "Month", "Day", "Capital", "Max Risk", "No of lots", "Trade Risk", "Entry", "Entry Time", "Point Risk", "Exit", "Exit Time", "PnL" ,"New Capital"])
    nifty_5min_csv = csv.reader(csv_file, delimiter=',')
    rows = list(nifty_5min_csv)
    total_dataset = len(rows)
    
    #Initilize variables to calculate day's high and time
    new_capital = 0
    max_risk = 0
    
    point_risk = 0
    trade_risk_perlot = 0
    no_of_lots = 0
    trade_risk = 0
    trade_return = 0
    
    line_count = 1
    
    #Process data. Default rows to check entered in while
    while line_count < total_dataset:
        point_risk = float(rows[line_count][5])
        trade_risk_perlot = (point_risk * 75) / 2
        max_risk = risk_percent * capital
        if trade_risk_perlot <= max_risk:
            no_of_lots = max_risk // trade_risk_perlot
            trade_risk = no_of_lots * trade_risk_perlot
            trade_return = float(rows[line_count][9]) * trade_risk
            charges_slippage = 0.015 * no_of_lots * float (rows[line_count][3])
            new_capital = capital + trade_return #- charges_slippage            
            writer.writerow([rows[line_count][0], rows[line_count][1], rows[line_count][2], capital, max_risk, no_of_lots, trade_risk, rows[line_count][3], rows[line_count][4], rows[line_count][5], rows[line_count][6], rows[line_count][7], trade_return, new_capital])
            
            
            #Code for calculating drawdowns
            if new_capital < equity_high:
                if equity_low == 0:
                    current_drdwn_begin = rows[line_count][0] + '-' + rows[line_count][1] + '-' + rows[line_count][2] + " " + rows[line_count][4]
                    current_drdwn_no_trades = 1
                    equity_low = new_capital
                    equity_low_trade_open = rows[line_count][0] + '-' + rows[line_count][1] + '-' + rows[line_count][2] + " " + rows[line_count][4]


                if new_capital < equity_low:
                    equity_low = new_capital
                    equity_low_trade_open = rows[line_count][0] + '-' + rows[line_count][1] + '-' + rows[line_count][2] + " " + rows[line_count][4]
            
            if new_capital > equity_high:
                if current_drdwn_no_trades != 0:
                    current_drdwn_per = ((equity_high - equity_low)/equity_high)*100
                    current_drdwn_close = rows[line_count][0] + '-' + rows[line_count][1] + '-' + rows[line_count][2] + " " + rows[line_count][4]
                    drdwn.append([current_drdwn_no_trades-1, current_drdwn_no_of_days, current_drdwn_per, current_drdwn_begin, equity_low_trade_open, current_drdwn_close])
                    current_drdwn_no_trades = 0
                    current_drdwn_no_of_days = 0
                    
                    if equity_low < max_equity_low:
                        max_equity_low = equity_low
                    equity_low = 0
                    equity_low_trade_open = 0
                equity_high = new_capital
                equity_high_trade_open = rows[line_count][0] + '-' + rows[line_count][1] + '-' + rows[line_count][2] + " " + rows[line_count][4]

            if current_drdwn_no_trades != 0:
                current_drdwn_no_trades += 1
                current_drdwn_close = rows[line_count][0] + '-' + rows[line_count][1] + '-' + rows[line_count][2] + " " + rows[line_count][4]
                if rows[line_count][2] != rows[line_count-1][2]:
                    current_drdwn_no_of_days += 1
                
            #Code for calculating streaks
            if float(rows[line_count][9]) <= 0:
                loss_R2R.append(float(rows[line_count][9]))
                if lose_streak_trade_no == 0:
                    lose_streak_per = capital
                    lose_streak_begin = rows[line_count][0] + '-' + rows[line_count][1] + '-' + rows[line_count][2] + " " + rows[line_count][4]
                    if win_streak_trade_no > 1:
                        win_streak_end = rows[line_count-1][0] + '-' + rows[line_count-1][1] + '-' + rows[line_count-1][2] + " " + rows[line_count-1][4]
                        win_streak_per = (lose_streak_per - win_streak_per)/win_streak_per * 100
                        win_streaks.append([win_streak_trade_no, win_streak_per, win_streak_begin, win_streak_end])

                    win_streak_trade_no = 0
                    win_streak_per = 0
                lose_streak_trade_no += 1
                    
            elif float(rows[line_count][9]) > 0:
                win_R2R.append(float(rows[line_count][9]))
                if win_streak_trade_no == 0:
                    win_streak_per = capital
                    win_streak_begin = rows[line_count][0] + '-' + rows[line_count][1] + '-' + rows[line_count][2] + " " + rows[line_count][4]
                    if lose_streak_trade_no > 1:
                        lose_streak_end = rows[line_count-1][0] + '-' + rows[line_count-1][1] + '-' + rows[line_count-1][2] + " " + rows[line_count-1][4]
                        lose_streak_per = (lose_streak_per - win_streak_per)/lose_streak_per * 100
                        lose_streaks.append([lose_streak_trade_no, lose_streak_per, lose_streak_begin, lose_streak_end])
                    lose_streak_trade_no = 0
                    lose_streak_per = 0
                win_streak_trade_no += 1
        else:
            new_capital = capital
            trades_not_taken += 1
        trade_risk = 0
        trade_return = 0
        point_risk = 0
        trade_risk_perlot = 0
        max_risk = 0
        no_of_lots = 0
        capital = new_capital
        new_capital = 0
        line_count += 1
        

    if current_drdwn_no_trades != 0:
        current_drdwn_per = ((equity_high - equity_low)/equity_high)*100
        drdwn.append([current_drdwn_no_trades-1, current_drdwn_no_of_days, current_drdwn_per, current_drdwn_begin, equity_low_trade_open, current_drdwn_close])
    #Similar bit to be done for drawdowns at end of file

print('Analysis done. Check output file')

winrate_per = len(win_R2R) / (len(win_R2R) + len(loss_R2R)) * 100
lossrate_per = len(loss_R2R) / (len(win_R2R) + len(loss_R2R)) * 100

drdwn_maxduration = max(drdwn, key=lambda x: x[0])
drdwn_maxper = max(drdwn, key=lambda x: x[2])
max_win = max(win_streaks , key=lambda x: x[0])
max_loss = max(lose_streaks, key=lambda x: x[0])

avg_drdwn_per = returnavgofcol(2, drdwn)
avg_drdwn_duration_trades = returnavgofcol(0, drdwn)
avg_drdwn_duration_days = returnavgofcol(1, drdwn)
avg_win_streak = returnavgofcol(0, win_streaks)
avg_lose_streak = returnavgofcol(0, lose_streaks)
median_drdwn_per = returnmedianofcol(2, drdwn)
median_drdwn_duration_trades = returnmedianofcol(0, drdwn)
median_drdwn_duration_days = returnmedianofcol(1, drdwn)
median_win_streak = returnmedianofcol(0, win_streaks)
median_lose_streak = returnmedianofcol(0, lose_streaks)


output = open('output.txt', 'w') 

print('\n\n-----------------------------', file = output)
print(f'Starting Capital was {starting_capital}.\nMax equity high was at {equity_high} & max equity low was at {max_equity_low}\nFinal capital was {capital}', file = output)
print(f'Total return at end of backtest = {(capital - starting_capital)/starting_capital * 100}%', file = output)
print('-----------------------------', file = output)
print(f'No of drawdowns is {len(drdwn)}', file = output)
print(f'Average drawdowns was at {avg_drdwn_per}. Median was at {median_drdwn_per}', file = output)
print(f'Drawdowns lasted for an average of {avg_drdwn_duration_trades} trades. Median was at {median_drdwn_duration_trades} trades', file = output)
print(f'Drawdowns lasted for an average of {avg_drdwn_duration_days} days. Median was at {median_drdwn_duration_days} days', file = output)
print('-----------------------------', file = output)
print(f'Max drawdown was at {drdwn_maxper[2]}%.\nStarted from {drdwn_maxper[3]}. Low at {drdwn_maxper[4]}', file = output)
print('-----------------------------', file = output)
print(f'Maximum drawdown duration consisted of {drdwn_maxduration[0]} trades over {drdwn_maxduration[1]} days.\nStarted from {drdwn_maxduration[3]}. Ended at {drdwn_maxduration[5]}', file = output)
print('-----------------------------', file = output)
print(f'Longest winning streak was at {max_win[0]} from {max_win[2]} to {max_win[3]}. Return of {max_win[1]}%', file = output)
print(f'Longest losing streak was at {max_loss[0]} from {max_loss[2]} to {max_loss[3]}. Return of -{max_loss[1]}%', file = output)
print('-----------------------------', file = output)
print(f'The average winstreak was at {avg_win_streak} trades. Median was at {median_win_streak} trades', file = output)
print(f'The average losestreak was at {avg_lose_streak} trades. Median was at {median_lose_streak} trades', file = output)
print('-----------------------------', file = output)
print(f'Win Rate is {winrate_per}% with an average reward of {statistics.mean(win_R2R)}R. Median reward is {statistics.median(win_R2R)}', file = output)
print(f'Loss Rate is {lossrate_per}% with an average loss of {statistics.mean(loss_R2R)}R. Median loss is {statistics.median(loss_R2R)}', file = output)
print('-----------------------------', file = output)
print(f'No of trades not taken is {trades_not_taken}', file = output)
print('-----------------------------\n\n', file = output)

output.close()
