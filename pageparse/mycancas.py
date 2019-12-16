#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
   user:ligang
   mail:vagabond1132@gmail.com
   date:2019-10-15
    QQ :865853453
'''


'''
    mainframe 的 画布 绘制;;

'''

from  tkinter import *


class MyCanvas():
    def __init__(self, parentframe, cv_width, cv_height, colorset):
        '''     
            主窗口传递参数;;
        '''
        self.width = cv_width
        self.height = cv_height
        self.colorset = colorset

        '''
            绘制main_cv;
        '''
        self.cv = Canvas(parentframe, width= cv_width, height= cv_height, bg=colorset['cv_bg'])
    

    def clean_cv(self):
        self.cv.create_rectangle(0, 0, self.width, self.height, fill=self.colorset['cv_bg']);

    
    def itemDraw(self, itemlist, colortyp=None):
        self.cv.create_rectangle(0, 0, self.width, self.height, fill=self.colorset['cv_fg']);
        for item in itemlist:
            self.Draw(item, colortyp)
        self.cv.pack()
    
    def Draw(self, item, colortyp=None):
        if item.lockcolor:
            if colortyp is None:
                colortyp = 'tuple-select'
        else:
            colortyp = item.kind
        
        if item.end_x > self.width:
            self.cv.create_rectangle(0, item.start_y + item.itemheight, item.end_x - self.width, item.end_y + item.itemheight, fill=self.colorset[colortyp]);
        self.cv.create_rectangle(item.start_x, item.start_y, item.end_x, item.end_y, fill=self.colorset[colortyp]);
