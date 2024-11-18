#calculate the water transit time from lewiston ID (next dam upstream) to ice harbor in hours

def WTT(breachTouple, spillPerTouple):
    WTTdays = []
    for d in range(len(spillPerTouple[0])):
        time = 0
        if breachTouple[0] == False:
            time += 40/(7*spillPerTouple[0][d]/100+0.7*(1-spillPerTouple[0][d]/100))
        else:
            time += 40/7
        if breachTouple[1] == False:
            time += 37/(7*spillPerTouple[1][d]/100+0.7*(1-spillPerTouple[1][d]/100))
        else:
            time += 37/7
        if breachTouple[2] == False:
            time += 28/(7*spillPerTouple[2][d]/100+0.7*(1-spillPerTouple[2][d]/100))
        else:
            time += 28/7
        if breachTouple[3] == False:
            time += 32/(7*spillPerTouple[3][d]/100+0.7*(1-spillPerTouple[3][d]/100))
        else:
            time += 32/7
        WTTdays.append(time/24)
    return WTTdays