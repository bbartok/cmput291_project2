#!/bin/bash
rm -f terms.idx years.idx recs.idx

sort -u terms.txt | ./break.pl | db_load -T -t btree te.idx
sort -u years.txt | ./break.pl | db_load -T -t btree ye.idx
sort -u recs.txt | ./break.pl | db_load -T -t hash re.idx
