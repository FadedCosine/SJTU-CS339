import xml.etree.ElementTree as ET
import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st

path1 = "../SJTU-WiFi-clients-data"
minDuration = 10 #表示视为有效连接是，要求持续连接的最小值， 取值由draw_vaild_connect 函数所画的图像确定。
#因为有一些日期的连接信息不完整，经过不同日期的数据对比和完整性分析，我们选择了工作日和周末的日期如下
weekday = ['2018-05-14', '2018-05-15', '2018-05-16', '2018-05-17', '2018-05-18']
weekend = ['2018-05-12', '2018-05-13']
#Put all the path in the [pathlist] form given path
def find_all_file_in_the_folder(path):
    pathlist=[]
    for i in os.listdir(path):
        pathlist.append(i)
    return pathlist
#

def buildDic_time_AP_users(path, filelist, minDuration):
    time_AP_users = {}
    for filename in filelist:
        dom = ET.parse(os.path.join(path,filename))
        root = dom.getroot()
        if len(root) == 0 or root.find('client') == None:
            continue
        rootChildList = root[0]
        username = ""
        # since some data may lose the username, however, for a same file, the username should be the same, so we simply user the same username
        for child in rootChildList.findall('association'):
            if child.find('username') != None:
                username = child.find('username').text
                break
        for child in rootChildList:
            if child.tag == 'association':
                connect_time = child.find('connect_time').text
                disconect_time = child.find('disconnect_time').text
                connect_time_list = connect_time.split('T')
                disconnect_time_list = disconect_time.split('T')
                date = connect_time_list[0]
                connect = connect_time_list[1]
                connect_minute_index = int(connect.split(':')[0]) * 60 + int(connect.split(':')[1])
                disconnect = disconnect_time_list[1]
                disconnect_minute_index = int(disconnect.split(':')[0]) * 60 + int(disconnect.split(':')[1])
                # if an association duration time is less than minDuration, leave out this association
                if disconnect_minute_index - connect_minute_index < minDuration:
                    continue

                if date not in time_AP_users.keys():
                    time_AP_users[date] = []
                    for j in range(24 * 60):
                        time_AP_users[date].append({})# use -1 to denote in this time, there is nobody in any AP

                ap = child.find('ap').text
                for minute_i in range(connect_minute_index,disconnect_minute_index):
                    if ap not in time_AP_users[date][minute_i].keys():
                        time_AP_users[date][minute_i][ap] = []
                        time_AP_users[date][minute_i][ap].append(username)
                    else:
                        if username not in time_AP_users[date][minute_i][ap]:
                            time_AP_users[date][connect_minute_index][ap].append(username)
                # ap_userlist = time_AP_users[date][connect_minute_index]
                # if ap not in ap_userlist.keys():
                #     time_AP_users[date][connect_minute_index][ap] = []
                #     time_AP_users[date][connect_minute_index][ap].append(username)
                # else:
                #     if username not in ap_userlist[ap]:
                #         time_AP_users[date][connect_minute_index][ap].append(username)

    f = open("time_AP_users.pk", 'wb')
    pickle.dump(time_AP_users, f)
    f.close()
    return time_AP_users

def buildDic_AP_time_users(path, filelist, minDuration):
    AP_time_users = {}
    for filename in filelist:
        dom = ET.parse(os.path.join(path,filename))
        root = dom.getroot()
        if len(root) == 0 or root.find('client') == None:
            continue
        rootChildList = root[0]
        username = ""
        # since some data may lose the username, however, for a same file, the username should be the same, so we simply user the same username
        for child in rootChildList.findall('association'):
            if child.find('username') != None:
                username = child.find('username').text
                break
        for child in rootChildList:
            if child.tag == 'association':
                connect_time = child.find('connect_time').text
                disconect_time = child.find('disconnect_time').text
                connect_time_list = connect_time.split('T')
                disconnect_time_list = disconect_time.split('T')
                date = connect_time_list[0]
                ap = child.find('ap').text
                connect = connect_time_list[1]
                connect_minute_index = int(connect.split(':')[0]) * 60 + int(connect.split(':')[1])
                disconnect = disconnect_time_list[1]
                disconnect_minute_index = int(disconnect.split(':')[0]) * 60 + int(disconnect.split(':')[1])
                # if an association duration time is less than minDuration, leave out this association
                if disconnect_minute_index - connect_minute_index < minDuration:
                    continue

                if ap not in AP_time_users.keys():
                    AP_time_users[ap] = {}
                if date not in AP_time_users[ap].keys():
                    AP_time_users[ap][date] = []
                    for j in range(24 * 60):
                        AP_time_users[ap][date].append([])# use -1 to denote in this time, there is nobody in any AP

                for minute_i in range(connect_minute_index,disconnect_minute_index):
                    AP_time_users[ap][date][minute_i].append(username)

    f = open("AP_time_users.pk", 'wb')
    pickle.dump(AP_time_users, f)
    f.close()
    return AP_time_users

