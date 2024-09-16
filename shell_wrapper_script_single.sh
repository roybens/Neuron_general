#!/bin/bash

# rm -rf $SCRATCH/IC_Fitt*

cp -r `pwd`  $SCRATCH/NEURON_GENERAL-2
chmod -R 777 $SCRATCH/NEURON_GENERAL-2
sbatch plot_runfile_job.sh
	# sleep 10
