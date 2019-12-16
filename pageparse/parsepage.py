#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
   user:ligang
   mail:vagabond1132@gmail.com
   date:2019-10-15
    QQ :865853453

    解析上层传递的FileNme:
        解析其 PageHeader, TupleItem, Tuple 并解析Tuple Data;
'''


import os
import struct
from tkinter import messagebox


'''
'''
from pgtype import *


class ItemElem():
    def __init__(self, itemoff, itemlen, itemkind, itemstruct, TupleVale=''):
        '''
            根绝itemlen 来知道Kind; pageHeader or TupleItem ;

                计算每个Item的pos(start_x, start_y, end_x, end_y, color);
        '''
        self.cv_width = 896
        self.cv_height = 768 # 738
        self.itemwidth = 7
        self.itemheight = 12
        self.itemoff = itemoff
        self.itemlen = itemlen
        self.iteminfo = itemstruct  ## item - values;
        self.itemvalues = str(TupleVale)  ##内容转化;;;
        self.lockcolor = False
        
        self.step =  self.itemwidth * self.itemoff / self.cv_width  
        self.start_x = self.itemwidth * self.itemoff % self.cv_width
        self.start_y = self.itemheight * int(self.step)
        self.end_x =  self.itemwidth * (self.itemlen ) + self.start_x
        self.end_y =  self.start_y + self.itemheight
        self.kind =  itemkind


class ParsePage():
    def __init__(self, filename, pagesize, blkno):
        self.pageoff = 0
        self.pagebuf = ''

        '''
            罗列: 内容的数组;
        '''
        self.ItemList = []  ##记录总Total;
        self.tupleItemList = []
        self.lp_off = 0

        try:
            fp = open(filename, 'rb')
            fp.seek(pagesize * blkno)
            self.pagebuf = fp.read(pagesize)
            fp.close()


            '''
                解析类型ok;
            '''
            #ParseFileType(self.pagebuf)

        except:
            messagebox.showerror('error', "Can not open the file [%s]" % filename)

        self.pageHeaderStruct = struct.Struct('IIHHHHHHI')
        self.tupleItemStruct = struct.Struct('I')
        self.tupleHeaderStruct = struct.Struct('IIIHHHHHB')

        self.getPageHeader()

    def getPageHeader(self):
        structlist = self.pageHeaderStruct.unpack_from(self.pagebuf, self.pageoff)
        pageHeader = PageHeader()
        pageHeader.setPageHeader(structlist)

        pageEle = ItemElem(self.pageoff, self.pageHeaderStruct.size, KIND_PAGE_HEADER, pageHeader)
        self.ItemList.append(pageEle);

        self.pageoff = self.pageoff + self.pageHeaderStruct.size

        '''
            PageHeader + sizeof(4) -- 解析的TupleItem;
        '''
        itemTotal = (pageHeader.pd_lower - self.pageHeaderStruct.size ) / self.tupleItemStruct.size
        for loopitem in range(int(itemTotal)):
            self.getTupleItem()
            self.getTupleHeaderData()

    def getTupleItem(self):
        structlist = self.tupleItemStruct.unpack_from(self.pagebuf, self.pageoff)
        tupleItem = TupleItem()
        tupleItem.setTupleItem(structlist)
        tupleitemEle = ItemElem(self.pageoff, self.tupleItemStruct.size, KIND_TUPLE_ITEM, tupleItem)
        self.ItemList.append(tupleitemEle);
        self.pageoff += self.tupleItemStruct.size

        self.lp_off = tupleItem.lp_off
        self.lp_len = tupleItem.lp_len


    def getTupleHeaderData(self):
        tupleHeaderData = TupleHeaderData()
        structlist = self.tupleHeaderStruct.unpack_from(self.pagebuf, self.lp_off)
        tupleHeaderData.setTupleHeaderData(structlist)

        tuplevalue = self.pagebuf[self.lp_off + structlist[8]:self.lp_off + self.lp_len]
        ##print('TupleVale => %s' % tuplevalue)
        
        tupleheaderEle = ItemElem(self.lp_off, self.lp_len, KIND_TUPLE, tupleHeaderData, tuplevalue)

        self.ItemList.append(tupleheaderEle);
