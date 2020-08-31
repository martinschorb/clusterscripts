#! /usr/bin/python3

import os
import sys
import inspect
import subprocess
from datetime import datetime


n_threads = 4
time = 5
mem = 8

sparkdir = '/g/emcf/software/spark-3.0.0-bin-hadoop3.2/sbin/'


#%%
#===========================================================================

def write_slurm_template(script, out_path, env_name,
                         n_tasks, n_cpus, mem_limit, time_limit, mail_address, log, err, mailnotify=True,modules=None):


    slurm_template = ("#!/bin/bash\n"
                      "#SBATCH --job-name=spark"
                      "#SBATCH --nodes=%s\n"
                      "#SBATCH --ntasks-per-node=%s\n"
                      "#SBATCH --cpus-per-task=%s\n"
                      "#SBATCH --mem=%s\n"
                      "#SBATCH -t %i\n") % (n_nodes,n_tasks,n_cpus, mem_limit, time_limit)

    if mail_address is not None:
        slurm_template += ("#SBATCH --mail-type=FAIL,END\n" #"FAIL,BEGIN,END\n"
                           "#SBATCH --mail-user=%s\n") % mail_address


    slurm_template += "#SBATCH -e " + err + "_\%j.err\n"
    slurm_template += "#SBATCH -o " + log + "_\%j.log\n"

    slurm_template += ("\n"
                       "module purge \n"
                       "module load GCC \n"
                       'eval "$(/g/emcf/software/python/miniconda/bin/conda shell.bash hook)"\n'
                       "conda activate %s\n")
                       "module load Java\n")

#    if modules is not None:
#        slurm_template += ("module load " + modules.join(', ') + "\n")

    slurm_template += ("\n"
                       "%s/start-master.sh\n"
                       "sed -i \"1s/^/Slurm JOBID: $SLURM_JOBID - Spark server address:\n/\"  %s/active_server ") % (env_name,sparkdir)


    if (mail_address is not None) & mailnotify:
        slurm_template += ("\n"
                           "mail -s \"Your Spark submission in Job $SLURM_JOBID\" %s  %s/active_server" % (mail_address,sparkdir)

    slurm_template += ("\n"
                       "spark-submit --total-executor-cores %s --executor-memory %s %s\n") % (n_total,spark_mem_limit,script)

    with open(out_path, 'w') as f:
        f.write(slurm_template)


#%%
#===========================================================================



def submit_spark_slurm(script, input_, n_total=n_threads, n_threads=n_threads, mem_limit=str(mem)+'G',
                 time_limit=time,
                 env_name=None, mail_address=None,modules=None):

    tmp_folder = os.path.expanduser('~/.spark/slurm')
    os.makedirs(tmp_folder, exist_ok=True)

    print("Submitting script %s to cluster" % script)
    print("with arguments %s" % " ".join(input_))

    script_name = os.path.split(script)[1]
    dt = datetime.now().strftime('_%Y_%m_%d_%H:%M:%S.%f')

    #jobid = os.environ'$SLURM_JOBID'
    #jobid = jobid.rstrip('\n')

    tmp_name = os.path.splitext(script_name)[0] + dt #+ '_' + jobid


    batch_script = os.path.join(tmp_folder, '%s.sh' % tmp_name)
    log = os.path.join(tmp_folder, '%s' % tmp_name)
    err = os.path.join(tmp_folder, '%s' % tmp_name)

    if env_name is None:
        env_name = os.environ.get('CONDA_DEFAULT_ENV', None)
        if env_name is None:
            raise RuntimeError("Could not find conda")

    print("Batch script saved at", batch_script)
    print("Log will be written to %s.log, error log to %s.err" % (log, err))
    write_slurm_template(script, batch_script, env_name,
                         int(n_threads), mem_limit, int(time_limit), mail_address, log, err,modules=modules)

    cmd = ['sbatch', '-J', script_name, batch_script]
    cmd.extend(input_)
    subprocess.run(cmd)


#%%
#===========================================================================



def scrape_kwargs(input_):
    params = inspect.signature(submit_slurm).parameters
    kwarg_names = [name for name in params
                   if params[name].default != inspect._empty]
    kwarg_positions = [i for i, inp in enumerate(input_)
                       if inp in kwarg_names]

    kwargs = {input_[i]: input_[i + 1] for i in kwarg_positions}

    kwarg_positions += [i + 1 for i in kwarg_positions]
    input_ = [inp for i, inp in enumerate(input_) if i not in kwarg_positions]

    return input_, kwargs


#%%
#===========================================================================



def main():
    script = os.path.realpath(os.path.abspath(sys.argv[1]))
    input_ = sys.argv[2:]

    # scrape the additional arguments (n_threads, mem_limit, etc. from the input)
    input_, kwargs = scrape_kwargs(input_)
    submit_slurm(script, input_, **kwargs)


if __name__ == '__main__':
    main()
