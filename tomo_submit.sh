#!/bin/bash
#SBATCH -N 1                        # number of nodes
#SBATCH -n 12                        # number of cores
#SBATCH --mem 12G                  # memory pool for all cores
#SBATCH -t 0-00:15:00                   # runtime limit (D-HH:MM:SS)
#SBATCH --mail-type=FAIL 
#SBATCH --mail-user=haberbos@embl.de 
 
 
inputfile="$1";
inputdir="$2";
directive="$3";



module load IMOD
source $EBROOTIMOD/IMOD-linux.sh

tomouser=`whoami`;

extension=$([[ "$inputfile" = *.* ]] && echo ".${inputfile##*.}" || echo '')

base=${inputfile%$extension}

ext1=${extension,,}

sfile=$inputdir/$inputfile

 cp $sfile $TMPDIR/

 cd $TMPDIR
 ls
 batchruntomo -root $base -directive $directive -current . -em $tomouser@embl.de -cp 8

 rfile=$TMPDIR/${base}.rec

 cp $rfile $inputdir/