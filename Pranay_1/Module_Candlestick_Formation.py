def getnewhigh(high,candle_high):
    if high == 0:
        return candle_high
    elif candle_high > high:
        return candle_high
    else:
        return high

def getnewlow(low,candle_low):
    if low == 0:
        return candle_low
    elif candle_low < low:
        return candle_low
    else:
        return low

def isforming5mincandle(timestr):
    m=int(timestr[3:5])
    if ((m+1)%5 == 0):
        return 0
    else:
        return 1

def resizecandlesticks(o,h,l,c):
    op = o[-50:]
    hi = h[-50:]
    lo = l[-50:]
    cl = c[-50:]
    return[op,hi,lo,cl]

def formcandle(mychart, current_row):
    o = mychart[0]
    h = mychart[1]
    l = mychart[2]
    c = mychart[3]
    candle_timestamp = mychart[4]
    candle_high = mychart[5]
    candle_low = mychart[6]
    
    candle_high = getnewhigh(candle_high,float(current_row[2]))
    candle_low = getnewlow(candle_low,float(current_row[3]))

    #once highs and lows before 10 are formed, 5 minute candles need to be made
    if ( isforming5mincandle(current_row[0][11:20]) ): #returns 1 if 0,1,2,3. returns 0 if 4
        candletime = current_row[0][11:20]
        if (int(candletime[3:5])%5==0):
            candle_open = float(current_row[1])
            candle_timestamp.append(current_row[0])
            o.append(candle_open)
    else:
        candle_close = float(current_row[4])
        l.append(candle_low)
        h.append(candle_high)
        c.append(candle_close)
        #print(f'Candle OHLC is {o[-1]}, {h[-1]}, {l[-1]}, {c[-1]}')
        #Reset for next candle
        candle_open = 0
        candle_close = 0
        candle_high = 0
        candle_low = 0
                
        if len(o) >= 100:
            #print('Candles Resized')
            newsize = resizecandlesticks(o, h, l, c)
            o = newsize[0]
            h = newsize[1]
            l = newsize[2]
            c = newsize[3]
        #End code for candle formation
    mychart = [o,h,l,c, candle_timestamp, candle_high, candle_low]
    return mychart
