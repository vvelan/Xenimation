# Xenimation

This repository allows you to create animation gifs showing how energy depositions occur in xenon, how they produce dectable signals, and how this can vary for different types of interactions.

## Examples

To see some examples of Xenimation output, see the directories Plots_Custom, Plots_ERvsNR, Plots_VaryEnergy, and Plots_VaryField. Within each of those, there are gifs showing examples of animations you can make using Xenimation.

## Notebooks

There are four notebooks you can to use to produce these gifs. The Xenimate_ERvsNR.ipynb notebook lets you vary just particle type (ER/NR) for a given energy and field. The Xenimate_VaryEnergy.ipynb and Xenimate_VaryField.ipynb notebooks let you vary energy or field, while keeping the other and particle type constant. The Xenimate_Custom.ipynb notebook lets you define a custom path through various energies, fields, and particle types. See each notebook for more details.

## Documentation

The general principle behind Xenimation is that for a given interaction type, recoil energy, and drift field, there is a unique energy flow diagram that can be drawn. This diagram shows the fraction of energy going into each detectable channel. By combining diagrams from different interactions, one can create a smooth animation that shows how changing each parameter affects the energy partitioning.

See Plots_ERvsNR/NR_10keV_200Vcm.png for an example of what a single diagram looks like.

1. At top-left, the type of interaction is shown. This can be either "Electronic Recoil (ER)" or "Nuclear Recoil (NR)".
2. Below this, a green arrow represents the total energy deposited by the interaction. The recoil energy and drift field are displayed. Note that this is the **total** energy deposited, not the reconstructed energy or the detectable energy.
3. The energy is immediately deposited in three channels: excitation, ionization, and heat. Each of these channels has an associated arrow. The widths of these three arrows are related to the energy in each channel, and the combined widths of all three arrows is equal to the width of the original green arrow.
    - The width of the heat arrow is simply proportional to the fraction of energy going into heat for nuclear recoils, given by the Lindhard factor. For electronic recoils, the fraction of energy going into heat is unknown, but it is known to be a constant. This fraction can be set by the user in XenimationConfig.py; by default, it is set as 0.27 = 1 - (10 eV / 13.7 eV). This is an approximation that each excimer and e/ion pair was creating using 10 eV of energy (the VUV photons are 175 nm = 7 eV in xenon, and the xenon ionization energy in vaccum is 12 eV), but we know that W = 13.7 eV.
    - Here is a test.
