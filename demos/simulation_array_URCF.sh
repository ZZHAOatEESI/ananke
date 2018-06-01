#!/bin/bash
#$ -S bin/bash
#$ -j y
#$ -cwd
#$ -M zz374@drexel.edu
#$ -l h_rt=04:00:00
#$ -P rosenPrj
#$ -pe shm 1
#$ -l mem_free=10G
#$ -l h_vmem=8G
#$ -q all.q
#$ -t 2-47

. /etc/profile.d/modules.sh
. ~/.bashrc
module load shared
module load proteus
module load sge/univa
module load gcc/4.8.1

which python

SIMFILE=simulation_list.csv
SIMULATIONID=$(awk "(NR==$SGE_TASK_ID){print}" $SIMFILE | cut -d , -f 1)
NCLUST=$(awk "(NR==$SGE_TASK_ID){print}" $SIMFILE | cut -d , -f 2)
NTSPERCLUST=$(awk "(NR==$SGE_TASK_ID){print}" $SIMFILE | cut -d , -f 3)
NTP=$(awk "(NR==$SGE_TASK_ID){print}" $SIMFILE | cut -d , -f 4)
NSR=$(awk "(NR==$SGE_TASK_ID){print}" $SIMFILE | cut -d , -f 5)
SIGNALVAR=$(awk "(NR==$SGE_TASK_ID){print}" $SIMFILE | cut -d , -f 6)
SHIFTAMT=$(awk "(NR==$SGE_TASK_ID){print}" $SIMFILE | cut -d , -f 7)

mkdir -p simulations
ananke initialize shape -n ${NTP} -o simulations/simulation_${SIMULATIONID}.h5
ananke import simulation -i simulations/simulation_${SIMULATIONID}.h5 -c ${NCLUST} -t ${NTSPERCLUST} -n ${NSR} -s ${SHIFTAMT} -v ${SIGNALVAR} -o simulations/${SIMULATIONID}
ananke compute_distances -i simulations/simulation_${SIMULATIONID}.h5 -d sts -M 2 -m 0.01 -s 0.01 -z simulations/${SIMULATIONID}_signals.gz -o scores.txt
ananke compute_distances -i simulations/simulation_${SIMULATIONID}.h5 -d euclidean -M 2 -m 0.01 -s 0.01 -z simulations/${SIMULATIONID}_signals.gz -o scores.txt
ananke compute_distances -i simulations/simulation_${SIMULATIONID}.h5 -d dtw -M 2 -m 0.01 -s 0.01 -z simulations/${SIMULATIONID}_signals.gz -o scores.txt
ananke compute_distances -i simulations/simulation_${SIMULATIONID}.h5 -d ddtw -M 2 -m 0.01 -s 0.01 -z simulations/${SIMULATIONID}_signals.gz -o scores.txt
