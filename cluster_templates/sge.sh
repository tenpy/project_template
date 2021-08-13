#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -m ae # mail on 'a'bort and/or 'e'xit
{requirements}

set -e  # abort whole script if any command fails

# === prepare the environement as necessary ===
# module load python/3.7
# conda activate tenpy
{environment_setup}

#if you want to redirect output to file, you can use somehting like
# command &> "{jobname}.task_{task_id}.out"

echo "Running task {task_id} of {config_file} on $HOSTNAME at $(date)"
python {cluster_jobs_module} run {config_file} {task_id} 
echo "finished at $(date)"
