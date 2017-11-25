##### A bash script that
- automatically creates a path in reciprocal space for Cubic phase of BaTiO3 phonon calculation,
- then acts as a wrapper around *Phonopy* software whuch extract symmetry of the system and generates relevant atomic displacements
- these displacements are parsed to create input to *proprietary* code ASAP (not available publically I'm afraid) which then calculates forces
- forces are parsed to create input for *Phonopy* to finish phonon calculation along the path in reciprocal space
- once complete, the output of *Phonopy* is parsed post-processed using "qpointBandConstructor.py" and "gnuPlotterThisSyst.gnu" gnuplot script is created
- cd to $pathOut and type "gnuplot < gnuPlotterThisSyst.gnu" to see the bands

##### cd ./phonons, (optionally edit and) run ./prepareFORCE\_SETSbto
