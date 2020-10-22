import sys
import csv


import Module_Candlestick_Formation as chart
import Module_Pranay_1_Signal as tradesignal
import Module_Pranay_1_TradeManagement as tm

with open('Nifty.csv') as csv_file, open('Nifty_Pranay_1.csv','w', newline='') as result_file:
    
    #Reading from file
    writer = csv.writer(result_file)
    writer.writerow(["Year", "Month", "Day", "Entry", "Entry Time", "Risk", "Exit", "Exit Time", "PnL", "R2R"])
    one_min_csv = csv.reader(csv_file, delimiter=',')
    rows = list(one_min_csv)
    total_dataset = len(rows)
    #total_dataset = 5000
    
    
    #Variables for chartformation
    o = []
    h = []
    l = []
    c = []
    candle_timestamp = []
    candle_high = 0
    candle_low = 0
    mychart = [o,h,l,c,candle_timestamp,candle_high,candle_low]
    
    #variablesforsignal
    prev_close = 0
    
    #Variabls for open position properties
    signal = 0
    pos_open = 0
    trade_open =0
    sl = 0
    risk = 0
    open_pos_prop = [signal,pos_open,trade_open,sl,risk]
        
    #To store finished trades
    closed_trades = []

    #To store all positions (open and close)
    all_positions = [open_pos_prop, closed_trades]
    
    
    #Reading each row
    line_count = 1
    while line_count < total_dataset:
        current_row = rows[line_count]
        
        mychart = chart.formcandle(mychart, current_row)
        if signal == 0:
            open_pos_prop = tradesignal.getsignal(open_pos_prop, mychart, prev_close, current_row)
            signal = open_pos_prop[0]
            all_positions[0] = open_pos_prop
        else:
            all_positions = tm.managetrade(all_positions, mychart, current_row)
            open_pos_prop = all_positions[0]
            signal = open_pos_prop[0]

        
        line_count += 1
        if line_count < total_dataset:
            if rows[line_count][0][0:10] != current_row[0][0:10]:
                #print(f'New day at {rows[line_count][0][0:10]}')
                prev_close = mychart[3][-1]
            
    writer.writerows(all_positions[1])