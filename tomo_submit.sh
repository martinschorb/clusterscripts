#!/bin/bash
#SBATCH -N 1                        # number of nodes
#SBATCH -n 12                        # number of cores
#SBATCH --mem 12G                  # memory pool for all cores
#SBATCH -t 0-00:30:00                   # runtime limit (D-HH:MM:SS)
#SBATCH --mail-type=FAIL 
#SBATCH --mail-user=schorb@embl.de 

numcpu=12 









# THIS NEEDS TO BE LINE 19 !!!
# ---------------------------------------------------------------------------------------------------

inputfile="$1";
inputdir="$2";
directive="$3";
option="$4";


module load IMOD

tomouser=`whoami`;

extension=$([[ "$inputfile" = *.* ]] && echo ".${inputfile##*.}" || echo '')

base=${inputfile%$extension}

ext1=${extension,,}

sfile=$inputdir/$inputfile

if [[ $option = "d" ]];
then
  base=${inputfile%a$extension}
  bfile=$inputdir/${inputfile%a$extension}b.st
  cp $bfile $TMPDIR/
fi

cp $sfile $TMPDIR/
cp $directive $TMPDIR/

loc_dir=$(basename "${directive}")

cd $TMPDIR

 if [[ $option = "m" ]]; # single axis montaged tomo with patch tracking and automated empty-area removal
 then
 echo starting automated removal of empty resin areas, montaged tomogram
 module load Anaconda2
 source $EBROOTIMOD/IMOD-linux.sh

 pip install --install-option="--prefix="$TMPDIR tifffile
 pip install --install-option="--prefix="$TMPDIR mrcfile
 export PYTHONPATH=$PYTHONPATH:$TMPDIR/lib/python2.7/site-packages
 python /g/emcf/schorb/code/cluster/patchtomo.py -u `whoami` -m $inputfile $loc_dir $numcpu
 
 elif [[ $option = "p" ]];# single axis tomo with patch tracking and automated empty-area removal
 then
 echo starting automated removal of empty resin areas
 module load Anaconda2
 source $EBROOTIMOD/IMOD-linux.sh

 pip install --install-option="--prefix="$TMPDIR tifffile
 pip install --install-option="--prefix="$TMPDIR mrcfile
 export PYTHONPATH=$PYTHONPATH:$TMPDIR/lib/python2.7/site-packages
 python /g/emcf/schorb/code/cluster/patchtomo.py -u `whoami` $inputfile $loc_dir $numcpu
 
 else
 batchruntomo -root $base -directive $loc_dir -current . -em $tomouser@embl.de -cp $numcpu
 fi
 
 
 rfile=$TMPDIR/${base}.rec
 cp $rfile $inputdir/ 
 
 cat etomo_err_*.log >> $inputdir/"$base-$SLURM_JOBID _err.log"
 cp batchruntomo.log $inputdir/"$base-$SLURM_JOBID .log"


