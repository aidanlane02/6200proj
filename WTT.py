#calculate the water transit time from lewiston ID (next dam upstream) to ice harbor in hours

def WTT(breachTouple):
    time = 0
    if breachTouple[0] == False:
        time += 40/0.7
    else:
        time += 40/7
    if breachTouple[1] == False:
        time += 37/0.7
    else:
        time += 37/7
    if breachTouple[2] == False:
        time += 28/0.7
    else:
        time += 28/7
    if breachTouple[3] == False:
        time += 32/0.7
    else:
        time += 32/7
    return time