def buildDic_users_time_AP(path, filelist,minDuration):
    users_time_AP = {}
    ap_id_name_dict = {}
    for filename in filelist:
        dom = ET.parse(os.path.join(path, filename))
        root = dom.getroot()
        #print('root.tag = ' + root.tag)
        if len(root) == 0  or root.find('client') == None:
            continue
        username = ""
        client = root[0]
        for child in client.findall('association'):
            if child.find('username') != None:
                username = child.find('username').text
                break
        if username not in users_time_AP.keys():
            users_time_AP[username] = {}
        for child in client.findall('association'):
            connect_time = child.find('connect_time').text
            disconect_time = child.find('disconnect_time').text
            ap_id = child.find('ap').get('id')
            ap_id_name_dict[ap_id] = child.find('ap').text
            connect_time_list = connect_time.split('T')
            disconnect_time_list = disconect_time.split('T')

            connect = connect_time_list[1]
            connect_minute_index = int(connect.split(':')[0]) * 60 + int(connect.split(':')[1])
            #connect_minute = connect[:-3]
            disconnect = disconnect_time_list[1]
            # disconnect_minute = disconnect[:-3]
            disconnect_minute_index = int(disconnect.split(':')[0]) * 60 + int(disconnect.split(':')[1])
            # if an association duration time is less than minDuration, leave out this association
            if disconnect_minute_index - connect_minute_index < minDuration:
                continue
            if connect_time_list[0] not in users_time_AP[username].keys():
                users_time_AP[username][connect_time_list[0]] = [[] for i in range(24 * 60) ]
            for minute_i in range(connect_minute_index,disconnect_minute_index):
                users_time_AP[username][connect_time_list[0]][minute_i].append(ap_id)

    #
    f = open("users_time_AP.pk", 'wb')
    pickle.dump(users_time_AP, f)
    f.close()

def visualization_of_top10_AP_time(filename,write_weekday_filename, write_weekend_filename, minDuration):
    if not os.path.exists(filename):
        print("Writting file!")
        filelst = find_all_file_in_the_folder(path1)
        time_AP_users = buildDic_time_AP_users(path1, filelst, minDuration)
        f = open(filename, 'wb')
        pickle.dump(time_AP_users, f)
        f.close()
    else:
        print("Openning file!")
        f = open(filename, 'rb')
        time_AP_users = pickle.load(f)
        f.close()
    weekday_time = [8 * 60, 21 * 60]
    weekend_time = [9 * 60, 22 * 60]

    #ap: date : number of users
    weekday_time_AP_usernumber = [{} for i in range(weekday_time[0],weekday_time[1])]
    j = 0
    for date in weekday:
        if date not in time_AP_users.keys():
            continue
        j += 1
        for i in range(weekday_time[1] - weekday_time[0]):
            for ap in time_AP_users[date][weekday_time[0] + i].keys():
                if ap not in weekday_time_AP_usernumber[i].keys():
                    weekday_time_AP_usernumber[i][ap] = len(time_AP_users[date][weekday_time[0] + i][ap])
                else:
                    weekday_time_AP_usernumber[i][ap] += len(time_AP_users[date][weekday_time[0] + i][ap])

    for minute in range(len(weekday_time_AP_usernumber)):
        for ap in weekday_time_AP_usernumber[minute].keys():
            weekday_time_AP_usernumber[minute][ap] /= j

    weekend_time_AP_usernumber = [{} for i in range(weekend_time[0], weekend_time[1])]
    j = 0
    for date in weekend:
        if date not in time_AP_users.keys():
            continue
        j += 1
        for i in range(weekend_time[1] - weekend_time[0]):
            for ap in time_AP_users[date][weekend_time[0] + i].keys():
                if ap not in weekend_time_AP_usernumber[i].keys():
                    weekend_time_AP_usernumber[i][ap] = len(time_AP_users[date][weekend_time[0] + i][ap])
                else:
                    weekend_time_AP_usernumber[i][ap] += len(time_AP_users[date][weekend_time[0] + i][ap])

    for minute in range(len(weekend_time_AP_usernumber)):
        for ap in weekend_time_AP_usernumber[minute].keys():
            weekend_time_AP_usernumber[minute][ap] /= j

    f = open(write_weekday_filename, 'w')
    f.write('name,type,value,date\n')
    for minute_index in range(len(weekday_time_AP_usernumber)):
        top10_ap = sorted(weekday_time_AP_usernumber[minute_index].items(), key=lambda x: x[1], reverse=True)[:10]
        hour = int((weekday_time[0] + minute_index) / 60)
        minute = weekday_time[0] + minute_index - hour * 60
        hour = str(hour)
        minute = str(minute)
        if len(hour) == 1 :
            hour = '0' + hour
        if len(minute) == 1 :
            minute = '0' + minute
        date = hour + ':' + minute
        i = 1
        for ap_usernumber in top10_ap:
            f.write(ap_usernumber[0]+','+ str(i) + ',' + str(ap_usernumber[1]) + ',' + date +'\n')
            i += 1
    f.close()

    f = open(write_weekend_filename, 'w')
    f.write('name,type,value,date\n')
    for minute_index in range(len(weekend_time_AP_usernumber)):
        top10_ap = sorted(weekend_time_AP_usernumber[minute_index].items(), key=lambda x: x[1], reverse=True)[:10]
        hour = int((weekend_time[0] + minute_index) / 60)
        minute = weekend_time[0] + minute_index - hour * 60
        hour = str(hour)
        minute = str(minute)
        if len(hour) == 1:
            hour = '0' + hour
        if len(minute) == 1:
            minute = '0' + minute
        date = hour + ':' + minute
        i = 1
        for ap_usernumber in top10_ap:
            f.write(ap_usernumber[0]+','+ str(i) + ',' + str(ap_usernumber[1])+ ',' + date +'\n')
            i += 1

