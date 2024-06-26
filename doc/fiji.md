# Start Fiji (EMCF flavor) on the EMBL Cluster

This tutorial explains how to launch Fiji as a cluster job for running computations.

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

## Launching Fiji

You should find an icon called `Fiji_Cluster` on your desktop.

![desktop](doc/img/desktop_icon.png "Fiji - Desktop icon")

If you don't (some more recent EMBL users might need that), open a terminal by right-clicking in an empty area of the desktop and selecting `Open Terminal here`.
Then copy and paste this command and execute it by pressing `Return`.

```cp /g/emcf/schorb/code/admin_scripts/Fiji_Cluster_GUI.desktop ~/Desktop```

Now, the desktop icon should be there.

When you click the icon the following window appears:

![params](doc/img/fiji_cluster_params.png "Fiji - Cluster parameters")

Here, you can control the resources you like to request for the cluster processing job. Be aware that your job will be terminated after the time limit you specify here, even when it is still running a computation. Also, the more resources (and the longer), your priority in getting them assigned will be lowered and you might have to wait some time until Fiji can start.

Once you click `Go`, the resources will be requested from the cluster and once a free slot is found, Fiji will launch. At the same time there will be a small window that reminds you of the remaining run time of the job.

![fiji_cluster](doc/img/cluster_fiji.png "Fiji - Cluster run")

You can in principle run multiple sessions at once, but this can get confusing to assign which Fiji runs as which job with its associated remaining time.

![multi-fiji](doc/img/multi-fiji.png "Fiji - multiple sessions")

The memory, you have requested before will be set to Fiji automatically. However, when you manually increased the number of assigned CPUs, you will have to tell this to Fiji to make use of them.

For this, you need to open `Edit -> Options -> Memory & Threads`.

![mem](doc/img/mem_threads.png "Fiji - Cluster parameters")

And here, you can specify the number of threads (= number of CPUs).

![numthreads](doc/img/mem_threads_01.png "Fiji - Cluster parameters")

## Interrupting sessions

When you run a long processing, there is no need to stay connected with x2go all the time. You can simply disconnect from the VPN and re-connect at any later time. The session will continue to run as it is.

To follow the formally correct procedure, you can also click the `Pause` button at the bottom of the x2go status frame for your running connection. This will disconnect but not end your session.

![pause](doc/img/x2go_pause.png "x2go - Pause")




## Connection problems


IT has upgraded the graphical login node for the cluster.
Therefore one connection setting has to be modified.
This only applies for machines where you have already used the X2go connection.

In this case you will get a "Host key cerification failed" error after accepting the (new) host key.

![x2go_key_error](doc/img/key_error.png "x2go - key error")

To fix this:

MAC:

- open a terminal
- type and run:
     open -a Textedit ~/.ssh/known_hosts
- in this file, remove the line that starts with "login-gui.cluster.embl.de"
- save the file


![x2go_key_update](doc/img/key_update.png "x2go - key update")

Windows:
- open a file explorer
- go to (type into the address bar) %USERPROFILE%\ssh
- open the file "known_hosts" with a text editor
- in this file, remove the line that starts with "login-gui.cluster.embl.de"
- save the file


Now, when connecting, X2go will ask you to accept the (new) host key. Hit yes and the connection should open. 

## Happy processing!
