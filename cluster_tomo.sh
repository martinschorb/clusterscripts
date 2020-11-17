#!/bin/bash
#
#
# allowed options are:
#
#
# -p: automatic patch tracking,   will define the patch locations by excluding large light areas (empty resin,...)
# -m: automatic patch tracking for montages,   will perform above task for montaged tomos
# -d: dual axis,   set up processing and combination for dual-axis tomograms, axes need to be named *a.st and *b.st
# -fl: flattening,  runs automatic flattening and trimming of the reconstructed volume (ideal for serial tomos)
# -a: all data, dumps all intermediate data top the group share (for manual refinement, debugging)
#
#

workdir="$1";
directive="$2";
option="$3";

# imodlatest='/g/emcf/software/imod_latest/IMOD';

#clusterscripts=~/clusterscripts


tomouser=`whoami`;

cd "$workdir"

find . -type f -iname '*.st'  | while IFS= read -r  file ;do
#      printf 'File found: '"'%s'"'\n' "$file"

#  	    curr_user=`stat -c %U "$file"`
#  	    echo $curr_user


 	    extension=$([[ "$file" = *.* ]] && echo ".${file##*.}" || echo '')


  	    base=${file##*/}
#    	    echo $base
# 	    directory=${file%$base}
#	    echo $directory

  	    base1=${base%$extension}
#	    echo $base1

	    if [ ${base1:(-3)} == 'map' ]
	    then
	      continue
	    fi


  	    ext1=${extension,,}
#    	    echo $ext1

	    dir1=${directory:2}
	    dir1="$workdir"/"$dir1"
#  	    echo $dir1

# 	    tomotype=${dir1%%/*}
# 	    echo $tomotype

if [ ! -e tomo_submit.sh ]
then
  cp /g/emcf/schorb/code/cluster/tomo_submit.sh ./
  sed -i s/schorb@/${tomouser}@/g ./tomo_submit.sh
  # remove windows line endings that screw up slurm
  cp tomo_submit.sh tomo_submit.sh.bkp
  tr -d '\015' <tomo_submit.sh.bkp > tomo_submit.sh
fi



#  	    case $tomotype in

if [[ $option == *d* ]]
then
      base2=${base1%${base1: -1}}
      axis="${base1: -1}"
      if [ -e $base2.rec ]
      then
	echo "skipping "$base" because combined reconstruction already exists."
      else

	if [[ $axis == "a" ]]
	then
	  echo "submitting "$base" to the cluster for automatic dual-axis reconstruction."
	  sbatch ./tomo_submit.sh "$base" "$dir1" "$directive" $option
	fi
      fi
else


  if [ -e $base1.rec ]
  then
      echo "skipping "$base" because it already exists."
  else
      echo "submitting "$directory/$base" to the cluster for automatic reconstruction."
      sbatch ./tomo_submit.sh "$base" "$dir1" "$directive" $option
  fi

fi

done

rm -f tomo_submit.sh
