# Xenimation

This repository allows you to create animation gifs showing how energy depositions occur in xenon, how they produce dectable signals, and how this can vary for different types of interactions.

## Detailed Documentation

Below is a relatively complete documentation for the structure of Xenimation. It does not include instructions on how to use the Jupyter notebooks; for that, you should read the READMEs in the notebooks themselves.

### Image layout

The general principle behind Xenimation is that for a given interaction type, recoil energy, and drift field, there is a unique energy flow diagram that can be drawn. This diagram shows the fraction of energy going into each detectable channel. By combining diagrams from different interactions, one can create a smooth animation that shows how changing each parameter affects the energy partitioning.

See Plots_ERvsNR/NR_10keV_200Vcm.png for an example of what a single diagram looks like.

1. At top-left, the type of interaction is shown. This can be either "Electronic Recoil (ER)" or "Nuclear Recoil (NR)". However, note that there are two available models for electronic recoils in NEST: the "beta" model and the "gamma" model. Xenimation defaults to the beta model, but the gamma model can be set.
2. Below this, a green arrow represents the total energy deposited by the interaction. The recoil energy and drift field are displayed. Note that this is the **total** energy deposited, not the reconstructed energy or the detectable energy. The width of this arrow is constant in Xenimation; it is a fixed fraction of the figure height.
3. The energy is immediately deposited in three channels: excitation, ionization, and heat. Each of these channels has an associated arrow. The widths of these three arrows are related to the energy in each channel, and the combined widths of all three arrows is equal to the width of the original green arrow.
    - The width of the heat arrow is simply proportional to the fraction of energy going into heat for nuclear recoils, given by the Lindhard factor. For electronic recoils, the fraction of energy going into heat is unknown, but it is known to be a constant. This fraction can be set by the user in XenimationConfig.py; by default, it is set as 0.27 = 1 - (10 eV / 13.7 eV). This is an approximation that each excimer and e/ion pair was creating using 10 eV of energy (the VUV photons are 175 nm = 7 eV in xenon, and the xenon ionization energy in vaccum is 12 eV), and we know that W = 13.7 eV.
    - The widths of the excitation and ionization arrows add together to equal the remainder of the energy. Their individual widths are proportional to the number of quanta (excimers or e/ion pairs) in that channel. For example, if an equal amount of excimers and e/ion pairs were generated, the excitation and ionization arrows would be of equal width. If twice as many excimers were generated as e/ion pairs, the excitation arrow would be twice as wide as the ionization arrow. Note that this implicitly assumes that the amount of energy required to create an excimer is equal to the energy required to create an e/ion pair. This is not strictly true, but it is an approximation we make.
4. The ionization arrow is split into the recombination and escape arrows, and its width is split according to the number of e/ion pairs that either recombine or do not recombine.
5. The escape arrow corresponds to escaping electrons, which eventually form the S2 signal in a xenon TPC. These arrow widths are identical.
6. The recombination arrow combines with the excitation arrow; the sum of their widths corresponds to the total number of excimers produced. Two arrows are depicted coming out of this interaction. These two arrows correspond to the fast (singlet) and slow (triplet) de-excitation channels. Their widths are proportional to the number of photons produced in these decays.
7. There is text spread around the image to help the reader. This text includes the type of atom/molecule at each stage, and it also numerically shows the number of quanta in each channel.

### Producing an image

The majority of the work to produce each image is done by functions in the Xenimation.py file. The user should not need to change this file. Namely, the GetFlowImage() function produces an Image object (from the PIL module) given a particle type, recoil energy, and drift field. It does this by the following process:

1. Simulate the interaction with NEST (specifically, with nestpy). Calculate the mean number of excimers, e/ion pairs, photons, and escaping electrons produced, as well as the fraction of energy going into heat and the singlet-to-triplet ratio.

2. Using these results, determine what the text on the image and the relative widths of each arrow should be.

3. Draw the text, the arrows, and the atom image on a matplotlib canvas. Convert the matplotlib figure to an Image object.
    - The position, size, and rotation of each of these objects, as well as the size of the canvas itself, are defined in XenimationConfig.py. See below in the "User Control" section for details.

4. Return this Image object to the user, and optionally save it as an image file.

### Producing an animation

Xenimation animations are saved as gifs. These are simply image files stitched together. As a result, an animation is produced by appending several image files into a gif, which can be done with simple tools in the PIL module. For more details, see the Jupyter notebooks, which show exactly how to do this.

### User control

Apart from the notebooks, the user should only need to adjust the parameters in DetectorConfig.py and XenimationConfig.py. The parameters in DetectorConfig.py are the liquid xenon densiy (in g/mL) and the average molar mass of a xenon atom in the detector (in g/mol). The XenimationConfig.py contains many parameters, but the user will likely only want to change the parameters in the top of the file, in the section "USER MIGHT NEED TO CHANGE THESE". These are the size of the figure itself, the colors of the arrows and text, and the fraction of energy going into heat for electronic recoils.

Advanced users might want to change the other parameters in XenimationConfig.py, although I recommend contacting Vetri Velan (<vvelan@berkeley.edu>) before doing this. In XenimationConfig.py, each arrow and each text is defined. This means that the position, rotation, and size of each arrow, and the position, rotation, font size, and value of each text block are manually defined. In situations where one of these parameters is dependent on the interaction itself (e.g. most of the arrow widths, most of the text values), it is left blank or filled with a template. The sizes and positions are defined relative to the figure size. Thus, if a user changes the figure size, they will not need to manually change these parameters.
