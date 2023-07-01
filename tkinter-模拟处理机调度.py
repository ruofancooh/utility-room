from tkinter import *
from tkinter.ttk import Treeview
from tkinter.scrolledtext import ScrolledText
import json
import copy


def debug():
    #控制台输出信息
    print(data.time)

    print(f'datalist[{data.data_index}]')
    for pro in data.datalist[data.data_index]:
        print(f'{pro[0]} {pro[1]} {pro[2]}')

    print('processlist')
    for pro in data.processlist:
        print(f'{pro[0]} {pro[1]} {pro[2]} {pro[3]} {pro[4]} {pro[5]}')

    print('readylist')
    for pro in data.readylist:
        print(f'{pro.name} {pro.arrival_time} {pro.remaining_execution_time}')

    print('not_arrive')
    for pro in data.not_arrive:
        print(f'{pro.name} {pro.arrival_time} {pro.remaining_execution_time}')

    print('running')
    for pro in data.running:
        print(f'{pro.name} {pro.arrival_time} {pro.remaining_execution_time}')

    print('------')


#定义进程类
class Process:
    def __init__(self, name, arrival_time, execution_time):
        self.name = name  #进程名
        self.arrival_time = arrival_time  #到达时间
        self.remaining_execution_time = execution_time  #剩余执行时间


