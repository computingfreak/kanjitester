#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  from_aligned_file.py
#  kanji_test
# 
#  Created by Lars Yencken on 06-11-2008.
#  Copyright 2008 Lars Yencken. All rights reserved.
#

import sys, optparse

import consoleLog
from cjktools.common import sopen
from cjktools import scripts

from kanji_test.util.alignment import AlignedFile

import align_core

_log = consoleLog.default

def from_aligned_file(syllabus_name, aligned_file, output_file):
    _log.start('Extracting gp-aligned words', nSteps=4)

    _log.log('Building set of expected words')
    include_set = set((w.surface, w.reading) for w in \
            align_core.iter_words(syllabus_name))

    _log.log('Loading alignments')
    alignments = AlignedFile(aligned_file)
    
    _log.log('Saving alignments')
    o_stream = sopen(output_file, 'w')
    for alignment in alignments:
        key = (alignment.grapheme, alignment.phoneme)
        if key in include_set:
            print >> o_stream, alignment.to_line()
            include_set.remove(key)
    o_stream.close()

    if include_set:
        _log.finish('%d entries not found (see missing.log)' % len(include_set))
        o_stream = sopen('missing.log', 'w')
        for surface, reading in sorted(include_set):
            print >> o_stream, '%s %s:%s %s' % (surface, reading, surface,
                reading)
        o_stream.close()
    else:
        _log.finish('All entries found')

#----------------------------------------------------------------------------#

def _create_option_parser():
    usage = \
"""%prog [options] syllabus_name aligned_file output_file

Extracts the alignments for the words in the syllabus from the aligned file."""

    parser = optparse.OptionParser(usage)

    parser.add_option('--debug', action='store_true', dest='debug',
            default=False, help='Enables debugging mode [False]')

    return parser

def main(argv):
    parser = _create_option_parser()
    (options, args) = parser.parse_args(argv)

    try:
        (syllabus_words, aligned_file, aligned_output) = args
    except ValueError:
        parser.print_help()
        sys.exit(1)

    from_aligned_file(syllabus_words, aligned_file, aligned_output)
    return

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    main(sys.argv[1:])

# vim: ts=4 sw=4 sts=4 et tw=78:
