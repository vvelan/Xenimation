import numpy as np
import math as m

# Figure dimensions
fig_width = 15
fig_height = 10
axes_xmax = 1. * fig_width
axes_ymin = -1. * fig_width

# Colors
NR_color = '#FF0000'
ER_color = '#0000FF'
EDep_color = '#6AA84F'

# Fraction of width going into heat for ER and NR
NR_heat_fraction = 0.85
ER_heat_fraction = 0.27

# Arrow positions, angles, lengths, and widths (width for a0 only)
# xr means x-relative, i.e. relative to (0,0) at top-left and (1, -1) at bottom-right
a0_eDep_xr = 0.14
a0_eDep_yr = 0.49
a0_eDep_theta = 0.
a0_eDep_lr = 0.13
a0_eDep_wr = 0.11
a1_excitation_xr = 0.41
a1_excitation_yr = 0.33
a1_excitation_theta = 0.46
a1_excitation_lr = 0.11
a2_ionization_xr = 0.41
a2_ionization_yr = 0.53
a2_ionization_theta = -0.67
a2_ionization_lr = 0.11
a3_heat_xr = 0.30
a3_heat_yr = 0.67
a3_heat_theta = -1 * m.pi / 2
a3_heat_lr = 0.07
a4_recombination_xr = 0.55
a4_recombination_yr = 0.50
a4_recombination_theta = m.pi / 2
a4_recombination_lr = 0.16
a5_tfast_xr = 0.76
a5_tfast_yr = 0.15
a5_tfast_theta = 0.
a5_tfast_lr = 0.23
a6_tslow_xr = 0.76
a6_tslow_yr = 0.29
a6_tslow_theta = 0.
a6_tslow_lr = 0.20
a7_extraction_xr = 0.66
a7_extraction_yr = 0.71
a7_extraction_theta = 0.
a7_extraction_lr = 0.07
a8_s2_xr = 0.84
a8_s2_yr = 0.71
a8_s2_theta = 0.
a8_s2_lr = 0.07

arrow_properties = {}
arrow_properties['name'] = ['eDep', 'excitation', 'ionization', 'heat', 'recombination', 'tfast', 'tslow', 'extraction', 's2']
arrow_properties['xr'] = np.array([a0_eDep_xr, a1_excitation_xr, a2_ionization_xr, a3_heat_xr, a4_recombination_xr, a5_tfast_xr, a6_tslow_xr, a7_extraction_xr, a8_s2_xr])
arrow_properties['x'] = arrow_properties['xr'] * axes_xmax
arrow_properties['yr'] = np.array([a0_eDep_yr, a1_excitation_yr, a2_ionization_yr, a3_heat_yr, a4_recombination_yr, a5_tfast_yr, a6_tslow_yr, a7_extraction_yr, a8_s2_yr])
arrow_properties['y'] = arrow_properties['yr'] * axes_ymin
arrow_properties['theta'] = np.array([a0_eDep_theta, a1_excitation_theta, a2_ionization_theta, a3_heat_theta, a4_recombination_theta, a5_tfast_theta, a6_tslow_theta, a7_extraction_theta, a8_s2_theta])
arrow_properties['lr'] = np.array([a0_eDep_lr, a1_excitation_lr, a2_ionization_lr, a3_heat_lr, a4_recombination_lr, a5_tfast_lr, a6_tslow_lr, a7_extraction_lr, a8_s2_lr])
arrow_properties['l'] = arrow_properties['lr'] * axes_xmax
arrow_properties['wr'] = np.array([a0_eDep_wr, 0., 0., 0., 0., 0., 0., 0., 0.])
arrow_properties['w'] = arrow_properties['wr'] * np.abs(axes_ymin)

# Arrow head properties
arrow_properties['head_hr'] = np.full(len(arrow_properties['name']), 0.04)
arrow_properties['head_h'] = arrow_properties['head_hr'] * axes_xmax
arrow_properties['min_head_br'] = np.full(len(arrow_properties['name']), 0.04)
arrow_properties['min_head_b'] = arrow_properties['min_head_br'] * axes_xmax

# [0.13827839 0.40567766 0.40934066 0.30494505 0.55494505 0.75824176 0.75824176 0.66117216 0.83516484]
# [0.49102873 0.33115891 0.5285492  0.67047445 0.49755403 0.1517132 0.28874447 0.70636359 0.70636359]
# 0.4597565780541614
# -0.6738629793235875