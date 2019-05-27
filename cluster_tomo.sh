#!/bin/bash

workdir="$1";
directive="$2";
option="$3";


# imodlatest='/g/emcf/software/imod_latest/IMOD';

#clusterscripts=~/clusterscripts


tomouser=`whoami`;

cd $workdir

find . -type f -iname '*.st' -or -iname '*.mrc'  | while IFS= read -r  file ;do
#      printf 'File found: '"'%s'"'\n' "$file"

#  	    curr_user=`stat -c %U "$file"`
#  	    echo $curr_user		    

 	    
 	    extension=$([[ "$file" = *.* ]] && echo ".${file##*.}" || echo '')
 	    
	    
  	    base=${file##*/}
#    	    echo $base
 	    directory=${file%$base}
 	    
 	    
  	    base1=${base%$extension}
# 	    echo $base1


  	    ext1=${extension,,}
#    	    echo $ext1

	    dir1=${directory:2}
	    dir1=$workdir/$dir1
#  	    echo $dir1
	    
# 	    tomotype=${dir1%%/*}
# 	    echo $tomotype

	    
#  	    case $tomotype in

if [[ $option == "d" ]]
then                     
      axis="${base1: -1}"
      if [[ $axis == "a" ]]
      then
	echo "submitting "$base" to the cluster for automatic dual-axis reconstruction."
	sbatch ./tomo_submit.sh $base $dir1 $directive $option
      fi
else 


  if [ -e $base1.rec ]
  then
      echo "skipping "$base" because it already exists."
  else
      echo "submitting "$base" to the cluster for automatic reconstruction."
      sbatch ./tomo_submit.sh $base $dir1 $directive $option
  fi

fi
	   
done