def draw_vaild_connect(path, filelist):
    vaild_connect_num = [0] * (24 * 60)
    for filename in filelist:
        dom = ET.parse(os.path.join(path,filename))
        root = dom.getroot()
        if len(root) == 0 or root.find('client') == None:
            continue
        rootChildList = root[0]
        username = ""
        # since some data may lose the username, however, for a same file, the username should be the same, so we simply user the same username
        for child in rootChildList.findall('association'):
            if child.find('username') != None:
                username = child.find('username').text
                break
        for child in rootChildList:
            if child.tag == 'association':
                connect_time = child.find('connect_time').text
                disconect_time = child.find('disconnect_time').text
                connect_time_list = connect_time.split('T')
                disconnect_time_list = disconect_time.split('T')

                connect = connect_time_list[1]
                connect_minute_index = int(connect.split(':')[0]) * 60 + int(connect.split(':')[1])
                disconnect = disconnect_time_list[1]
                disconnect_minute_index = int(disconnect.split(':')[0]) * 60 + int(disconnect.split(':')[1])
                duration = disconnect_minute_index - connect_minute_index
                for i in range(duration+1):
                    vaild_connect_num[i] += 1

    plt.plot(range(1,50), vaild_connect_num[1:50])
    plt.ylabel("#valid connection")
    plt.xlabel("minimal duration time")
    plt.show()


def count_association_time(path, filelist):
    duration_list = []
    if not os.path.exists("Association_duration.pk"):
        print("Write:")
        duration_list = [0] * 24 * 60
        for filename in filelist:

            dom = ET.parse(os.path.join(path, filename))
            root = dom.getroot()
            #print('root.tag = ' + root.tag)
            if len(root) == 0  or root.find('client') == None:
                continue
            client = root[0]
            for child in client.findall('association'):
                connect_time = child.find('connect_time').text
                disconect_time = child.find('disconnect_time').text
                connect_time_list = connect_time.split('T')
                disconnect_time_list = disconect_time.split('T')
                connect = connect_time_list[1]
                connect_minute_index = int(connect.split(':')[0]) * 60 + int(connect.split(':')[1])
                disconnect = disconnect_time_list[1]
                disconnect_minute_index = int(disconnect.split(':')[0]) * 60 + int(disconnect.split(':')[1])
                duration = disconnect_minute_index - connect_minute_index
                duration_list[duration] += 1
        f = open("Association_duration.pk", "wb")
        pickle.dump(duration_list, f)
        f.close()
    else:
        print("Read:")
        f = open("Association_duration.pk", 'rb')
        duration_list = pickle.load(f)
        f.close()
    i = len(duration_list)-1
    print(duration_list)
    for i in range(len(duration_list)-1,-1,-1):
        if duration_list[i] != 0:
            print("largest duration: ", i)
            break
    plt.plot(range(len(duration_list[:i+1])), duration_list[:i+1])
    plt.ylabel("number")
    plt.xlabel("Association duration(minute)")
    # plt.xlim((0, 24))
    # my_x_ticks = np.arange(0 , 24, 1)
    # plt.xticks(my_x_ticks)
    plt.title("Association duration statistics" )
    plt.show()


#has something wrong may be, a ap may not be connected by user all the time
def count_AP(filename,minDuration):
    if not os.path.exists(filename):
        filelst = find_all_file_in_the_folder(path1)
        AP_time_users = buildDic_AP_time_users(path1, filelst, minDuration)
        f = open(filename, 'wb')
        pickle.dump(AP_time_users, f)
        f.close()
    else:
        f = open(filename, 'rb')
        AP_time_users = pickle.load(f)
        f.close()

    print("The total number of AP is ",len(AP_time_users))

