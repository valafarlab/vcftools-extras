#!/usr/bin/env python2.7

from __future__ import print_function

import sys

import vcf

'''
consenpos - Get positions of the consensus corresponding to the reference
'''

def main():

    offset = 0

    vcf_reader = vcf.Reader(sys.stdin)
    vcf_reader.infos['CP'] = vcf.parser._Info('CP',1,'Integer','Consensus position')
    vcf_reader.infos['VL'] = vcf.parser._Info('VL',1,'Integer','Variant Length')
    vcf_writer = vcf.Writer(sys.stdout, vcf_reader)

    for record in vcf_reader:
        if len(record.ALT) != 1:
            print(("Multiple variants at position ",
                   str(record.POS)+". Will not determine consensus positions"),
                   sys.stderr)
            raise Exception

        record.INFO['CP'] = record.POS + offset
        record.INFO['VL'] = len(record.ALT[0]) - len(record.REF)
        
        if record.is_indel:
            offset += len(record.ALT[0]) - len(record.REF)

        vcf_writer.write_record(record)

if __name__ == '__main__':
    main()
