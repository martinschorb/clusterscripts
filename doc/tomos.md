# Reconstructing Tomograms with IMOD batch on the EMBL Cluster

This tutorial explains how to reconstruct tomograms on the EMBL cluster.

It makes use of the graphical login procedure for the EMBL cluster, described [here](https://wiki.embl.de/cluster/Env).


## Setting up x2go

Before you start, you need to install a client software to connect.
Just download x2goclient (available for Windows, Linux and Mac from [here](https://wiki.x2go.org/doku.php/doc:installation:x2goclient) and configure your session as follows.

When you first launch the program, you need to set up the connection. Click the white symbol in the top left corner to add a new connection.

![x2go](doc/img/X2go.png "x2go")

Here, you should the following connection details with your user name:

![x2go_connect](doc/img/conn_01.png "x2go - connection details")

If you want, you can also switch to the `Input/Output` tab to set up the display settings.

![x2go_disp](doc/img/conn_disp.png "x2go - display settings")


Once you have set up the connection, you can just launch it by double-clicking its box on the right side of the x2go main window. Put your password and you will get a graphical desktop on EMBL's cluster submission node.

## Launching The batch reconstructions

You should find an icon called `Tomo_Cluster` on your desktop.

![desktop](doc/img/cluster_icon.png "Tomogram Reconstruction - Desktop icon")

If you don't (some more recent EMBL users might need that), open a terminal by right-clicking in an empty area of the desktop and selecting `Open Terminal here`.
Then copy and paste this command and execute it by pressing `Return`.

```
cp /g/emcf/schorb/code/admin_scripts/Tomo_Cluster_GUI.desktop ~/Desktop
```

Now, the desktop icon should be there.

When you click the icon the following window appears:

![params](doc/img/tomo_cluster_params.png "Tomogram Reconstruction - Cluster parameters")

Here, you can control the resources you like to request for the individual reconstruction cluster processing job. Be aware that your jobs will be terminated after the time limit you specify here, even when it is still running a computation. For dual axis reconstruction, some more time is needed. Also, the more resources (and the longer), your priority in getting them assigned will be lowered and you might have to wait some time until the reconstructions can start. It is not recommended to request more than 16 CPUs for a job.

You then need to browse to the source directory that hosts all your tilt series (called `.st`). And you need to specify a batchdirective file in `ADOC` format.

If desired, you can also give additional parameters to request specific processing steps like patch area cleaning (`p`), montage stitching (`m`) or dual axis reconstruction (`d`).

Once you click `Go`, the resources will be requested from the cluster and once a free slot is found, the reconstructions will launch. At the same time there will be a small window that reminds you of the remaining run time of the job.

## Checking the status of running cluster jobs

By clicking the `Update Status` button, you will be presented with a list of all your running cluster jobs.

![status](doc/img/tomo_cluster_jobs.png "Cluster status")

You can also get this information when you re-open the GUI window without launching any additional reconstruction jobs.




## Interrupting sessions

When you run long processing, there is no need to stay connected with x2go all the time. You can simply disconnect (also from the VPN) and re-connect at any later time. The session will continue to run as it is.

To follow the formally correct procedure, you can also click the `Pause` button at the bottom of the x2go status frame for your running connection. This will disconnect but not end your session.

![pause](doc/img/x2go_pause.png "x2go - Pause")



## Happy reconstruction!