#定义数据类
class Data:
    def __init__(self):
        self.datalist = []  #保存所有测试数据的列表，点击‘切换下一组’时从这里读取
        self.processlist = []  #保存当前这一组测试数据的列表，点击‘下一步’时更新表格从这里读取
        self.data_index = 0  #当前的测试数据索引
        self.not_arrive = []  #当前未到达的进程列表
        self.readylist = []  #就绪队列
        self.running = []  #正在运行的进程
        self.time = 0  #当前时间
        with open('data.json', 'r') as f:
            '''
            data.json like:
            [
                [
                    ["p1", 0, 7],
                    ["p2", 2, 4],
                    ["p3", 4, 1],
                    ["p4", 5, 4]
                ],
                [
                    ["p1", 3, 7],
                    ["p2", 4, 6],
                    ["p3", 5, 5],
                    ["p4", 6, 4],
                    ["p5", 7, 3]
                ],
                [
                    ["p1", 3, 5],
                    ["pa", 4, 5],
                    ["p2", 0, 1],
                    ["pb", 3, 1]
                ],
                [
                    ["p1", 0, 1]
                ]
            ]
            从文件中读取几组测试数据，保存到datalist中
            datalist的每一项是一组测试数据，每一项类似
            [
                [进程名，到达时间，剩余执行时间]，
                [进程名，到达时间，剩余执行时间]，
                [进程名，到达时间，剩余执行时间]
            ]
            '''
            self.datalist = json.loads(f.read())

    def create_this_list(self):
        #打开子窗口时或点击‘下一组’时调用

        #生成当前这组测试数据的列表processlist
        self.processlist = copy.deepcopy(self.datalist[self.data_index])
        for pro in self.processlist:
            #剩余运行时间
            pro.append(copy.deepcopy(pro[2]))
            #完成时间
            pro.append(0)
            #周转时间
            pro.append(0)
        '''
        processlist:
        [
            [进程名，到达时间，运行时间，剩余运行时间，完成时间，周转时间],
            [进程名，到达时间，运行时间，剩余运行时间，完成时间，周转时间]
        ]
        '''

        #把当前的测试数据转化成进程对象，存放在未到达的进程列表not_arrive中
        self.not_arrive = []
        for pro in self.processlist:
            self.not_arrive.append(Process(pro[0], pro[1], pro[2]))

        #对not_arrive列表按到达时间从晚到早排序
        def take_arrival_time(pro):
            return pro.arrival_time

        self.not_arrive.sort(key=take_arrival_time, reverse=True)

    def clear(self):
        #清空除测试数据列表和索引外的所有数据，关闭子窗口时或点击‘下一组’时调用
        self.processlist = []  #保存当前这一组测试数据的列表
        self.not_arrive = []  #当前未到达的进程列表
        self.readylist = []  #就绪队列
        self.running = []  #正在运行的进程
        self.time = 0  #当前时间

    def calculate_time(self):
        #计算平均周转时间和平均带权周转时间
        avg_turnaround_time = 0  #平均周转时间
        avg_weighted_turnaround_time = 0  #平均带权周转时间
        for pro in self.processlist:
            '''
            processlist:
            [
                [进程名，到达时间，运行时间，剩余运行时间，完成时间，周转时间],
                [进程名，到达时间，运行时间，剩余运行时间，完成时间，周转时间]
            ]
            '''
            pro[5] = pro[4] - pro[1]
            avg_turnaround_time += pro[5]
            avg_weighted_turnaround_time += (pro[5] / pro[2])
        avg_turnaround_time /= len(self.processlist)
        avg_weighted_turnaround_time /= len(self.processlist)
        return avg_turnaround_time, avg_weighted_turnaround_time

    def fcfs(self):
        '''
        先来先服务调度（FCFS）
        每次调度是从就绪队列中，选择一个最先进入该队列的进程，把处理机分配给它，使之投入运行。
        该进程一直运行到完成或发生某事件而阻塞后，才放弃处理机。
        返回调度结果字符串
        分4种情况
        1.running不为空：让正在运行的进程运行完，让未到达的进程到达
        2.running为空，readylist不为空：让就绪队列头上cpu
        3.running为空，readylist为空，not_arrive不为空：如果时间到了，让未到达的进程到达，否则增加时间
        4.running为空，readylist为空，not_arrive为空：调度结束
        '''
        #开始这一次调度
        name = ''  #返回的进程名
        namelist = []  #返回的进程名列表
        timelist = []  #返回的到达时间列表
        start_time = data.time  #本次开始时间
        execution_time = 0  #本次运行的时间

        if len(self.running) != 0:  #有正在运行的进程时：
            #fcfs，本次运行的时间等于剩余运行时间
            execution_time = self.running[0].remaining_execution_time
            #本次运行的进程名
            name = self.running[0].name
            #正在运行的进程清空
            self.running.pop()
            #更新当前时间
            data.time += execution_time
            #更新进程的剩余执行时间和完成时间
            for pro in self.processlist:
                if pro[0] == name:
                    pro[3] -= execution_time
                    pro[4] = data.time

            #如果时间到了，让未到达的进程到达
            for pro in reversed(self.not_arrive):
                #倒序遍历，防止remove出错
                if pro.arrival_time <= data.time:
                    namelist.append(pro.name)
                    timelist.append(pro.arrival_time)
                    self.readylist.append(pro)
                    self.not_arrive.remove(pro)
            result = f'{start_time}~{data.time}ms：\t\t{name}运行\n'
            if len(namelist) != 0:
                for i in range(len(namelist)):
                    result += f'{timelist[i]}ms：\t\t{namelist[i]}到达\n'
                return result
            else:
                return result

        else:  #没有正在运行的进程时：
            if len(self.readylist) != 0:
                #有进程到达时，就绪队列头上cpu
                self.running.append(self.readylist.pop(0))
                name = self.running[0].name

                return f'{data.time}ms：\t\t{name}上cpu\n'

            else:
                #running,readylist,not_arrive都为空时，调度结束
                if len(self.not_arrive) == 0:
                    a, b = self.calculate_time()
                    return f'调度已结束\n平均周转时间：{a}ms\n平均带权周转时间：{b}ms\n'
                else:  #not_arrive不为空时

                    #如果时间到了，让未到达的进程到达
                    for pro in reversed(self.not_arrive):
                        #倒序遍历，防止remove出错
                        if pro.arrival_time <= data.time:
                            namelist.append(pro.name)
                            timelist.append(pro.arrival_time)
                            self.readylist.append(pro)
                            self.not_arrive.remove(pro)
                    result = ''
                    if len(namelist) != 0:
                        for i in range(len(namelist)):
                            result += f'{timelist[i]}ms：\t\t{namelist[i]}到达\n'
                        return result
                    else:
                        #如果时间没到，增加时间
                        data.time = self.not_arrive[-1].arrival_time
                        return f'{start_time}~{data.time}ms：\t\t无进程运行\n'

    def spf(self):
        '''
        非抢占式短进程优先调度（SPF）：
        每次调度是从就绪队列中，选择一个估计运行时间最短的进程，把处理机分配给它，使之投入运行。
        该进程一直运行到完成或发生某事件而阻塞后，才放弃处理机。
        返回调度结果字符串
        分4种情况
        1.running不为空：让正在运行的进程运行完，让未到达的进程到达
        2.running为空，readylist不为空：让就绪队列中最短的进程上cpu
        3.running为空，readylist为空，not_arrive不为空：如果时间到了，让未到达的进程到达，否则增加时间
        4.running为空，readylist为空，not_arrive为空：调度结束
        '''
        #开始这一次调度
        name = ''  #返回的进程名
        namelist = []  #返回的进程名列表
        timelist = []  #返回的到达时间列表
        start_time = data.time  #本次开始时间
        execution_time = 0  #本次运行的时间

        if len(self.running) != 0:  #有正在运行的进程时：
            #spf，本次运行的时间等于剩余运行时间
            execution_time = self.running[0].remaining_execution_time
            #本次运行的进程名
            name = self.running[0].name
            #正在运行的进程清空
            self.running.pop()
            #更新当前时间
            data.time += execution_time
            #更新进程的剩余执行时间和完成时间
            for pro in self.processlist:
                if pro[0] == name:
                    pro[3] -= execution_time
                    pro[4] = data.time

            #如果时间到了，让未到达的进程到达
            for pro in reversed(self.not_arrive):
                #倒序遍历，防止remove出错
                if pro.arrival_time <= data.time:
                    namelist.append(pro.name)
                    timelist.append(pro.arrival_time)
                    self.readylist.append(pro)
                    self.not_arrive.remove(pro)
            result = f'{start_time}~{data.time}ms：\t\t{name}运行\n'
            if len(namelist) != 0:
                for i in range(len(namelist)):
                    result += f'{timelist[i]}ms：\t\t{namelist[i]}到达\n'
                return result
            else:
                return result

        else:  #没有正在运行的进程时：
            if len(self.readylist) != 0:
                #有进程到达时，最短的上cpu，一样短则靠前的上cpu
                shortest_time = self.readylist[0].remaining_execution_time
                shortest_index = 0
                for index, pro in enumerate(self.readylist):
                    if pro.remaining_execution_time < shortest_time:
                        shortest_time = pro.remaining_execution_time
                        shortest_index = index

                self.running.append(self.readylist.pop(shortest_index))
                name = self.running[0].name

                return f'{data.time}ms：\t\t{name}上cpu\n'

            else:
                #running,readylist,not_arrive都为空时，调度结束
                if len(self.not_arrive) == 0:
                    a, b = self.calculate_time()
                    return f'调度已结束\n平均周转时间：{a}ms\n平均带权周转时间：{b}ms\n'
                else:  #not_arrive不为空时

                    #如果时间到了，让未到达的进程到达
                    for pro in reversed(self.not_arrive):
                        #倒序遍历，防止remove出错
                        if pro.arrival_time <= data.time:
                            namelist.append(pro.name)
                            timelist.append(pro.arrival_time)
                            self.readylist.append(pro)
                            self.not_arrive.remove(pro)
                    result = ''
                    if len(namelist) != 0:
                        for i in range(len(namelist)):
                            result += f'{timelist[i]}ms：\t\t{namelist[i]}到达\n'
                        return result
                    else:
                        #如果时间没到，增加时间
                        data.time = self.not_arrive[-1].arrival_time
                        return f'{start_time}~{data.time}ms：\t\t无进程运行\n'

    def srtf(self):
        '''
        最短剩余时间优先（SRTF）调度：是抢占式的SPF，即最短进程优先调度的抢占式版本。
        使用这个算法，调度程序总是选择剩余运行时间最短的那个进程运行。
        每当就绪队列有新到进程时，系统就将新到进程的剩余时间同当前运行进程的剩余时间做比较。
        如果新到进程比当前运行进程需要更少的剩余时间，当前进程就让出CPU回到就绪队列，而新到进程占用CPU运行。
        这种方式可以使新的短作业获得良好的服务。
        返回调度结果字符串
        分5种情况
        1.running不为空，not_arrive为空：不会再发生抢占，让正在运行的进程运行完
        2.running不为空，not_arrive不为空：增加时间
            2.1.如果时间增加后，running没运行完：让not_arrive最早到达的到达，判断是否抢占
            2.2.如果时间增加后，running运行完了：取消增加时间，让running运行完，增加时间
        3.running为空，readylist不为空：让就绪队列中最短的进程上cpu
        4.running为空，readylist为空，not_arrive不为空：如果时间到了，让未到达的进程到达，否则增加时间
        5.running为空，readylist为空，not_arrive为空：调度结束
        '''
        #开始这一次调度
        name = ''  #返回的进程名
        namelist = []  #返回的进程名列表
        timelist = []  #返回的到达时间列表
        start_time = data.time  #本次开始时间
        execution_time = 0  #本次运行的时间

        if len(self.running) != 0:  #有正在运行的进程时：
            #not_arrive为空时，不会再发生抢占
            if len(self.not_arrive) == 0:
                #本次运行的时间等于剩余运行时间
                execution_time = self.running[0].remaining_execution_time
                #本次运行的进程名
                name = self.running[0].name
                #正在运行的进程清空
                self.running.pop()
                #更新当前时间
                data.time += execution_time
                #更新进程的剩余执行时间和完成时间
                for pro in self.processlist:
                    if pro[0] == name:
                        pro[3] -= execution_time
                        pro[4] = data.time
                return f'{start_time}~{data.time}ms：\t\t{name}运行\n'
            else:
                #not_arrive不为空时，增加时间
                data.time = self.not_arrive[-1].arrival_time

                #如果时间增加后，running没运行完
                if data.time - start_time < self.running[
                        0].remaining_execution_time:
                    #本次运行的时间
                    execution_time = data.time - start_time
                    #本次运行的进程名
                    name = self.running[0].name
                    #更新进程的剩余执行时间
                    self.running[0].remaining_execution_time -= execution_time
                    for pro in self.processlist:
                        if pro[0] == name:
                            pro[3] -= execution_time
                    #让not_arrive最早到达的到达
                    self.readylist.append(self.not_arrive.pop())
                    #在running和readylist中寻找剩余运行时间最短的进程
                    shortest_time = self.running[0].remaining_execution_time
                    shortest_index = None
                    for index, pro in enumerate(self.readylist):
                        if pro.remaining_execution_time < shortest_time:
                            shortest_time = pro.remaining_execution_time
                            shortest_index = index

                    result = f'{start_time}~{data.time}ms：\t\t{name}运行\n{data.time}ms：\t\t{self.readylist[-1].name}到达\n'
                    #依旧是running最短时，不抢占
                    if shortest_index is None:
                        return result
                    else:
                        #抢占
                        self.readylist.append(self.running.pop())
                        self.running.append(self.readylist.pop(shortest_index))
                        result += f'{data.time}ms：\t\t{name}下cpu，{self.running[0].name}抢占\n'
                        return result
                else:  #如果时间增加后，running运行完了
                    #取消增加时间，让running运行完
                    data.time = start_time
                    #本次运行的时间等于剩余运行时间
                    execution_time = self.running[0].remaining_execution_time
                    #本次运行的进程名
                    name = self.running[0].name
                    #正在运行的进程清空
                    self.running.pop()
                    #更新当前时间
                    data.time += execution_time
                    #更新进程的剩余执行时间和完成时间
                    for pro in self.processlist:
                        if pro[0] == name:
                            pro[3] -= execution_time
                            pro[4] = data.time
                    return f'{start_time}~{data.time}ms：\t\t{name}运行\n'

        else:  #没有正在运行的进程时：
            if len(self.readylist) != 0:

                #在同一时刻有进程到达时
                for pro in reversed(self.not_arrive):
                    #倒序遍历，防止remove出错
                    if pro.arrival_time == data.time:
                        namelist.append(pro.name)
                        timelist.append(pro.arrival_time)
                        self.readylist.append(pro)
                        self.not_arrive.remove(pro)
                if len(namelist) != 0:
                    result = ''
                    for i in range(len(namelist)):
                        result += f'{timelist[i]}ms：\t\t{namelist[i]}到达\n'
                    return result

                #有进程到达时，最短的上cpu，一样短则靠前的上cpu
                shortest_time = self.readylist[0].remaining_execution_time
                shortest_index = 0
                for index, pro in enumerate(self.readylist):
                    if pro.remaining_execution_time < shortest_time:
                        shortest_time = pro.remaining_execution_time
                        shortest_index = index

                self.running.append(self.readylist.pop(shortest_index))
                name = self.running[0].name

                return f'{data.time}ms：\t\t{name}上cpu\n'

            else:
                #running,readylist,not_arrive都为空时，调度结束
                if len(self.not_arrive) == 0:
                    a, b = self.calculate_time()
                    return f'调度已结束\n平均周转时间：{a}ms\n平均带权周转时间：{b}ms\n'
                else:  #not_arrive不为空时

                    #如果时间到了，让未到达的进程到达
                    for pro in reversed(self.not_arrive):
                        #倒序遍历，防止remove出错
                        if pro.arrival_time <= data.time:
                            namelist.append(pro.name)
                            timelist.append(pro.arrival_time)
                            self.readylist.append(pro)
                            self.not_arrive.remove(pro)
                    result = ''
                    if len(namelist) != 0:
                        for i in range(len(namelist)):
                            result += f'{timelist[i]}ms：\t\t{namelist[i]}到达\n'
                        return result
                    else:
                        #如果时间没到，增加时间
                        data.time = self.not_arrive[-1].arrival_time
                        return f'{start_time}~{data.time}ms：\t\t无进程运行\n'


