import numpy as np
import math as m



##### USER MIGHT NEED TO CHANGE THESE #####

# Figure dimensions
fig_width = 16
fig_height = 9
axes_xmax = 1. * fig_width
axes_ymin = -1. * fig_height

# Colors
NR_color = '#FF0000'
ER_color = '#0000FF'
EDep_color = '#6AA84F'

# Fraction of width going into heat for ER
ER_heat_fraction = 0.27



##### USER UNLIKELY TO NEED TO CHANGE THESE #####

# Arrow box positions, angles, lengths, and widths (width for a0 only)
# xr means x-relative, i.e. relative to (0,0) at top-left and (1, -1) at bottom-right
a0_eDep_xr = 0.12
a0_eDep_yr = 0.55
a0_eDep_theta = 0.
a0_eDep_lr = 0.17
a0_eDep_wr = 0.25
a1_excitation_xr = 0.41
a1_excitation_yr = 0.33
a1_excitation_theta = 0.46
a1_excitation_lr = 0.11
a2_ionization_xr = 0.45
a2_ionization_yr = 0.63
a2_ionization_theta = -0.67
a2_ionization_lr = 0.11
a3_heat_xr = 0.32
a3_heat_yr = 0.77
a3_heat_theta = -1 * m.pi / 2
a3_heat_lr = 0.08
a4_recombination_xr = 0.55
a4_recombination_yr = 0.50
a4_recombination_theta = m.pi / 2
a4_recombination_lr = 0.16
a5_tfast_xr = 0.76
a5_tfast_yr = 0.15
a5_tfast_theta = 0.
a5_tfast_lr = 0.20
a6_tslow_xr = 0.76
a6_tslow_yr = 0.29
a6_tslow_theta = 0.
a6_tslow_lr = 0.20
a7_extraction_xr = 0.66
a7_extraction_yr = 0.92
a7_extraction_theta = 0.
a7_extraction_lr = 0.07
a8_s2_xr = 0.84
a8_s2_yr = 0.92
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
arrow_properties['color'] = np.full(len(arrow_properties['name']), '#000000')

# Arrow head properties
arrow_properties['head_hr'] = np.full(len(arrow_properties['name']), 0.04)
arrow_properties['head_h'] = arrow_properties['head_hr'] * axes_xmax
arrow_properties['min_head_br'] = np.full(len(arrow_properties['name']), 0.04)
arrow_properties['min_head_b'] = arrow_properties['min_head_br'] * axes_xmax
arrow_properties['head_b_scale'] = np.full(len(arrow_properties['name']), 1.6)

# Atom position and size
atom_left_posr = 0.17
atom_bottom_posr = 0.36
atom_widthr = 0.21
atom_heightr = 0.21

# Base (i.e. max) fontsize
title_fontsize = fig_width / 16. * 35.

