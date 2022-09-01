#!/bin/bash

#SBATCH -N 1                        # number of nodes
#SBATCH -n 12                        # number of cores
#SBATCH --mem 8G                  # memory pool for all cores
#SBATCH -t 0-00:15:00                   # runtime limit (D-HH:MM:SS)
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=schorb@embl.de

numcpu=12








# THIS NEEDS TO BE LINE 19 !!!
# ---------------------------------------------------------------------------------------------------

inputfile="$1";
inputdir="$2";
directive="$3";
option="$4"

imod="IMOD"

module load $imod
source $EBROOTIMOD/IMOD-linux.sh

tomouser=`whoami`;

extension=$([[ "$inputfile" = *.* ]] && echo ".${inputfile##*.}" || echo '')

base1=$(basename "${inputfile}")

base=${base1%$extension}

ext1=${extension,,}

sfile="$inputdir"/"$inputfile"

if [[ $option = *d* ]];
then
  base=${inputfile%a$extension}
  bfile="$inputdir"/${inputfile%a$extension}b.st
  cp "$bfile" "$TMPDIR/"
  cp "$bfile.mdoc" "$TMPDIR/"
fi

echo "$sfile"

echo ---------------

cp "$sfile" "$TMPDIR/"
cp "$sfile.mdoc" "$TMPDIR/"
cp "$directive" "$TMPDIR/"

loc_dir=$(basename "${directive}")

cd "$TMPDIR"

 if [[ $option = *fl* ]]; # run automated flattening
 then
 echo runtime.ReplaceStep.any.20 = /g/emcf/schorb/code/cluster/flattentrim.sh \""$TMPDIR"/${base}_full.rec\">> "$loc_dir"
 fi


 if [[ $option = *m* ]]; # single axis montaged tomo with patch tracking and automated empty-area removal
 then
 echo starting automated removal of empty resin areas, montaged tomogram
 module load Anaconda3
 module load git

 source $EBROOTIMOD/IMOD-linux.sh

 pip install git+https://git.embl.de/schorb/pyem --user

 python /g/emcf/schorb/code/cluster/patchtomo.py -u `whoami` -m "$inputfile" "$loc_dir" $numcpu

 elif [[ $option = *p* ]];# single axis tomo with patch tracking and automated empty-area removal
 then
 echo starting automated removal of empty resin areas
 module load Anaconda3
 module load git
 module load $imod

 source $EBROOTIMOD/IMOD-linux.sh

 #pip install --install-option="--prefix="$TMPDIR tifffile
 #pip install --install-option="--prefix="$TMPDIR mrcfile
 pip install git+https://git.embl.de/schorb/pyem --user

 if [[ $option = *d* ]];
 then
  python /g/emcf/schorb/code/cluster/patchtomo.py -d -u `whoami` "$inputfile" "$loc_dir" $numcpu
 else
  python /g/emcf/schorb/code/cluster/patchtomo.py -u `whoami` "$inputfile" "$loc_dir" $numcpu
 fi

 else
  batchruntomo -root $base -directive $loc_dir -current . -em $tomouser@embl.de -cp $numcpu
 fi



if [[ $option = *a* ]];
then
  outputdir="$inputdir"/rec_${base}
  mkdir "$outputdir"

  cp "$TMPDIR"/* "$outputdir"

else

   rfile="$TMPDIR"/${base}.rec
   cp "$rfile" "$inputdir"/

  if [[ $option = *d* ]];
  then
    rfile_a="$TMPDIR"/${base}a.rec
    rfile_b="$TMPDIR"/${base}b.rec
    cp $rfile_a "$inputdir"/
    cp $rfile_b "$inputdir"/
  fi
fi

 cat etomo_err_*.log >> "$inputdir"/"$base-$SLURM_JOBID _err.log"
 cp batchruntomo.log "$inputdir"/"$base-$SLURM_JOBID .log"
