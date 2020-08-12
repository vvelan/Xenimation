# Xenimation

This repository allows you to create animation gifs showing how energy depositions occur in xenon, how they produce dectable signals, and how this can vary for different types of interactions.

## Installation

Installation is quite simple. You should have Python 3 installed on your machine, with the following libraries: numpy, scipy, matplotlib, PIL, and nestpy. The first four should be easy to find and install. You can find nestpy here: https://pypi.org/project/nestpy/ Other than that, just clone this repository to your machine, and you can get started!

## Notebooks (Quick and Easy to Use)

There are four notebooks you can to use to produce these gifs. The Xenimate_ERvsNR.ipynb notebook lets you vary just particle type (ER/NR) for a given energy and field. The Xenimate_VaryEnergy.ipynb and Xenimate_VaryField.ipynb notebooks let you vary energy or field, while keeping the other and particle type constant. The Xenimate_Custom.ipynb notebook lets you define a custom path through various energies, fields, and particle types. See each notebook for more details.

If you just want to create quick animations, without worrying about the details, just use these notebooks. Most of the parameters you might want to change are in there. There are a few other specifications you might want to set. In DetectorConfig.py, you can set the xenon density and the average molar mass of a xenon atom in a detector. In XenimationConfig.py, you can set graphical details, i.e. the figure size and colors, as well as the fraction of energy going into heat for electronic recoils.

## Examples

To see some examples of Xenimation output, see the directories Plots_Custom, Plots_ERvsNR, Plots_VaryEnergy, and Plots_VaryField. Within each of those, there are gifs showing examples of animations you can make using the Xenimation notebooks.

## Detailed Documentation

See Documentation.md for more detailed documentation on Xenimation.

## Contact

Need help? Notice bugs? Any suggestions for improvement? Contact Vetri Velan <vvelan@berkeley.edu>.
