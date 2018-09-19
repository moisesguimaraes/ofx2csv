#!/bin/bash

for f in $1*.ofx; do ./ofx2csv.py $2 $f > ${f%.ofx}.csv; done