# Text properties: text, position, halignment, fontsize, bolding, color
# Convention is same as arrow properties; see above
t0_pid_text = '%s Recoil (%s)'
t0_pid_xr = 0.015
t0_pid_yr = 0.06
t0_pid_halign = 'left'
t0_pid_fontsize = title_fontsize
t0_pid_bold = True
t1_eDep_text = 'Energy Deposition'
t1_eDep_xr = 0.015
t1_eDep_yr = 0.2
t1_eDep_halign = 'left'
t1_eDep_fontsize = title_fontsize * 0.85
t1_eDep_bold = True
t2_keV_text = '%.0f keV'
t2_keV_xr = 0.18
t2_keV_yr = 0.28
t2_keV_halign = 'right'
t2_keV_fontsize = title_fontsize * 0.85
t2_keV_bold = True
t3_field_text = '%.0f V/cm'
t3_field_xr = 0.20
t3_field_yr = 0.36
t3_field_halign = 'right'
t3_field_fontsize = title_fontsize * 0.85
t3_field_bold = True
t4_atom_text = 'Xe'
t4_atom_xr = 0.32
t4_atom_yr = 0.4
t4_atom_halign = 'center'
t4_atom_fontsize = title_fontsize * 1.2
t4_atom_bold = True
t5_heat_text = 'Heat (not observed)'
t5_heat_xr = 0.32
t5_heat_yr = 0.985
t5_heat_halign = 'center'
t5_heat_fontsize = title_fontsize * 0.85
t5_heat_bold = False
t6_excimer_text = r'Xe$_2^{*}$'
t6_excimer_xr = 0.3
t6_excimer_yr = 0.1
t6_excimer_halign = 'center'
t6_excimer_fontsize = title_fontsize
t6_excimer_bold = True
t7_eionpair_text = r'Xe$^{+}$/e$^{-}$'
t7_eionpair_xr = 0.3
t7_eionpair_yr = 0.9
t7_eionpair_halign = 'center'
t7_eionpair_fontsize = title_fontsize
t7_eionpair_bold = True
t8_tfast_text = r'$\tau_{fast}$'
t8_tfast_xr = 0.7
t8_tfast_yr = 0.1
t8_tfast_halign = 'center'
t8_tfast_fontsize = title_fontsize
t8_tfast_bold = True
t9_tslow_text = r'$\tau_{slow}$'
t9_tslow_xr = 0.7
t9_tslow_yr = 0.2
t9_tslow_halign = 'center'
t9_tslow_fontsize = title_fontsize
t9_tslow_bold = True
t10_S1_text = 'S1'
t10_S1_xr = 0.9
t10_S1_yr = 0.1
t10_S1_halign = 'center'
t10_S1_fontsize = title_fontsize
t10_S1_bold = True
t11_recombination_text = 'Recombination'
t11_recombination_xr = 0.6
t11_recombination_yr = 0.5
t11_recombination_halign = 'center'
t11_recombination_fontsize = title_fontsize
t11_recombination_bold = True
t12_electron_text = r'e$^{-}$'
t12_electron_xr = 0.7
t12_electron_yr = 0.9
t12_electron_halign = 'center'
t12_electron_fontsize = title_fontsize
t12_electron_bold = True
t13_S2_text = 'S2'
t13_S2_xr = 0.96
t13_S2_yr = 0.94
t13_S2_halign = 'center'
t13_S2_fontsize = title_fontsize * 1.2
t13_S2_bold = True

text_properties = {}
text_properties['name'] = ['pid', 'eDep', 'keV', 'field', 'atom', 'heat', 'excimer', 'eionpair', 'tfast', 'tslow', 'S1', 'recombination', 'electron', 'S2']
text_properties['text'] = np.array([t0_pid_text, t1_eDep_text, t2_keV_text, t3_field_text, t4_atom_text, t5_heat_text, t6_excimer_text, t7_eionpair_text, t8_tfast_text, t9_tslow_text, t10_S1_text, t11_recombination_text, t12_electron_text, t13_S2_text])
text_properties['xr'] = np.array([t0_pid_xr, t1_eDep_xr, t2_keV_xr, t3_field_xr, t4_atom_xr, t5_heat_xr, t6_excimer_xr, t7_eionpair_xr, t8_tfast_xr, t9_tslow_xr, t10_S1_xr, t11_recombination_xr, t12_electron_xr, t13_S2_xr])
text_properties['x'] = text_properties['xr'] * axes_xmax
text_properties['yr'] = np.array([t0_pid_yr, t1_eDep_yr, t2_keV_yr, t3_field_yr, t4_atom_yr, t5_heat_yr, t6_excimer_yr, t7_eionpair_yr, t8_tfast_yr, t9_tslow_yr, t10_S1_yr, t11_recombination_yr, t12_electron_yr, t13_S2_yr])
text_properties['y'] = text_properties['yr'] * axes_ymin
text_properties['halign'] = np.array([t0_pid_halign, t1_eDep_halign, t2_keV_halign, t3_field_halign, t4_atom_halign, t5_heat_halign, t6_excimer_halign, t7_eionpair_halign, t8_tfast_halign, t9_tslow_halign, t10_S1_halign, t11_recombination_halign, t12_electron_halign, t13_S2_halign])
text_properties['fontsize'] = np.array([t0_pid_fontsize, t1_eDep_fontsize, t2_keV_fontsize, t3_field_fontsize, t4_atom_fontsize, t5_heat_fontsize, t6_excimer_fontsize, t7_eionpair_fontsize, t8_tfast_fontsize, t9_tslow_fontsize, t10_S1_fontsize, t11_recombination_fontsize, t12_electron_fontsize, t13_S2_fontsize])
text_properties['bold'] = np.array([t0_pid_bold, t1_eDep_bold, t2_keV_bold, t3_field_bold, t4_atom_bold, t5_heat_bold, t6_excimer_bold, t7_eionpair_bold, t8_tfast_bold, t9_tslow_bold, t10_S1_bold, t11_recombination_bold, t12_electron_bold, t13_S2_bold])
text_properties['color'] = np.full(len(text_properties['name']), '#000000')
