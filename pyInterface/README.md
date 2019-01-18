# Python interfaces / wrappers
- *aioCalc_Fqq.py* iterates over Quantum Espresso software package outputs, extracting positions of ionic cores and localised electron clouds; converts this an input to ASAP software package to calculate Forces, electrostatic potential and store it on disk.
- *unitCellAutoRelaxer_theta.py* - relaxes a crystal structure while imposing a rhombohedral symmetry. Forces, stress components etc. are evaluated using ASAP software package; minimisation is via scipy.optimize
- *phonons* contains four codes that together calculate vibrational properties of a material at finite temperature.