def find_open_close_class(filename, minDuration, active_hour_weekday, active_hour_weekend, disconnect_threshold_list):
    if not os.path.exists(filename):
        print("Writting file!")
        filelst = find_all_file_in_the_folder(path1)
        users_time_AP = buildDic_users_time_AP(path1, filelst, minDuration)
        f = open(filename, 'wb')
        pickle.dump(users_time_AP, f)
        f.close()
    else:
        print("Openning file!")
        f = open(filename, 'rb')
        users_time_AP = pickle.load(f)
        f.close()
    # for user in users_time_AP.keys():
    #     for date in users_time_AP[user].keys():
    #         for i in users_time_AP[user][date]:
    #             print(i)
    #             return
    weekday = ['2018-05-14', '2018-05-15', '2018-05-16', '2018-05-17', '2018-05-18']
    weekend = ['2018-05-12', '2018-05-13']
    # for user in users_time_AP.key():
    weekday_close_class = []
    weekend_close_class = []
    avg_weekday_close_class_number = []
    avg_weekend_close_class_number = []
    for disconnect_threshold in disconnect_threshold_list:
        weekday_close_class.append({})
        for user in users_time_AP.keys():
            for weekday_date in weekday:
                if weekday_date not in users_time_AP[user].keys():
                    continue
                start_minute = active_hour_weekday[0] * 60
                end_minute = active_hour_weekday[1] * 60
                isActive = 1
                for minute in range(start_minute,end_minute, int(disconnect_threshold/2)):
                    has_connected_AP = 0
                    for i in range(int(disconnect_threshold/2)):
                        if users_time_AP[user][weekday_date][minute+i] != []:
                            has_connected_AP = 1
                    if not has_connected_AP:
                        isActive = 0
                        break
                if isActive:
                    if weekday_date not in weekday_close_class[-1].keys():
                        weekday_close_class[-1][weekday_date] = []
                    weekday_close_class[-1][weekday_date].append(user)

        weekday_sum = 0
        for weekday_date in weekday:
            # print(weekday_date + ' '+ str(len(weekday_close_class[-1][weekday_date])))
            weekday_sum += len(weekday_close_class[-1][weekday_date])
        avg_weekday_close_class_number.append(weekday_sum/5)

        weekend_close_class.append({})
        for user in users_time_AP.keys():
            for weekend_date in weekend:
                if weekend_date not in users_time_AP[user].keys():
                    continue
                start_minute = active_hour_weekend[0] * 60
                end_minute = active_hour_weekend[1] * 60
                isActive = 1
                for minute in range(start_minute, end_minute, int(disconnect_threshold / 2)):
                    has_connected_AP = 0
                    for i in range(int(disconnect_threshold / 2)):
                        if users_time_AP[user][weekend_date][minute + i] != []:
                            has_connected_AP = 1
                    if not has_connected_AP:
                        isActive = 0
                        break
                if isActive:
                    if weekend_date not in weekend_close_class[-1].keys():
                        weekend_close_class[-1][weekend_date] = []
                    weekend_close_class[-1][weekend_date].append(user)

        weekend_sum = 0
        for weekend_date in weekend:
            # print(weekend_date + ' ' + str(len(weekend_close_class[-1][weekend_date])))
            weekend_sum += len(weekend_close_class[-1][weekend_date])
        avg_weekend_close_class_number.append(weekend_sum / 2)
    f = open("weekday_close_class.pk",'wb')
    pickle.dump(weekday_close_class,f)
    f.close()

    f = open("weekend_close_class.pk", 'wb')
    pickle.dump(weekend_close_class, f)
    f.close()
    print("avg_weekday_close_class_number: ",avg_weekday_close_class_number)
    print("avg_weekend_close_class_number: ", avg_weekend_close_class_number)
    plt.plot(range(len(avg_weekday_close_class_number)), avg_weekday_close_class_number)
    plt.ylabel("close class number")
    plt.xlabel("disconnect threshold (minute)")
    plt.title("The change of weekday's average close class number against disconnect threshold" )
    plt.show()
    plt.plot(range(len(avg_weekend_close_class_number)), avg_weekend_close_class_number)
    plt.ylabel("close class number")
    plt.xlabel("disconnect threshold (minute)")
    plt.title("The change of weekend's average close class number against disconnect threshold" )
    plt.show()
    """user_moreAP_atOnetime = {}
    for user in users_time_AP.keys():
        for date in users_time_AP[user].keys():
            for i in range(len(users_time_AP[user][date])):
                if users_time_AP[user][date][i] != []:
                    if len(users_time_AP[user][date][i]) != 1:
                        minute = str(int(i/60)) + ':'+ str(i-int(i/60)*60)
                        user_moreAP_atOnetime[user] = [date,minute,users_time_AP[user][date][i]]
                        break
            break
    user_fileList = {}
    for file in filelist:
        dom = ET.parse(os.path.join(path, file))
        root = dom.getroot()
        # print('root.tag = ' + root.tag)
        if len(root) == 0 or root.find('client') == None:
            continue
        username = ""
        client = root[0]
        for child in client.findall('association'):
            if child.find('username') != None:
                username = child.find('username').text
                break
        if username not in user_fileList.keys():
            user_fileList[username] = []
        user_fileList[username].append(file)
        if username in user_moreAP_atOnetime.keys():
            print(file)
            print(user_moreAP_atOnetime[username])
    print("Username_Filelist")
    for username in user_fileList.keys():
        print(username)
        print(user_fileList[username])"""
# 以上注释的内容是用于调试
# 经过调试，发现在所给数据中，一个用户一分钟内可能出现在两个或以上的AP的用户列表中

def draw_avg_close_class():
    avg_weekday_close_class_number = [56.6, 85.6, 107.2, 130.8, 140.2, 182.4, 199.0, 241.8, 278.0, 341.2, 362.8, 490.6, 551.4, 515.6, 642.8, 732.4,
     693.0, 883.4, 835.2, 1075.2, 1055.0, 975.2, 1307.2, 1264.8]
    avg_weekend_close_class_number = [51.5, 72.5, 88.0, 102.0, 103.0, 128.0, 133.5, 152.0, 161.0, 182.5, 174.5, 230.5, 253.5, 213.0, 248.0, 298.5, 266.5, 334.5, 300.5, 395.5, 375.5, 348.0, 467.0, 460.5]
    plt.plot([ i*10 for i in range(1,len(avg_weekday_close_class_number)+1)], avg_weekday_close_class_number)
    plt.ylabel("close class number")
    plt.xlabel("disconnect threshold (minute)")
    plt.title("Weekday's average close class number against disconnect threshold" )
    plt.show()

    plt.plot([ i*10 for i in range(1,len(avg_weekend_close_class_number)+1)], avg_weekend_close_class_number)
    plt.ylabel("close class number")
    plt.xlabel("disconnect threshold (minute)")
    plt.title("Weekend's average close class number against disconnect threshold" )
    plt.show()

