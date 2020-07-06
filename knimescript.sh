#!/bin/bash

# creates cluster runtime scripts based on KNIME input.


p1="$1";
p2="$2";
p3="$3";

tail -n+2 knime_in.csv | cut -d, -f2 > tomo_submit.sh

tail -n+20 /g/emcf/schorb/code/cluster/tomo_submit.sh >> tomo_submit.sh


# remove windows line endings that screw up slurm
cp tomo_submit.sh tomo_submit.sh.bkp
tr -d '\015' <tomo_submit.sh.bkp > tomo_submit.sh

cat tomo_submit.sh > test.txt

/g/emcf/schorb/code/cluster/cluster_tomo.sh $p1 $p2 $p3