#创建数据对象
data = Data()


#定义窗口类
class Window:
    def __init__(self):
        #创建主窗口
        self.root = Tk()
        self.root.title('处理机调度')
        self.root.geometry('300x200')
        self.scheduling_mode = ''  #调度方式

        #创建按钮
        self.button1 = Button(
            self.root,
            text='先来先服务调度',
            command=lambda:
            [self.check_scheduling_mode('fcfs'),
             self.create_top_window()])
        self.button2 = Button(
            self.root,
            text='非抢占式短进程优先调度',
            command=lambda:
            [self.check_scheduling_mode('spf'),
             self.create_top_window()])
        self.button3 = Button(
            self.root,
            text='最短剩余时间优先调度',
            command=lambda:
            [self.check_scheduling_mode('srtf'),
             self.create_top_window()])
        self.button1.pack(fill='both', expand=True)
        self.button2.pack(fill='both', expand=True)
        self.button3.pack(fill='both', expand=True)

        self.root.mainloop()

    def check_scheduling_mode(self, scheduling_mode):
        #更改调度方式
        self.scheduling_mode = scheduling_mode

    def create_top_window(self):  #创建子窗口
        #冻结主窗口
        self.root.attributes('-disabled', 1)
        #创建子窗口
        self.top = Toplevel(self.root)
        #设置窗口标题
        if self.scheduling_mode == 'fcfs':
            self.top.title('先来先服务调度')
        elif self.scheduling_mode == 'spf':
            self.top.title('非抢占式短进程优先调度')
        elif self.scheduling_mode == 'srtf':
            self.top.title('最短剩余时间优先调度')
        #定义与标签关联的变量
        self.var_readylist = StringVar()
        self.var_readylist.set('就绪队列：')
        self.var_time = StringVar()
        self.var_time.set('当前时间：')
        #创建就绪队列标签
        self.label1 = Label(self.top, textvariable=self.var_readylist)
        self.label1.grid(row=0, column=0, sticky='w')
        #创建当前时间标签
        self.label2 = Label(self.top, textvariable=self.var_time)
        self.label2.grid(row=0, column=1, sticky='w')
        #创建测试数据表格
        self.label3 = Label(self.top, text='测试数据')
        self.label3.grid(row=1, column=0)
        column = ('process_name', 'arrival_time', 'remaining_execution_time')
        self.table = Treeview(self.top,
                              height=15,
                              columns=column,
                              show='headings')
        self.table.grid(row=2, column=0)
        #设置列
        self.table.column(0, width=100, anchor='center')
        self.table.column(1, width=100, anchor='center')
        self.table.column(2, width=100, anchor='center')
        #设置列标题
        self.table.heading(0, text='进程')
        self.table.heading(1, text='到达时间')
        self.table.heading(2, text='剩余执行时间')
        #创建切换下一组测试数据按钮
        self.button4 = Button(self.top, text='下一组', command=self.update1)
        self.button4.grid(row=3, column=0)
        #创建调度结果文本框
        self.label4 = Label(self.top, text='调度结果')
        self.label4.grid(row=1, column=1)
        self.text_box_result = ScrolledText(self.top, height=25, width=40)
        self.text_box_result.grid(row=2, column=1)
        #创建进行下一步调度按钮
        self.button5 = Button(self.top, text='下一步', command=self.update2)
        self.button5.grid(row=3, column=1)
        #关闭子窗口时，解冻主窗口并清空数据
        self.top.protocol(
            'WM_DELETE_WINDOW', lambda: [
                self.root.attributes('-disabled', 0),
                self.top.destroy(),
                data.clear()
            ])

        #生成第一组测试数据的列表,和未到达的进程列表
        data.create_this_list()
        #显示第一组测试数据
        self.display_data()
        debug()

        self.top.mainloop()

    def display_data(self):
        #点击‘下一组’时，在表格中显示测试数据，来源是datalist

        #清空已有数据
        children = self.table.get_children()
        for row in children:
            self.table.delete(row)

        #插入这组数据
        for pro in data.datalist[data.data_index]:
            #插入行
            self.table.insert('', 'end', values=(pro[0], pro[1], pro[2]))

    def update_table(self):
        #点击‘下一步’时，更新表格，来源是processlist

        #清空已有数据
        children = self.table.get_children()
        for row in children:
            self.table.delete(row)

        #更新这组数据
        for pro in data.processlist:
            #插入行
            self.table.insert('', 'end', values=(pro[0], pro[1], pro[3]))

    def update1(self):  #点击'下一组'时更新窗口
        data.clear()
        #更改测试数据索引
        if data.data_index == len(data.datalist) - 1:
            data.data_index = 0
        else:
            data.data_index += 1
        #生成当前这组测试数据的列表,和未到达的进程列表
        data.create_this_list()
        #在表格中显示测试数据
        self.display_data()
        #清空就绪队列
        self.var_readylist.set('就绪队列：')
        #清空当前时间
        self.var_time.set('当前时间：')
        #清空上一组的调度结果
        self.text_box_result.delete('1.0', END)
        debug()

    def update2(self):  #点击'下一步'时更新窗口

        #调度
        result = ''
        if self.scheduling_mode == 'fcfs':
            result = data.fcfs()
        elif self.scheduling_mode == 'spf':
            result = data.spf()
        elif self.scheduling_mode == 'srtf':
            result = data.srtf()

        #更新表格
        self.update_table()
        #更新就绪队列标签
        text = '就绪队列：'
        for ready in data.readylist:
            text += ready.name + ' '
        self.var_readylist.set(text)

        #调度结果插入文本框
        self.text_box_result.insert(END, result)
        #更新当前时间标签
        self.var_time.set(f'当前时间：{data.time}')
        debug()


Window()
