# EMCF Cluster tools for EMBL

Cluster tools for EMCF applications.

includes Constantin's nice slurm submitter...

[Instructions on how to start an interactive Fiji as a cluster job](doc/fiji.md)


# Handy commands:

- interactive cluster job:
```srun -t 60:00 -N1 -n1 -W 0 --pty -E $SHELL```