#since at first we don't know how to calculate the arrival rate

# understanding one:
# maintain a user list of all the AP's, arrival rate is the new-come users divided by unit time
def arrival_rate_varyingtime(filename, minDuration):
    if not os.path.exists(filename):
        print("Writting file!")
        filelst = find_all_file_in_the_folder(path1)
        time_AP_users = buildDic_time_AP_users(path1, filelst, minDuration)

        f = open(filename, 'wb')
        pickle.dump(time_AP_users, f)
        f.close()
    else:
        print("Openning file!")
        f = open(filename, 'rb')
        time_AP_users = pickle.load(f)
        f.close()
    time_users = {}
    for date in time_AP_users.keys():
        time_users[date] = []
        # time_users[data] : [ minute1_all_user_set, minute2_all_user_set, ... ]

        for minuteDic in range(len(time_AP_users[date])):
            UserSet = set()
            for AP in time_AP_users[date][minuteDic].keys():
                UserSet.update(time_AP_users[date][minuteDic][AP])

            time_users[date].append(UserSet)
    arrival_rate = {}
    for date in time_users.keys():
        print("Date is :", date)
        arrival_rate[date] = []
        for i in range(len(time_users[date])-1):
            arrival_rate[date].append(len(time_users[date][i+1]-time_users[date][i]))
        print(arrival_rate[date])
    f = open("arrival_rate.pk", 'wb')
    pickle.dump(arrival_rate, f)
    f.close()
    return arrival_rate

# arrival rate = ( number of new-comer during 10 minutes) / 10
def draw_arrival_rate(arrival_rate):
    # f = open("arrival_rate.pk", 'rb')
    # arrival_rate = pickle.load(f)
    # f.close()
    date_list = []
    for date in arrival_rate.keys():
        date_list.append(date)
    date_list.sort()
    print(date_list)
    weekday = ['2018-05-14', '2018-05-15', '2018-05-16', '2018-05-17', '2018-05-18']
    weekend = ['2018-05-12', '2018-05-13']
    arrival_rate_weekday_per_10_min = [0] * (int(len(arrival_rate["2018-05-14"])/10)+1)
    for date in weekday:
        new_comer_per_10_min = [sum(arrival_rate[date][i*10:(i+1)*10]) for i in range(int(len(arrival_rate[date])/10))]
        for i in range(len(new_comer_per_10_min[:-1])):
            arrival_rate_weekday_per_10_min[i] += new_comer_per_10_min[i]/10
        arrival_rate_weekday_per_10_min[-1] += (new_comer_per_10_min[-1]/(len(arrival_rate[date])- int(len(arrival_rate[date])/10) * 10))
    arrival_rate_weekday_per_10_min = [i/len(weekday) for i in arrival_rate_weekday_per_10_min]

    plt.plot([ i/6 for i in range(len(arrival_rate_weekday_per_10_min))], arrival_rate_weekday_per_10_min)
    plt.ylabel("arrival rate (#users/min)")
    plt.xlabel("time (hour)")
    plt.xlim((0, 24))
    my_x_ticks = np.arange(0 , 24, 1)
    plt.xticks(my_x_ticks)
    plt.title("Average user arrival rate in weekday" )
    plt.show()

    arrival_rate_weekend_per_10_min = [0] * (int(len(arrival_rate["2018-05-12"]) / 10) + 1)
    for date in weekend:
        new_comer_per_10_min = [sum(arrival_rate[date][i * 10:(i + 1) * 10]) for i in
                                range(int(len(arrival_rate[date]) / 10))]
        for i in range(len(new_comer_per_10_min[:-1])):
            arrival_rate_weekend_per_10_min[i] += new_comer_per_10_min[i] / 10
        arrival_rate_weekend_per_10_min[-1] += (
                    new_comer_per_10_min[-1] / (len(arrival_rate[date]) - int(len(arrival_rate[date]) / 10) * 10))
    arrival_rate_weekend_per_10_min = [i / len(weekend) for i in arrival_rate_weekend_per_10_min]
    plt.plot([ i/6 for i in range(len(arrival_rate_weekend_per_10_min))], arrival_rate_weekend_per_10_min)
    plt.ylabel("arrival rate (#users/min)")
    plt.xlabel("time (hour)")
    plt.xlim((0, 24))
    my_x_ticks = np.arange(0 , 24, 1)
    plt.xticks(my_x_ticks)
    plt.title("Average user arrival rate in weekend" )
    plt.show()
    for date in date_list:
            #the total len of arrival_rate[date] is 1439, so that we can write the code as follow
            new_comer_per_10_min = [sum(arrival_rate[date][i*10:(i+1)*10]) for i in range(int(len(arrival_rate[date])/10))]
            arrival_rate_per_10_min = [ i/10 for i in new_comer_per_10_min[:-1]]
            arrival_rate_per_10_min.append(new_comer_per_10_min[-1]/(len(arrival_rate[date])- int(len(arrival_rate[date])/10) * 10))
            print(arrival_rate_per_10_min)
            plt.plot([ i/6 for i in range(len(arrival_rate_per_10_min))], arrival_rate_per_10_min)
            plt.ylabel("arrival rate (#users/min)")
            plt.xlabel("time (hour)")
            plt.xlim((0, 24))
            my_x_ticks = np.arange(0 , 24, 1)
            plt.xticks(my_x_ticks)
            plt.title("Average user arrival rate in " + date)
            plt.show()

