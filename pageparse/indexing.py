#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
   user:ligang
   mail:vagabond1132@gmail.com
   date:2019-11-25
   QQ :865853453


    进行解析Index;

'''

import struct
from parsepage import *


FILE_TYPE_INDEX_BRIN   = 'BRIN'
FILE_TYPE_INDEX_BTREE  = 'BTREE'
FILE_TYPE_INDEX_GIN    = 'GIN'
FILE_TYPE_INDEX_SPGIST = 'SPGIT'
FILE_TYPE_INDEX_HASH   = 'HASH'
FILE_TYPE_TABLE_DATA   = 'TABLE'


NO_INDEX  = 'FILENODE'


'''
#define SizeofPageHeaderData  (offsetof(PageHeaderData, pd_linp))   

#define TYPEALIGN(ALIGNVAL,LEN)  \\
    (((uintptr_t) (LEN) + ((ALIGNVAL) - 1)) & ~((uintptr_t) ((ALIGNVAL) - 1)))

#define MAXALIGN(LEN)           TYPEALIGN(MAXIMUM_ALIGNOF, (LEN))


## 偏移PageHeader; 进行读取METAPAGE;
#define PageGetContents(page)  \\
    ((char *)(page) + MAXALIGN(SizeofPageHeaderData))  

'''

class ParseFileType(object):
    def __init__(self, pagebuf):
        self.pageoff = 24  ## PageHeaderData sizeof;

        self.is_brin(pagebuf)
        pass


    def get_file_type(self):
        '''
            返回文件类型; 
        '''


        return NO_INDEX


    def is_brin(self, pagebuf):
        self.version = 1
        self.magic = 0xA8109CFA

        '''
        #define BRIN_CURRENT_VERSION		1
        #define BRIN_META_MAGIC			0xA8109CFA
        
        #define IS_BRIN_INDEX_METAPAGE(pagedata) \
        		 ((BrinMetaPageData *) PageGetContents((pagedata)))->brinVersion == \
        													BRIN_CURRENT_VERSION && \
        		 ((BrinMetaPageData *) PageGetContents((pagedata)))->brinMagic == \

        															BRIN_META_MAGIC
        typedef struct BrinMetaPageData
        {
            uint32      brinMagic;      => unsigned int; 4byte  I
            uint32      brinVersion;    => unsigned int; 4byte  I
            BlockNumber pagesPerRange;  => unsigned int; 4byte I
            BlockNumber lastRevmapPage; => unsigned int; 4byte I
        }BrinMetaPageData;
        '''

        self.brinstruct = struct.Struct('IIII');
        indexlist = self.brinstruct.unpack_from(pagebuf, self.pageoff)

        print('brinMagic  = %ld   Version = %ld  PreRange = %ld,  mapPage = %d' % (indexlist[0], indexlist[1], indexlist[2], indexlist[3]));

        return FILE_TYPE_INDEX_BRIN

    def is_btree(self):
        self.version = 2
        self.magic = 0x053162
        '''
            #define BTREE_MAGIC		0x053162	/* magic number of btree pages */
            #define BTREE_VERSION	2		/* current version number */

            #define IS_BTREE_INDEX_METAPGE(pagedata) \
                        BTPageGetMeta(pagedata)->btm_magic == BTREE_MAGIC && \
                        BTPageGetMeta(pagedata)->btm_version == BTREE_VERSION
        '''
        return FILE_TYPE_INDEX_BTREE

    def is_gin(self):
        '''
            #define GIN_CURRENT_VERSION		2
            
            #define IS_GIN_INDEX_METAPAGE(pagedata) \
            		 GinPageGetMeta(pagedata)->ginVersion == GIN_CURRENT_VERSION
        '''
        self.version = 2



        return FILE_TYPE_INDEX_GIN

    def is_spgist(self):
        '''
            typedef struct SpGistLastUsedPage
            {
                BlockNumber blkno;
                int         freeSpace;
            }SpGistLastUsedPage;
            
            #define SPGIST_CACHED_PAGES 8

            typedef struct SpGistLUPCache
            {
                SpGistLastUsedPage cachedPage[SPGIST_CACHED_PAGES];
            }SpGistLUPCache;


            typedef struct SpGistMetaPageData
            {
                uint32      magicNumber;
                SpGistLUPCache lastUsedPages;
            }SpGistMetaPageData;


            // gist-基础;
            //highgo_ligang_2019-07-27 11:49:46+0800 index spgist
            #define SPGIST_MAGIC_NUMBER (0xBA0BABEE)

            #define IS_SPGIST_INDEX_METAPAGE(pagedata) \
            	 SpGistPageGetMeta(pagedata)->magicNumber == SPGIST_MAGIC_NUMBER
        '''
        self.maigc = 0xBA0BABEE

        return FILE_TYPE_INDEX_SPGIST

    def is_hash(self):
        self.version = 4
        self.magic = 0x6440640
        '''
            #define HASH_MAGIC		0x6440640
            #define HASH_VERSION	4

            #define IS_HASH_INDEX_METAPAGE(pagedata) \
                HashPageGetMeta(pagedata)->hashm_magic == HASH_MAGIC && \
                HashPageGetMeta(pagedata)->hashm_version == HASH_VERSION

        '''
        return FILE_TYPE_INDEX_HASH

    def is_table(self):
        return FILE_TYPE_TABLE_DATA
