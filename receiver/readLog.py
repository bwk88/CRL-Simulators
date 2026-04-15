from email import message
import os
from datetime import datetime

# startTime = "2024-06-28_17-37"
# endTime = "2024-06-28_17-43"

def getLogFiles():
    path = "./logs/"
    logfiles = []
    print('path:', os.listdir(path))
    for fname in os.listdir(path):
        print('fname:', fname)
        if "rcv.log" in fname:
            logfiles.append(fname)
    return logfiles

def str_to_datetime(dtime):
    dateTimeFormat = "%Y-%m-%d_%H-%M"
    return datetime.strptime(dtime, dateTimeFormat)

def str_to_datetimeS(dtime):
    dateTimeFormat = "%Y-%m-%d %H:%M:%S"
    return datetime.strptime(dtime, dateTimeFormat)

def findLogFiles(startTime, endTime):
    logfiles = getLogFiles()
    logsToSearch=[]
    # startTime = str_to_datetime(startTime)
    # endTime = str_to_datetime(endTime)

    if startTime == endTime :
        return logsToSearch
    
    for fileName in logfiles:
        tempList = fileName.split(".")

        # find files in start and end time
        if len(tempList) == 3:
            dtime = str_to_datetime(tempList[2])
            if dtime>=startTime and dtime<endTime:
                logsToSearch.append(fileName)

    if len(logsToSearch) == 0:
        logsToSearch.append('rcv.log')
        return logsToSearch

    # boundary files, one previous and one next file
    first_index = logfiles.index(logsToSearch[0])
    last_index = logfiles.index(logsToSearch[-1])

    # print(logsToSearch[-1])
    # print(first_index, last_index)
    
    if first_index != 0 and last_index == len(logfiles)-1:
        logsToSearch.append(logfiles[first_index-1])
        
    else:
        logsToSearch.append(logfiles[first_index-1])
        logsToSearch.append(logfiles[last_index+1])

    logsToSearch.append('rcv.log') 
    return logsToSearch

def example():
    print('example func of readlog.py')

def get_replay_packets(startTime, endTime):
    logsToSearch = findLogFiles(startTime, endTime)
    # startTime = str_to_datetime(startTime)
    # endTime = str_to_datetime(endTime)
        
    logsToSearch = sorted(logsToSearch)
    # print(logsToSearch)
    messageList = []
        

    for logName in logsToSearch:
        with open("./logs/"+logName, 'r') as logfile:
            for logline in logfile:
                dtime = logline.split(',')[0]
                dtime = str_to_datetimeS(dtime)
                if dtime >= startTime and dtime < endTime:
                    messageList.append(logline)
    print("Message log filtered successfully")

    # with open("filteredLog", 'w') as file:
    #     for mes in messageList:
    #         file.writelines(mes)        
    return messageList 