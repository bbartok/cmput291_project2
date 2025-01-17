#!/bin/bash
rm -f te.idx ye.idx re.idx

sort -u terms.txt | ./break.pl | db_load -c duplicates=1 -T -t btree te.idx
sort -u years.txt | ./break.pl | db_load -c duplicates=1 -T -t btree ye.idx
sort -u recs.txt | ./break.pl | db_load -c duplicates=1 -T -t hash re.idx