def calculate_AP_residence_time(path, filelist, minDuration):
    AP_date_residence = {}
    for filename in filelist:
        dom = ET.parse(os.path.join(path,filename))
        root = dom.getroot()
        if len(root) == 0 or root.find('client') == None:
            continue
        rootChildList = root[0]
        username = ""
        # since some data may lose the username, however, for a same file, the username should be the same, so we simply user the same username
        for child in rootChildList.findall('association'):
            if child.find('username') != None:
                username = child.find('username').text
                break
        for child in rootChildList:
            if child.tag == 'association':
                connect_time = child.find('connect_time').text
                disconect_time = child.find('disconnect_time').text
                connect_time_list = connect_time.split('T')
                disconnect_time_list = disconect_time.split('T')
                date = connect_time_list[0]
                ap = child.find('ap').text
                connect = connect_time_list[1]
                connect_minute_index = int(connect.split(':')[0]) * 60 + int(connect.split(':')[1])
                disconnect = disconnect_time_list[1]
                disconnect_minute_index = int(disconnect.split(':')[0]) * 60 + int(disconnect.split(':')[1])
                duration = disconnect_minute_index - connect_minute_index
                if duration < minDuration:
                    continue
                if ap not in AP_date_residence.keys():
                    AP_date_residence[ap] = {}
                if date not in AP_date_residence[ap].keys():
                    AP_date_residence[ap][date] = []


                AP_date_residence[ap][date].append(duration)

    f = open("AP_date_residence.pk", 'wb')
    pickle.dump(AP_date_residence, f)
    f.close()
    weekday = ['2018-05-14', '2018-05-15', '2018-05-16', '2018-05-17', '2018-05-18']
    weekend = ['2018-05-12', '2018-05-13']
    ap_weekday_residence_time = {}
    for ap in AP_date_residence.keys():
        sum_residence_time = 0
        i = 0
        for date in weekday:
            if date not in AP_date_residence[ap].keys():
                continue
            i += 1
            sum_residence_time += (sum(AP_date_residence[ap][date])/len(AP_date_residence[ap][date]))
        if i == 0 :
            continue
        ap_weekday_residence_time[ap] = sum_residence_time / i
    ap_weekend_residence_time = {}
    for ap in AP_date_residence.keys():
        sum_residence_time = 0
        i = 0
        for date in weekend:
            if date not in AP_date_residence[ap].keys():
                continue
            i += 1
            sum_residence_time += (sum(AP_date_residence[ap][date]) / len(AP_date_residence[ap][date]))
        if i == 0 :
            continue
        ap_weekend_residence_time[ap] = sum_residence_time / i
    f = open("AP_weekday_residence_time.pk", 'wb')
    pickle.dump(ap_weekday_residence_time, f)
    f.close()
    f = open("AP_weekend_residence_time.pk", 'wb')
    pickle.dump(ap_weekend_residence_time, f)
    f.close()
    i = 0
    for ap in ap_weekday_residence_time:
        if i < 10:
            i += 1
            print("AP is ", ap)
            print("Weekday residence time is ", ap_weekday_residence_time[ap])
        else:
            break
    i = 0
    for ap in ap_weekend_residence_time:
        if i < 10:
            i += 1
            print("AP is ", ap)
            print("Weekend residence time is ", ap_weekend_residence_time[ap])
        else:
            break
    # 以下注释的代码用于调试， 输出其中一个AP在周末和工作日的active hour中的平均驻留时间
    #print(" The expected user residence time of MH-GCLXSYZX-9#-OUT in weekday is ", ap_weekday_residence_time["MH-GCLXSYZX-9#-OUT"] )
    #print(" The expected user residence time of MH-GCLXSYZX-9#-OUT in weekend is ",
          ap_weekend_residence_time["MH-GCLXSYZX-9#-OUT"])
    return ap_weekday_residence_time,ap_weekend_residence_time

def calculate_AP_arrival_rate(filename,minDuration):
    if not os.path.exists(filename):
        print("Writting file!")
        filelst = find_all_file_in_the_folder(path1)
        AP_time_users = buildDic_AP_time_users(path1, filelst, minDuration)
        f = open(filename, 'wb')
        pickle.dump(AP_time_users, f)
        f.close()
    else:
        print("Openning file!")
        f = open(filename, 'rb')
        AP_time_users = pickle.load(f)
        f.close()
    weekday_time = [8 * 60, 21 * 60]
    weekend_time = [9 * 60, 22 * 60]

    arrival_rate = {}
    for ap in AP_time_users.keys():
        if ap not in arrival_rate.keys():
            arrival_rate[ap] = {}
        for date in AP_time_users[ap].keys():
            if date in weekday:
                if date not in arrival_rate.keys():
                    arrival_rate[ap][date] = [] # from 8:00 ~ 20:59
                for minute in range(weekday_time[0], weekday_time[1]):
                    UserSet_pre = set()
                    UserSet_pre.update(AP_time_users[ap][date][minute-1])
                    UserSet_now = set()
                    UserSet_now.update(AP_time_users[ap][date][minute])
                    arrival_rate[ap][date].append(len(UserSet_now-UserSet_pre))
            if date in weekend:
                if date not in arrival_rate.keys():
                    arrival_rate[ap][date] = []  # from 8:00 ~ 20:59
                for minute in range(weekend_time[0], weekend_time[1]):
                    UserSet_pre = set()
                    UserSet_pre.update(AP_time_users[ap][date][minute - 1])
                    UserSet_now = set()
                    UserSet_now.update(AP_time_users[ap][date][minute])
                    arrival_rate[ap][date].append(len(UserSet_now - UserSet_pre))
    ap_avg_arrival_rate = {}
    for ap in arrival_rate.keys():
        ap_avg_arrival_rate[ap] = {}
        for date in arrival_rate[ap]:
            ap_avg_arrival_rate[ap][date] = sum(arrival_rate[ap][date]) / len(arrival_rate[ap][date])
    ap_weekday_avg_rate = {}
    max_weekday_rate = 0
    max_weekday_ap = ''
    max_weekend_rate = 0
    max_weekend_ap = ''
    for ap in ap_avg_arrival_rate.keys():
        weekday_sum_rate = 0
        i = 0
        for date in weekday:
            if date not in ap_avg_arrival_rate[ap].keys():
                continue
            i += 1
            weekday_sum_rate += ap_avg_arrival_rate[ap][date]
        if i == 0 :
            continue
        ap_weekday_avg_rate[ap] = weekday_sum_rate / i
        if max_weekday_rate < ap_weekday_avg_rate[ap]:
            max_weekday_rate = ap_weekday_avg_rate[ap]
            max_weekday_ap = ap
    ap_weekend_avg_rate = {}
    for ap in ap_avg_arrival_rate.keys():
        weekend_sum_rate = 0
        i = 0
        for date in weekend:
            if date not in ap_avg_arrival_rate[ap].keys():
                continue
            i += 1
            weekend_sum_rate += ap_avg_arrival_rate[ap][date]
        if i == 0 :
            continue
        ap_weekend_avg_rate[ap] = weekend_sum_rate / i
        if max_weekend_rate < ap_weekend_avg_rate[ap]:
            max_weekend_rate = ap_weekend_avg_rate[ap]
            max_weekend_ap = ap
    f = open("AP_arrival_rate.pk", 'wb')
    pickle.dump(arrival_rate, f)
    f.close()

    f = open("AP_weekday_avg_rate.pk", 'wb')
    pickle.dump(ap_weekday_avg_rate, f)
    f.close()

    f = open("AP_weekend_avg_rate.pk", 'wb')
    pickle.dump(ap_weekend_avg_rate, f)
    f.close()

    i = 0
    for ap in ap_weekday_avg_rate:
        if i < 10:
            i += 1
            print("AP is ", ap)
            print("Weekday average arrival rate is ", ap_weekday_avg_rate[ap])
        else:
            break
    i = 0
    for ap in ap_weekend_avg_rate:
        if i < 10:
            i += 1
            print("AP is ", ap)
            print("Weekend average arrival rate is ", ap_weekend_avg_rate[ap])
        else:
            break

    print("Highest arrival rate in weekday is ", max_weekday_rate)
    print("The AP is ", max_weekday_ap)
    print("Highest arrival rate in weekend is ", max_weekend_rate)
    print("The AP is ", max_weekend_ap)
    return  ap_weekday_avg_rate, ap_weekend_avg_rate

