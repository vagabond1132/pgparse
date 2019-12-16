#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
   user:ligang
   mail:vagabond1132@gmail.com
   date:2019-10-15
   QQ :865853453

    基本C结构类型

'''


'''
    import C struct;
        用于从文件中读取struct结构体;
'''

KIND_PAGE_HEADER = 'pageheader'
KIND_TUPLE_ITEM  = 'tupleitem'
KIND_TUPLE       = 'tuple'

class ParseStruct(object):
    pass
        

class PageHeader(ParseStruct):
    def __init__(self):
        '''
            PG Struct:
               include/stotage/bufpage.h
            typedef struct PageHeaderData   ==> 24byte;
            {
                PageXlogRecPtr pd_lsn;    ==> 8byte;  II

                uint16  pd_checksum;  => 2byte  H
                uint16  pd_flags;     => 2byte  H
                LocationIndex   pd_lower; => 2byte H
                LocationIndex   pd_upper; => 2byte H
                LocationIndex   pd_special; => 2byte H

                uint16  pd_pagesize_version; =>2byte H

                TransactionId   pd_prune_xid; => 4byte H
                ItemIdData  pd_linp[FLEXIBLE_ARRAY_MEMBER];  => 可变长数组, 保存item; 即0;
                    {
                        unsigned lp_off：15
                                 lp_flags:2,
                                 lp_len:15;

                        //unsigned int => 4 bytes;
                    }

            }PageHeaderData;

        '''
        self.pd_lsn = 0
        self.pd_checksum = 0
        self.pd_flags = 0
        self.pd_lower = 0
        self.pd_upper = 0
        self.pd_special = 0
        self.pd_pagesize_version = 0
        self.pd_prune_xid = 0
        self.pd_linp = 0

    def setPageHeader(self, list):
        self.pd_lsn = '%s/%s' % (list[0], list[1])
        self.pd_checksum = list[2]
        self.pd_flags = list[3]
        self.pd_lower = list[4]
        self.pd_upper = list[5]
        self.pd_special = list[6]
        self.pd_pagesize_version = list[7]
        self.pd_prune_xid = list[8]

    def getPageHeader(self):
        str =   'pd_lsn = %s\n' % self.pd_lsn  +  \
                'pd_checksum = %d\n' % self.pd_checksum + \
                'pd_flags = %d\n' % self.pd_flags + \
                'pd_lower = %d\n' % self.pd_lower + \
                'pd_upper = %d\n' % self.pd_upper + \
                'pd_special = %d\n' % self.pd_special + \
                'pd_pagesize_version = %d\n' % self.pd_pagesize_version + \
                'pd_prune_xid = %d\n' % self.pd_prune_xid 

        return str


class TupleItem(ParseStruct):
    def __init__(self):
        '''
            src/include/storage/itemid.h

            ItemIdData  pd_linp[FLEXIBLE_ARRAY_MEMBER];
                {
                    unsigned lp_off：15
                             lp_flags:2,
                             lp_len:15;

                    //unsigned int => 4 bytes;
                }
        '''
        self.lp_off = 0
        self.lp_flags = 0
        self.lp_len = 0

    def setTupleItem(self, list):
        itemstr =  '{:032b}'.format(list[0])

        # 按照2进制进行转换;;
        self.lp_len =  int(itemstr[0:15], 2)
        self.lp_flags = int(itemstr[15:17], 2)
        self.lp_off = int(itemstr[17:], 2)

    def getTupleItem(self):
        str =  'lp_len = %d\n' % self.lp_len + \
               'lp_flags = %d\n' % self.lp_flags + \
               'lp_off = %d\n' % self.lp_off 
        
        return str


class TupleHeaderData:
    def __init__(self):
        '''
           PG Struct:
                include/access/htup_details.h

            struct HeapTupleHeaderData{
                union
                {
                    HeapTupleFields t_heap;
                    DatumTupleField t_datum;
                }   t_choice;                   => 12byte III
                
                ItemPointerData t_ctid;         => 6byte HHH
                    {
                        uint16 bi_hi; => H
                        uint16 bi_lo; => H
                        uint16 offsetNumber; => H
                    }

                uint16  t_infomask2;            => 2byte H
                uint16  t_infomask;             => 2byte H
                uint8   t_hoff;                 => 1byte B
                bits8   t_bits[FLEXIBLE_ARRAY_MEMER];  => 0;
            };
        '''
        self.t_choice = 0

        self.t_ctid_blkid_bi_hi = 0
        self.t_ctid_blkid_bi_lo = 0
        self.t_ctid_posid = 0

        self.t_infomask2 = 0
        self.t_infomask = 0
        self.t_hoff = 0
        self.t_bits = 0
 

    def setTupleHeaderData(self, list):
        self.t_choice = list[0]
        self.t_ctid_blkid_bi_hi = list[3]
        self.t_ctid_blkid_bi_lo = list[4]
        self.t_ctid_posid  = list[5]
    
        self.t_infomask2 = list[6]
        self.t_infomask = list[7]
        self.t_hoff = list[8]
 

    def getTupleHeaderData(self):
        str =   't_choice => %d\n' % self.t_choice + \
                't_ctid.blkid.bi_hi => %d\n' % self.t_ctid_blkid_bi_hi + \
                't_ctid.blkid.bi_lo => %d\n' % self.t_ctid_blkid_bi_lo + \
                't_ctid.posid => %d\n' % self.t_ctid_posid + \
                't_infomask2 => %d\n' % self.t_infomask2 + \
                't_infomask => %d\n' % self.t_infomask + \
                't_hoff => %d\n' % self.t_hoff 

        return str



class Tuple(ParseStruct):
    def __init__(self, buf, buflen, tupleoff, tuplelen):
        self.buf = buf
        self.buflen = buflen
        self.tupleoff = tupleoff
        self.tuplelen = tuplelen

        print('buf = %s' % self.buf)
        print('buflen = %d' % self.buflen)
        print('tupleoff = %d' % self.tupleoff)
        print('tuplelen = %d' % self.tuplelen)
