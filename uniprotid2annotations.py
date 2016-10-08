#!/usr/bin/env python3

import sys
import re
import multiprocessing as mp
import logging

import requests

#biopython
from Bio import SeqIO

###Prerequisites###
# requests, biopython
# e.g.
#  $ pip install requests biopython

###使い方###
# 引数1にuniprotIDをいれると関連したアノテーションが標準出力に出力される.
# 出力フォーマットはタブ区切りで，一行ずつにキーと値が表示される形式になっている.
# e.g. 
# python uniprotid2annotations.py uniprotID > out_gnlinks_annotations.tsv

#2016.10.8, created by Shohei Nagata
#uniprotKB IDを入力し，それをg-linksに投げて，結果をいい感じな形で出力する。

#環境
#anaconda, biopython

#呪文
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

num_proc = mp.cpu_count()
if num_proc > 16:
    num_proc = 16

def get_glinks_output(kbid):
    try:
        glinks_tsv = requests.get('http://link.g-language.org/{gene_id}/tsv'.format(gene_id=kbid))
    except:
        logger.warn("error while requesting.. retry")
#        time.sleep(0.001)
        glinks_tsv = get_glinks_output(kbid)
    return glinks_tsv

def generate_featkeyval_glinks_tsv(glinks_tsv): #returns -> str
    for line in glinks_tsv.text.split('\n'):
        if line.startswith('# '):  #also removes header :D
            line = line.replace('# ', '')
            kvd = line.split('\t')
            key = kvd[0]
            val = kvd[1]
#            val = val.replace(':', '_') #for GO
            yield '{k}\t{v}'.format(k=key, v=val)


if __name__ == '__main__':
    uniprotid = sys.argv[1]
    glinks_tsv = get_glinks_output(uniprotid)
    for s in generate_featkeyval_glinks_tsv(glinks_tsv):
        print(s)
    logger.info("done: {}".format(uniprotid))

#    pool = mp.Pool(num_proc)
#    for out_gb_record in pool.imap(reannotate_gbk_record, gbk_records): #LOCUSの順番を保持したければ，imapじゃなくてmapを使い，結果を全てが終了するまで全部ためる。
#        SeqIO.write(out_gb_record, sys.stdout, 'genbank')
#        logger.info("done: {}".format(out_gb_record.id))