def draw_occupancy_distribution(ap_name,minDuration):
    #ap_weekday_avg_rate, ap_weekend_avg_rate = calculate_AP_arrival_rate("AP_time_users.pk", minDuration)
    f = open("AP_weekday_avg_rate.pk", 'rb')
    ap_weekday_avg_rate = pickle.load(f)
    f.close()
    f = open("AP_weekend_avg_rate.pk", 'rb')
    ap_weekend_avg_rate = pickle.load(f)
    f.close()
    f = open("AP_weekday_residence_time.pk", 'rb')
    ap_weekday_residence_time = pickle.load(f)
    f.close()
    f = open("AP_weekend_residence_time.pk", 'rb')
    ap_weekend_residence_time = pickle.load(f)
    f.close()
    ap_weekday_load = ap_weekday_avg_rate[ap_name] * ap_weekday_residence_time[ap_name]
    ap_weekend_load = ap_weekend_avg_rate[ap_name] * ap_weekend_residence_time[ap_name]
    print("ap_weekday_avg_rate is ", ap_weekday_avg_rate[ap_name])
    print("ap_weekend_avg_rate is ", ap_weekend_avg_rate[ap_name])
    print("ap_weekday_residence_time is ", ap_weekday_residence_time[ap_name])
    print("ap_weekend_residence_time is ", ap_weekend_residence_time[ap_name])
    print("Lambda weekday", ap_weekday_load)
    print("Lambda weekend", ap_weekend_load)

    if not os.path.exists("time_AP_users.pk"):
        print("Writting file!")
        filelst = find_all_file_in_the_folder(path1)
        time_AP_user = buildDic_time_AP_users(path1, filelst, minDuration)
        f = open("time_AP_users.pk", 'wb')
        pickle.dump(time_AP_user, f)
        f.close()
    else:
        print("Openning file!")
        f = open("time_AP_users.pk", 'rb')
        time_AP_user = pickle.load(f)
        f.close()
    weekday_time = [8 * 60, 21 * 60]
    weekend_time = [9 * 60, 22 * 60]
    weekday_ap_usernumber = [0] * 10041
    for date in weekday:
        if date not in time_AP_user.keys():
            continue
        for minute in range(weekday_time[0],weekday_time[1],minDuration):
            user_List = set()
            # if ap_name not in time_AP_user[date][minute].keys():
            #     continue
            # user_List.update(time_AP_user[date][minute][ap_name])
            for i in range(minDuration):
                if ap_name not in time_AP_user[date][minute + i].keys():
                    continue
                user_List.update(time_AP_user[date][minute + i][ap_name])
            user_number = len(user_List)
            weekday_ap_usernumber[user_number] += 1
    weekend_ap_usernumber = [0] * 10041
    for date in weekend:
        if date not in time_AP_user.keys():
            continue
        for minute in range(weekend_time[0], weekend_time[1],minDuration):
            user_List = set()
            # if ap_name not in time_AP_user[date][minute].keys():
            #     continue
            # user_List.update(time_AP_user[date][minute][ap_name])
            for i in range(minDuration):
                if ap_name not in time_AP_user[date][minute+i].keys():
                    continue
                user_List.update(time_AP_user[date][minute+i][ap_name])
            user_number = len(user_List)
            weekend_ap_usernumber[user_number] += 1
    print(weekday_ap_usernumber)
    print(weekend_ap_usernumber)
    weekday_pdf = [i / sum(weekday_ap_usernumber) for i in weekday_ap_usernumber]
    weekend_pdf = [i / sum(weekend_ap_usernumber) for i in weekend_ap_usernumber]

    x = np.arange(0,15)
    y1 = st.poisson.pmf(x, ap_weekday_load)
    plt.plot(x, y1,label = "model", color='red')
    plt.ylabel("pdf")
    plt.xlabel("#users")
    plt.title("Occupancy distribution of " + ap_name + " in weekday")

    plt.plot(x, weekday_pdf[:15],label = "real trace", color='blue')
    plt.title("Occupancy distribution of " + ap_name + " in weekday")
    plt.legend()
    plt.show()

    y2 = st.poisson.pmf(x, ap_weekend_load)
    plt.plot(x, y2,label = "model", color='red')
    plt.ylabel("pdf")
    plt.xlabel("#users")
    plt.title("Occupancy distribution of " + ap_name + " in weekend")

    plt.plot(x, weekend_pdf[:15],label = "real trace", color='blue')
    plt.ylabel("pdf")
    plt.xlabel("#users")
    plt.title("Occupancy distribution of " + ap_name + " in weekend")
    plt.legend()
    plt.show()


filelst = find_all_file_in_the_folder(path1)
count_association_time(path1, filelst) #以一分钟为单位，计算所有连接的连接时间的发布
count_AP("AP_time_users.pk",minDuration) #计算AP的总数量
draw_vaild_connect(path1, filelst) #画出 有效连接数量随最短持续连接时间阈值 的关系图， 用于确定参数 minDuration的取值
minDuration = 10
buildDic_users_time_AP(path1, filelst, minDuration) # 建立 users_time_AP的嵌套字典，用于维护每个用户每一分钟所连接的AP
buildDic_time_AP_users(path1, filelst, minDuration) #建立time_AP_users的嵌套字典，用于维护每一分钟每个AP下连接着的用户列表
buildDic_AP_time_users(path1, filelst, minDuration) #建立AP_time_users的嵌套字典，用于维护每个AP，以一分钟为单位时间，每个时间下连接着的用户列表
arrival_rate = arrival_rate_varyingtime("time_AP_users.pk") #计算出 工作日和周末 每一分钟的平均到达率
draw_arrival_rate(arrival_rate) #画出 到达率的图像 ，用于确定工作日和周末active hour 的取值
active_hour_weekday = [8, 21]
active_hour_weekend = [9, 22]
#计算open class 和 close class 的数量，并画出close class用户数量随允许close class断开连接的间隔时间的变化曲线
find_open_close_class("users_time_AP.pk",2, active_hour_weekday, active_hour_weekend,  list(range(10,250,10)))
# draw_avg_close_class() 这一个函数是因为代码在服务器上跑的时候因为服务器上没有装matplotlib，所以在本地另写的画出 close class 用户数量的变化图

#每一个AP 在工作日和周末 一天中在active hour中的平均到达率， 在后续建模分析用到
calculate_AP_arrival_rate("AP_time_users.pk", minDuration)

#每一个AP 在工作日和周末 一天中在active hour中的用户的平均逗留时间， 在后续建模分析用到
calculate_AP_residence_time(path1, filelst, minDuration)
#第一个参数是 需要建模的AP 名称
draw_occupancy_distribution("MH-XXY-1F-102",minDuration)
draw_occupancy_distribution("MH-YX2-4F-2-413",minDuration)

#输出工作日和周末 一天中每一分钟 连接数量最多的前十个校园AP列表到 csv 文件用于制作demo
visualization_of_top10_AP_time("time_AP_users.pk", "SJTU_AP_Weekday.csv", "SJTU_AP_Weekend.csv", minDuration)