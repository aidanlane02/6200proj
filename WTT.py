#calculate the water transit time from lewiston ID (next dam upstream) to ice harbor in hours

def WTT(breachTouple, downTouple):
    WTTdays = []
    for d in range(len(downTouple[0]['Spill Percent (%)'])):
        time = 0
        if breachTouple[0] == False:
            time += 40/(7*downTouple[0]['Spill Percent (%)'][d]/100+0.7*(1-downTouple[0]['Spill Percent (%)'][d]/100))
        else:
            time += 40/7
        if breachTouple[1] == False:
            time += 37/(7*downTouple[1]['Spill Percent (%)'][d]/100+0.7*(1-downTouple[1]['Spill Percent (%)'][d]/100))
        else:
            time += 37/7
        if breachTouple[2] == False:
            time += 28/(7*downTouple[2]['Spill Percent (%)'][d]/100+0.7*(1-downTouple[2]['Spill Percent (%)'][d]/100))
        else:
            time += 28/7
        if breachTouple[3] == False:
            time += 32/(7*downTouple[3]['Spill Percent (%)'][d]/100+0.7*(1-downTouple[3]['Spill Percent (%)'][d]/100))
        else:
            time += 32/7
        WTTdays.append(time/24)
    return WTTdays