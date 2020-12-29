#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
   user:ligang
   mail:vagabond1132@gmail.com
   date:2019-10-15
    QQ :865853453
'''

'''
    系统库
'''
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

import os

'''
    自己编写的库;
'''
from mycancas import MyCanvas
from parsepage import *

'''
界面操作:
    1. 控制窗口大小;
    2. 空间, 颜色， 大小， 布局

    left frame, main frame{canvas}, right franme;
'''
class MyWin():
    def __init__(self):
        self.win = Tk()
        self.colorSet = {}
        self.pageSize = 8 * 1024 ## default: Page  block =>  8k
        self.pageKind = 'rel'
        self.currBlk = self.totalBlk = 0
        self.fileName = ''
        #self.screenWidth = self.win.winfo_screenwidth()
        #self.screenHeight = self.win.winfo_screenheight() 
        self.screenWidth = 1366
        #self.creeenHeight = 768
        self.screenHeight = 780        
   
        self.prev_lock_item = None
        self.next_lock_item = None

    def MW_ColorSelect(self):

        ## 主要控件颜色
        self.colorSet['main_frame']  = 'lightgray'
        self.colorSet['left_frame']  = 'gray'
        self.colorSet['middle_frame']  = 'white'
        self.colorSet['right_frame'] = 'gray'
        self.colorSet['foot_frame'] = 'lightgray'

        self.colorSet['label_message_fg'] = 'white'
        self.colorSet['label_message_bg'] = 'gray'

        self.colorSet['foot_message_label'] = 'lightgray'

        ## 设置canvas 画布的颜色;
        self.colorSet['cv_fg'] = 'lightgray'
        self.colorSet['cv_bg'] = 'white'

        ## Page区域块;; {index, datafile}
        self.colorSet['page_header_fg'] = 'bisque'
        self.colorSet['page_header_bg'] = 'gray'
        self.colorSet['page_item_fg'] = 'red'
        self.colorSet['page_item_bg'] = 'gray'
        self.colorSet['page_tuple_fg'] = 'lime'
        self.colorSet['page_tuple_bg'] = 'gray'


        '''
            右侧显示信息:
        '''
        self.colorSet['page_message_fg'] = 'gray'
        self.colorSet['page_message_bg'] = 'lightgray'

        self.colorSet['tuple_item_message_fg'] = 'gray'
        self.colorSet['tuple_item_message_bg'] = 'lightgray'

        self.colorSet['tuple_message_fg'] = 'gray'
        self.colorSet['tuple_message_bg'] = 'lightgray'

        self.colorSet['wal_message_fg'] = 'gray'
        self.colorSet['wal_message_bg'] = 'lightgray'

        self.colorSet['tuple_value_fg'] = 'gray'
        self.colorSet['tuple_value_bg'] = 'lightgray'
    

        '''
            canvas -> item color;

                'aqua':                 '#00FFFF',
                'aquamarine':           '#7FFFD4',
                'azure':                '#F0FFFF',
                'beige':                '#F5F5DC',
                'bisque':               '#FFE4C4',
                'black':                '#000000',
                'blanchedalmond':       '#FFEBCD',
                'blue':                 '#0000FF',
                'blueviolet':           '#8A2BE2',
                'brown':                '#A52A2A',
                'burlywood':            '#DEB887',
                'cadetblue':            '#5F9EA0',
                'chartreuse':           '#7FFF00',
                'chocolate':            '#D2691E',
                'coral':                '#FF7F50',
                'cornflowerblue':       '#6495ED',
                'cornsilk':             '#FFF8DC',
        '''
        self.colorSet['pageheader'] = 'lime'
        self.colorSet['tupleitem'] = 'brown'
        self.colorSet['tuple'] = 'cadetblue'
        self.colorSet['tuple-select'] = 'orange'
        #self.colorSet['tupleheader'] = 'bisque'

        ##Wal file
        self.colorSet['wal_header'] = 'gray'

    def MW_AdjuseFrameSize(self):

        '''
            2:6:2
            ==>
            left_frame:middle_frame:right_frame;
        '''
        self.start_x = self.start_y = 0

        ## frame width & height
        self.foot_frame_height = 20
        self.middle_frame_width = 896

        self.foot_frame_width = self.right_frame_width  = self.left_frame_width = (self.screenWidth - self.middle_frame_width) / 2
        self.middle_frame_height  = self.right_frame_height = self.screenHeight
        self.left_frame_height = self.screenHeight - self.foot_frame_height

        # - self.foot_frame_height

        self.right_frame_messagebox_height = 200
        self.left_frame_messagebox_height = 500

        ## 控件;
        ## font_size
        self.label_message_size = 10
        self.page_header_size = 10
        self.tuple_item_size = 10
        self.tuple_size = 10
        self.wal_header_size = 10
        self.tuple_value_size = 10

        self.page_default_text = 'Page Header->\n'
        self.tuple_item_default_text = 'Tuple Item->\n'
        self.tuple_default_text = 'Tuple->\n'
        self.wal_default_text = 'Wal Header->\n'
        self.tuple_values_default_text = 'Tuple Values->\n'

        ''' 
            关键怎么绘制Item;
                8K = 8192byte 

        self.cv_width = 896
        self.cv_height = 768 # 738
        self.itemwidth = 7
        self.itemheight = 12
            
        '''
        
        ## canvas
        self.cv_width = self.middle_frame_width
        self.cv_height = self.middle_frame_height - 10

    '''
        绘制中心视图;
    '''
    def MW_MainFrame(self):
        self.mainframe = Frame(width=self.win.winfo_screenwidth(), height=self.win.winfo_screenheight())

        self.mainframe.left_frame = Frame(self.mainframe, width=self.left_frame_width, height=self.left_frame_height, bg=self.colorSet['left_frame'])
        self.mainframe.middle_frame = Frame(self.mainframe, width=self.middle_frame_width, height=self.middle_frame_height, bg=self.colorSet['middle_frame'])
        self.mainframe.right_frame = Frame(self.mainframe, width=self.right_frame_width, height=self.right_frame_height, bg=self.colorSet['right_frame'])


        self.MW_LeftFrame()
        self.MW_MiddleFrame()
        self.MW_RightFrame()

        self.mainframe.pack(side=TOP)

    '''
        绘制菜单栏;
    '''
    def MW_MainFrameMenu(self):
        menubar = Menu(self.win)

        ## file menu;
        file_menu = Menu(menubar)
        file_menu.add_command(label="Open(Ctrl+O)", command=self.action_openfile)
        file_menu.add_command(label="history(Ctrl+R)", command=self.action_read_history)

        #file_menu.add_separator()  ## 分割线;
        file_menu.add_command(label="Exit(Ctrl+Q)", command=self.win.quit)

        ##菜单栏;
        menubar.add_cascade(label="File", menu=file_menu)
        self.win.config(menu=menubar)

        self.win.bind("<Control-o>", self.action_openfile)
        self.win.bind("<Control-q>", self.win.quit)

    '''
        绘制左侧frame;
    '''
    def MW_LeftFrame(self):
        ##--- 功能控制按钮 ---

        ### ------选择 Page Size-------
        self.mainframe.left_frame.page_size_label = Label(self.mainframe.left_frame, text='PAGESIZE', bg=self.colorSet['label_message_bg'], fg=self.colorSet['label_message_fg'], font=('', self.label_message_size))
        self.mainframe.left_frame.page_size_label.place(x=20, y=40, width=80, height=20)

        self.mainframe.left_frame.page_size_combox =  ttk.Combobox(self.mainframe.left_frame, width=100, height=20, state='readonly')
        self.mainframe.left_frame.page_size_combox['values'] = ('8k', '16k', '32k', '64k', '128k')
        self.mainframe.left_frame.page_size_combox.current(0)
        self.mainframe.left_frame.page_size_combox.place(x=120, y=40, width=80, height=20)
        self.mainframe.left_frame.page_size_combox.bind("<<ComboboxSelected>>", self.action_page_select)

        ###  ------ 选择Page Kind -----------
        self.mainframe.left_frame.page_kind_label = Label(self.mainframe.left_frame, text='PAGEKIND', bg=self.colorSet['label_message_bg'], fg=self.colorSet['label_message_fg'], font=('', self.label_message_size))
        self.mainframe.left_frame.page_kind_label.place(x=20, y=80, width=80, height=20)

        self.mainframe.left_frame.page_kind_combox =  ttk.Combobox(self.mainframe.left_frame, width=100, height=20, state='readonly')
        self.mainframe.left_frame.page_kind_combox['values'] = ('rel', 'wal', 'brin', 'btree', 'gin', 'spgist', 'hash')
        self.mainframe.left_frame.page_kind_combox.current(0)
        self.mainframe.left_frame.page_kind_combox.place(x=120, y=80, width=80, height=20)
        self.mainframe.left_frame.page_kind_combox.bind("<<ComboboxSelected>>", self.action_page_select)

        ### ------提供BlK No选择------------
        self.mainframe.left_frame.prev_button = Button(self.mainframe.left_frame, text="Prev", command=self.action_button_prev)
        self.mainframe.left_frame.next_button = Button(self.mainframe.left_frame, text="Next", command=self.action_button_next)
        self.mainframe.left_frame.prev_button.place(x=20, y=120, width=80, height=20)
        self.mainframe.left_frame.next_button.place(x=120, y=120, width=80, height=20)

        ### 当前Page Blk显示;
        self.mainframe.left_frame.curr_blk_label = Label(self.mainframe.left_frame, text='Curr BlkNo: %d' % self.currBlk, bg=self.colorSet['label_message_bg'], fg=self.colorSet['label_message_fg'], font=('', self.label_message_size))
        self.mainframe.left_frame.curr_blk_label.place(x=0, y=170, width=120, height=20)
        self.mainframe.left_frame.total_blk_label = Label(self.mainframe.left_frame, text='Total BlkNo: %d' % self.totalBlk, bg=self.colorSet['label_message_bg'], fg=self.colorSet['label_message_fg'], font=('', self.label_message_size))
        self.mainframe.left_frame.total_blk_label.place(x=120, y=170, width=120, height=20)

        self.mainframe.left_frame.pack(side=LEFT) ##fill参数: Y 垂直， X水平


        '''
            应该使用富文本框;;
        '''
        self.mainframe.left_frame.tuplevalue_text = StringVar()
        self.mainframe.left_frame.tuplevalue_message = Message(self.mainframe.left_frame, bg=self.colorSet['tuple_value_bg'], fg=self.colorSet['tuple_value_fg'],
                textvariable=self.mainframe.left_frame.tuplevalue_text, anchor=NW, font=('', self.tuple_value_size))
        self.mainframe.left_frame.tuplevalue_message.place(x=self.start_x, y=self.start_y + 240 , width=self.left_frame_width, height=self.left_frame_messagebox_height)
        self.mainframe.left_frame.tuplevalue_message.bind('<Button-1>', self.action_tuple_values)
        self.mainframe.left_frame.tuplevalue_text.set(self.tuple_values_default_text)


    '''
        设置item tuple显示界面;;
    '''
    def MW_MiddleFrame(self):
        '''
            将参数传递给底层画布, 进行item显示;;
        '''
        self.mainframe.middle_frame.main_cv = MyCanvas(self.mainframe.middle_frame, self.cv_width, self.cv_height, self.colorSet)

        self.mainframe.middle_frame.main_cv.cv.bind('<Button-1>', self.action_canvas_click)
        self.mainframe.middle_frame.pack(side=LEFT)



    def MW_RightFrame(self):
        if 'rel' == self.pageKind:
            '''
                Page Header Info:
            '''
            self.mainframe.right_frame.page_header_text = StringVar()
            self.mainframe.right_frame.page_header_message = Message(self.mainframe.right_frame, bg=self.colorSet['page_message_bg'], fg=self.colorSet['page_message_fg'],
                    textvariable=self.mainframe.right_frame.page_header_text, anchor=NW, font=('', self.page_header_size))
            self.mainframe.right_frame.page_header_message.place(x=self.start_x, y=self.start_y, width=self.right_frame_width, height=self.right_frame_messagebox_height)
            self.mainframe.right_frame.page_header_message.bind('<Button-1>', self.action_page_header)
            self.mainframe.right_frame.page_header_text.set(self.page_default_text)

            '''
                Tuple Item Info:
                    //间隔 220即可;;
            '''
            self.mainframe.right_frame.tuple_item_text = StringVar()
            self.mainframe.right_frame.tuple_item_message = Message(self.mainframe.right_frame, bg=self.colorSet['tuple_item_message_bg'], fg=self.colorSet['tuple_item_message_fg'],
                    textvariable=self.mainframe.right_frame.tuple_item_text, anchor=NW, font=('', self.tuple_item_size))
            self.mainframe.right_frame.tuple_item_message.place(x=self.start_x, y=220, width=self.right_frame_width, height=self.right_frame_messagebox_height)
            self.mainframe.right_frame.tuple_item_message.bind('<Button-1>', self.action_tuple_item)
            self.mainframe.right_frame.tuple_item_text.set(self.tuple_item_default_text)

            '''
                Tuple Data:
            '''
            self.mainframe.right_frame.tuple_text = StringVar()
            self.mainframe.right_frame.tuple_message = Message(self.mainframe.right_frame, bg=self.colorSet['tuple_message_bg'], fg=self.colorSet['tuple_message_fg'],
                    textvariable=self.mainframe.right_frame.tuple_text, anchor=NW, font=('', self.tuple_size))
            self.mainframe.right_frame.tuple_message.place(x=self.start_x, y=440, width=self.right_frame_width, height=self.right_frame_messagebox_height)
            self.mainframe.right_frame.tuple_message.bind('<Button-1>', self.action_tuple)
            self.mainframe.right_frame.tuple_text.set(self.tuple_default_text)


        elif 'wal' == self.pageKind:
            '''
                Wal:
            '''
            self.mainframe.right_frame.wal_header_text = StringVar()
            self.mainframe.right_frame.wal_header_message = Message(self.mainframe.right_frame, bg=self.colorSet['wal_message_bg'], fg=self.colorSet['wal_message_fg'],
                    textvariable=self.mainframe.right_frame.wal_header_text, anchor=NW, font=('', self.wal_header_size))
            self.mainframe.right_frame.wal_header_message.place(x=self.start_x, y=self.start_y, width=self.right_frame_width, height=self.right_frame_height)
            self.mainframe.right_frame.wal_header_message.bind('<Button-1>', self.action_wal_header)
            self.mainframe.right_frame.wal_header_text.set(self.wal_default_text)

        self.mainframe.right_frame.pack(side=RIGHT)


    '''
        得到当前的Item;
            将相应的Tuple进行染色, 并且让更新右侧的记录;;
    '''
    def get_canvas_item(self, x, y):
        ret = None
        for item in self.page.ItemList:
            if self.prev_lock_item is not None:
                self.prev_lock_item.lockcolor = False
            
            if  KIND_PAGE_HEADER != item.kind and item.start_x < x and item.end_x > x and item.start_y < y and item.end_y > y:
                '''
                    关键是Item 与 tuple 如何关联;
                        item 中的数据如何进行展示;;
                '''
                item.lockcolor = True
                self.mainframe.middle_frame.main_cv.Draw(item, 'tuple-select')
                ret = self.find_boddy_by_item(item)
                if ret is not None:
                    ret.lockcolor = True
                    self.mainframe.middle_frame.main_cv.Draw(ret, 'tuple-select')
                self.prev_lock_item = item

            else:
                self.mainframe.middle_frame.main_cv.Draw(item)
        if ret is not None:
            ret.lockcolor = False
        
        return self.prev_lock_item, ret

    def find_boddy_by_item(self, item):
        '''
            无论通过tupleitem or tuple 都能对方的ItemElem; -- 图形信息;;
        '''
        for it in self.page.ItemList:
            ret = None
            if KIND_PAGE_HEADER == it.kind:
                continue

            if item.kind == it.kind:
                continue

            if KIND_TUPLE_ITEM == item.kind:
                '''
                    item is  tupleitem
                    it is tuple
                '''
                if item.iteminfo.lp_off  == it.itemoff:
                    ret = it
                    return ret

            elif KIND_TUPLE == item.kind:
                '''
                    item.kind is tuple
                    it.kind is tupleitem/
                '''
                if it.iteminfo.lp_off == item.itemoff:
                    ret = it
                    return ret


    '''
        点击画布功能;
        点击画布, 进行item 与 tuple的染色;
           需要根据 鼠标点击位置, 获取 pos
    '''
    def action_canvas_click(self, event):
        self.mainframe.middle_frame.main_cv.clean_cv()
        k, v = self.get_canvas_item(event.x, event.y)
        if None != k and None != v:
            if KIND_TUPLE_ITEM == k.kind:
                self.mainframe.right_frame.tuple_item_text.set(k.iteminfo.getTupleItem())

            if KIND_TUPLE == v.kind:
                self.mainframe.right_frame.tuple_text.set(v.iteminfo.getTupleHeaderData())
                self.mainframe.left_frame.tuplevalue_text.set(v.itemvalues)

            if KIND_TUPLE_ITEM == v.kind:
                self.mainframe.right_frame.tuple_item_text.set(v.iteminfo.getTupleItem())

            if KIND_TUPLE == k.kind:
                self.mainframe.right_frame.tuple_text.set(k.iteminfo.getTupleHeaderData())
                self.mainframe.left_frame.tuplevalue_text.set(k.itemvalues)

        else:
            self.resetTupleItem()

    '''
        right frame: 空间显示
    '''
    def action_wal_header(self, event):
        message = self.mainframe.right_frame.wal_header_text.get()
        messagebox.showinfo('Message Wal Header', message , parent=self.win)

    def action_page_header(self, event):
        message = self.mainframe.right_frame.page_header_text.get()
        messagebox.showinfo('Message Page Header', message , parent=self.win)


    def action_tuple_item(self, event):
        message = self.mainframe.right_frame.tuple_item_text.get()
        messagebox.showinfo('Message Tuple Item', message , parent=self.win)


    def action_tuple(self, event):
        message = self.mainframe.right_frame.tuple_text.get()
        messagebox.showinfo('Message Tuple', message , parent=self.win)

    def action_tuple_values(self, event):
        message = self.mainframe.left_frame.tuplevalue_text.get()
        messagebox.showinfo('Message Tuple Values', message , parent=self.win)


    '''
        PageSize & PageKind 可以放入同一个action;
    '''
    def action_page_select(self, event):
        '''
            发生改变重新出发 mainframe 的绘制
        '''
        if 'rel' == self.pageKind:
            self.mainframe.right_frame.page_header_message.place_forget()
            self.mainframe.right_frame.tuple_item_message.place_forget()
            self.mainframe.right_frame.tuple_message.place_forget()
        elif 'wal' == self.pageKind:
            self.mainframe.right_frame.wal_header_message.place_forget()

        self.pageSize = self.mainframe.left_frame.page_size_combox.get()
        self.pageKind = self.mainframe.left_frame.page_kind_combox.get()
        print("Combox: Page Size: %s " % self.pageSize);
        print("Combox: Page Kind: %s " % self.pageKind);

        self.MW_RightFrame()

    '''
        关于Page No显示问题;
    '''
    def action_button_prev(self):
        if self.currBlk > 0:
            self.currBlk -= 1
        self.mainframe.left_frame.curr_blk_label.config(text="Curr BlkNo: %d" % int(self.currBlk))
        print("button: prev  currblk %d" % int(self.currBlk))
        self.page = ParsePage(self.fileName, self.pageSize, self.currBlk)
        
        self.resetTupleItem()
        self.resetCancas()

    def action_button_next(self):
        if self.currBlk < self.totalBlk:
            self.currBlk = self.currBlk + 1

        self.mainframe.left_frame.curr_blk_label.config(text="Curr BlkNo: %d" % int(self.currBlk))
        print("button: next currblk： %d" % int(self.currBlk))
        self.page = ParsePage(self.fileName, self.pageSize, self.currBlk)

        self.resetTupleItem()
        self.resetCancas()


    '''
        显示框进行内容恢复;
    '''
    def resetTupleItem(self):
        self.mainframe.right_frame.tuple_item_text.set(self.tuple_item_default_text);
        self.mainframe.right_frame.tuple_text.set(self.tuple_default_text)
        self.mainframe.left_frame.tuplevalue_text.set(self.tuple_values_default_text)

    '''
        可选item控件进行颜色恢复;
    '''
    def resetCancas(self):
        self.mainframe.middle_frame.main_cv.itemDraw(self.page.ItemList)

    '''
        Open file控件;
    '''
    def action_openfile(self, event):
        self.fileName = filedialog.askopenfilename(initialdir=os.getcwd(), title='打开文件', filetypes=[('All Files', '*')])
        if self.fileName != '':
            self.win.title('PageParse: %s' % self.fileName)
            self.mainframe.middle_frame.main_cv.clean_cv()
            '''
                open file: 需要计算file size; 并且更新total blk, curr blk;
            '''
            self.fileSize = os.path.getsize(self.fileName)
            self.currBlk = 0
            self.totalBlk = self.fileSize / self.pageSize

            '''
                解析新打开的文件;
            '''
            self.page = ParsePage(self.fileName, self.pageSize, self.currBlk)

            self.mainframe.left_frame.total_blk_label.config(text="Total BlkNo: %d" % int(self.totalBlk))
            self.mainframe.middle_frame.main_cv.itemDraw(self.page.ItemList)

            '''
                直接显示当前的PageHeader:
            '''
            for item in self.page.ItemList:
                if item.kind == 'pageheader':
                    self.mainframe.right_frame.page_header_text.set(item.iteminfo.getPageHeader())
                    break
            '''
                并且记录到历史文件;  parse_history;
            '''
            self.action_write_history()


    def action_write_history(self):
        #fp = open('parse_history', 'a')
        #print("write [%s] to parse_history" % str(self.fileName))
        #fp.writelines(self.fileName + '\r')
        #fp.close()
        pass


    def action_read_history(self):
        '''
            弹窗提示;
        '''
        pass
    
        #with open('parse_history', 'r') as f:
        #    print(f.readline())



    '''
        启动窗口;
    '''
    def MW_Start(self):
        self.win.title('PageParse')
        self.win.geometry(str('%dx%d+0+0') % (self.screenWidth, self.screenHeight))
        #self.win.resizable(width=False, height=False) ## 禁止窗口拉伸;;
        self.win.maxsize(self.screenWidth, self.screenHeight)
        self.win.minsize(int(self.screenWidth / 2), int(self.screenHeight / 2))

        self.MW_ColorSelect()       ## 设置颜色集合;
        self.MW_AdjuseFrameSize()   ## 设置每个frame 以及 控件 大小;

        self.MW_MainFrame()         ## 设置主窗口; - 显示窗口;
        self.MW_MainFrameMenu()     ## 设置菜单栏;;
        #self.MW_FootFrame()         ## 设置底边信息;
        self.win.mainloop()

    '''
        窗口退出;
    '''
    def MW_Exit(self, message):
        print('MW_exit:  %s' % message)
        sys.exit(1)


if '__main__' == __name__:
    MyWin().MW_Start()
