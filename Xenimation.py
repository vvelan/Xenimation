import os
import io
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import interpolate
from PIL import Image
import XenimationConfig as XC
import DetectorConfig as DC
import NESThelper
import nestpy
from Xenimation import *



def GetFlowImage(pid, eDep, field, savefig=True, output_dir='./', output_filename='test.png'):
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    fig, ax = plt.subplots(1, 1, figsize=(XC.fig_width, XC.fig_height))
    ax.set_xlim([0, XC.axes_xmax])
    ax.set_ylim([XC.axes_ymin, 0])
    
    SetColors(pid)

    if pid == 'NR':
        interaction = nestpy.INTERACTION_TYPE(0)
    elif pid == 'gamma':
        interaction = nestpy.INTERACTION_TYPE(7)
    elif pid == 'beta' or pid == 'ER':
        interaction = nestpy.INTERACTION_TYPE(8)
    
    yields = nestpy.NESTcalc(nestpy.VDetector()).GetYields(interaction,
        energy=eDep, density=DC.Density, drift_field=field)
    Ni = (yields.PhotonYield + yields.ElectronYield) / yields.ExcitonRatio / (1. + 1. / yields.ExcitonRatio)
    Nex = yields.PhotonYield + yields.ElectronYield - Ni
    Nph = yields.PhotonYield
    Ne = yields.ElectronYield
    L = yields.Lindhard
    if (pid == 'ER' or pid == 'beta' or pid == 'gamma'):
        # An estimate of how much energy goes into heat for ERs
        L = 1. - XC.ER_heat_fraction
    SingTripRatio = NESThelper.GetSingTripRatio(pid, eDep, field)

    SetText(pid, eDep, field, Ni, Nex, Nph, Ne, SingTripRatio)
    SetArrowWidths(pid, Ni, Nex, Nph, Ne, L, SingTripRatio)
    
    for a in range(len(XC.arrow_properties['name'])):
        DrawArrow(fig, ax, a)
    
    for t in range(len(XC.text_properties['name'])):
        DrawText(fig, ax, t)

    DrawAtom(fig, ax, pid)
    
    ax.set_xlim([0, XC.axes_xmax])
    ax.set_ylim([XC.axes_ymin, 0])
    ax.axis('off')
    fig.tight_layout()
    if savefig:
        fig.savefig(output_dir + output_filename, transparent=False)
        im_out = Image.open(output_dir + output_filename)
    else:
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        im_out = Image.open(buf)

    plt.close('all')
    return im_out



def SetColors(pid):
    
    XC.arrow_properties['color'][0] = XC.EDep_color
    for a in range(1, len(XC.arrow_properties['color'])):
        if (pid == 'ER' or pid == 'beta' or pid == 'gamma'):
            XC.arrow_properties['color'][a] = XC.ER_color
            XC.text_properties['color'][0] = XC.ER_color
        elif (pid == 'NR'):
            XC.arrow_properties['color'][a] = XC.NR_color
            XC.text_properties['color'][0] = XC.NR_color

    for t in range(1, 4):
        XC.text_properties['color'][t] = XC.EDep_color

    XC.text_properties['color'][14] = XC.Credit_color

    for t in range(15, 21):
        XC.text_properties['color'][t] = XC.NQuanta_color



def SetText(pid, eDep, field, Ni, Nex, Nph, Ne, SingTripRatio):
    
    if (pid == 'ER' or pid == 'beta' or pid == 'gamma'):
        XC.text_properties['text'][0] = XC.text_properties['template'][0] % ('Electronic', pid)
    elif (pid == 'NR'):
        XC.text_properties['text'][0] = XC.text_properties['template'][0] % ('Nuclear', pid)

    XC.text_properties['text'][2] = XC.text_properties['template'][2] % eDep
    XC.text_properties['text'][3] = XC.text_properties['template'][3] % field
    XC.text_properties['text'][15] = XC.text_properties['template'][15] % Nex
    XC.text_properties['text'][16] = XC.text_properties['template'][16] % Ni
    XC.text_properties['text'][17] = XC.text_properties['template'][17] % (Ni - Ne)
    XC.text_properties['text'][18] = XC.text_properties['template'][18] % (Nph / (1 + 1 / SingTripRatio))
    XC.text_properties['text'][19] = XC.text_properties['template'][19] % (Nph / (1 + SingTripRatio))
    XC.text_properties['text'][20] = XC.text_properties['template'][20] % Ne



def SetArrowWidths(pid, Ni, Nex, Nph, Ne, L, SingTripRatio):
    
    XC.arrow_properties['w'][1] = XC.arrow_properties['w'][0] * Nex / (Nex + Ni) * L
    XC.arrow_properties['w'][2] = XC.arrow_properties['w'][0] * Ni / (Nex + Ni) * L
    XC.arrow_properties['w'][3] = XC.arrow_properties['w'][0] * (1 - L)
    XC.arrow_properties['w'][4] = (Ni - Ne) / Ni * XC.arrow_properties['w'][2]
    XC.arrow_properties['w'][5] = Nph / Nex * XC.arrow_properties['w'][1] / (1 + 1 / SingTripRatio)
    XC.arrow_properties['w'][6] = Nph / Nex * XC.arrow_properties['w'][1] / (1 + SingTripRatio)
    XC.arrow_properties['w'][7] = Ne / Ni * XC.arrow_properties['w'][2]
    XC.arrow_properties['w'][8] = Ne / Ni * XC.arrow_properties['w'][2]
    XC.arrow_properties['head_b'] = np.maximum(XC.arrow_properties['w'] * XC.arrow_properties['head_b_scale'],
        XC.arrow_properties['min_head_b'])



def DrawArrow(fig, ax, arrow_id):
    
    a = arrow_id

    # Draw the four lines corresponding to the main rectangular box of the arrow
    # The lines are, in order: top, right, bottom, left, in unrotated space
    npts = 200
    box0_x_unrot = np.linspace(-1 * XC.arrow_properties['l'][a] / 2, XC.arrow_properties['l'][a] / 2, npts)
    box0_y_unrot = np.full(npts, XC.arrow_properties['w'][a] / 2)
    box0_x, box0_y = Rotate(box0_x_unrot, box0_y_unrot, XC.arrow_properties['theta'][a])
    box0_x, box0_y = Shift(box0_x, box0_y, XC.arrow_properties['x'][a], XC.arrow_properties['y'][a])
    box0_x, box0_y = GetXIncreasing(box0_x, box0_y)
    box1_x_unrot = np.full(npts, XC.arrow_properties['l'][a] / 2)
    box1_y_unrot = np.linspace(-1 * XC.arrow_properties['w'][a] / 2, XC.arrow_properties['w'][a] / 2, npts)
    box1_x, box1_y = Rotate(box1_x_unrot, box1_y_unrot, XC.arrow_properties['theta'][a])
    box1_x, box1_y = Shift(box1_x, box1_y, XC.arrow_properties['x'][a], XC.arrow_properties['y'][a])
    box1_x, box1_y = GetXIncreasing(box1_x, box1_y)
    box2_x_unrot = np.linspace(-1 * XC.arrow_properties['l'][a] / 2, XC.arrow_properties['l'][a] / 2, npts)
    box2_y_unrot = np.full(npts, -1 * XC.arrow_properties['w'][a] / 2)
    box2_x, box2_y = Rotate(box2_x_unrot, box2_y_unrot, XC.arrow_properties['theta'][a])
    box2_x, box2_y = Shift(box2_x, box2_y, XC.arrow_properties['x'][a], XC.arrow_properties['y'][a])
    box2_x, box2_y = GetXIncreasing(box2_x, box2_y)
    box3_x_unrot = np.full(npts, -1 * XC.arrow_properties['l'][a] / 2)
    box3_y_unrot = np.linspace(-1 * XC.arrow_properties['w'][a] / 2, XC.arrow_properties['w'][a] / 2, npts)
    box3_x, box3_y = Rotate(box3_x_unrot, box3_y_unrot, XC.arrow_properties['theta'][a])
    box3_x, box3_y = Shift(box3_x, box3_y, XC.arrow_properties['x'][a], XC.arrow_properties['y'][a])
    box3_x, box3_y = GetXIncreasing(box3_x, box3_y)

    # Draw the three lines corresponding to the arrow head
    # The lines are, in order: base, top diagonal, bottom diagonal (imagine arrow pointing right)
    head0_x_unrot = np.full(npts, XC.arrow_properties['l'][a] / 2)
    head0_y_unrot = np.linspace(-1 * XC.arrow_properties['head_b'][a] / 2, XC.arrow_properties['head_b'][a] / 2, npts)
    head0_x, head0_y = Rotate(head0_x_unrot, head0_y_unrot, XC.arrow_properties['theta'][a])
    head0_x, head0_y = Shift(head0_x, head0_y, XC.arrow_properties['x'][a], XC.arrow_properties['y'][a])
    head0_x, head0_y = GetXIncreasing(head0_x, head0_y)
    head1_x_unrot = np.linspace(XC.arrow_properties['l'][a] / 2, XC.arrow_properties['l'][a] / 2 + XC.arrow_properties['head_h'][a], npts)
    head1_y_unrot = np.linspace(XC.arrow_properties['head_b'][a] / 2, 0, npts)
    head1_x, head1_y = Rotate(head1_x_unrot, head1_y_unrot, XC.arrow_properties['theta'][a])
    head1_x, head1_y = Shift(head1_x, head1_y, XC.arrow_properties['x'][a], XC.arrow_properties['y'][a])
    head1_x, head1_y = GetXIncreasing(head1_x, head1_y)
    head2_x_unrot = np.linspace(XC.arrow_properties['l'][a] / 2, XC.arrow_properties['l'][a] / 2 + XC.arrow_properties['head_h'][a], npts)
    head2_y_unrot = np.linspace(-1 * XC.arrow_properties['head_b'][a] / 2, 0, npts)
    head2_x, head2_y = Rotate(head2_x_unrot, head2_y_unrot, XC.arrow_properties['theta'][a])
    head2_x, head2_y = Shift(head2_x, head2_y, XC.arrow_properties['x'][a], XC.arrow_properties['y'][a])
    head2_x, head2_y = GetXIncreasing(head2_x, head2_y)

    # Get the maximum and minimum boundaries for the arrow box
    box_x = np.linspace(min(min(box0_x), min(box1_x), min(box2_x), min(box3_x)),
        max(max(box0_x), max(box1_x), max(box2_x), max(box3_x)), npts * 2)
    box_y_lo = np.zeros(len(box_x))
    box_y_hi = np.zeros(len(box_x))
    box0_y_int = np.interp(box_x, box0_x, box0_y, left=np.nan, right=np.nan)
    box1_y_int = np.interp(box_x, box1_x, box1_y, left=np.nan, right=np.nan)
    box2_y_int = np.interp(box_x, box2_x, box2_y, left=np.nan, right=np.nan)
    box3_y_int = np.interp(box_x, box3_x, box3_y, left=np.nan, right=np.nan)
    for p in range(len(box_x)):
        box_y_lo[p] = np.nanmin([box0_y_int[p], box1_y_int[p], box2_y_int[p], box3_y_int[p]])
        box_y_hi[p] = np.nanmax([box0_y_int[p], box1_y_int[p], box2_y_int[p], box3_y_int[p]])

    # Get the maximum and minimum boundaries for the arrow head
    head_x = np.linspace(min(min(head0_x), min(head1_x), min(head2_x)),
        max(max(head0_x), max(head1_x), max(head2_x)), npts * 2)
    head_y_lo = np.zeros(len(head_x))
    head_y_hi = np.zeros(len(head_x))
    head0_y_int = np.interp(head_x, head0_x, head0_y, left=np.nan, right=np.nan)
    head1_y_int = np.interp(head_x, head1_x, head1_y, left=np.nan, right=np.nan)
    head2_y_int = np.interp(head_x, head2_x, head2_y, left=np.nan, right=np.nan)
    for p in range(len(head_x)):
        head_y_lo[p] = np.nanmin([head0_y_int[p], head1_y_int[p], head2_y_int[p]])
        head_y_hi[p] = np.nanmax([head0_y_int[p], head1_y_int[p], head2_y_int[p]])

    # Plot arrow
    ax.fill_between(box_x, box_y_lo, box_y_hi, color=XC.arrow_properties['color'][a])
    ax.fill_between(head_x, head_y_lo, head_y_hi, color=XC.arrow_properties['color'][a])



def DrawText(fig, ax, text_id):
    
    t = text_id
    ax.text(XC.text_properties['x'][t], XC.text_properties['y'][t], XC.text_properties['text'][t],
        fontsize=XC.text_properties['fontsize'][t], color=XC.text_properties['color'][t],
        ha=XC.text_properties['halign'][t], va='center',
        fontweight=('bold' * XC.text_properties['bold'][t] + 'normal' * (1 - XC.text_properties['bold'][t])))



def DrawAtom(fig, ax, pid):
    
    imat = plt.imread('Atom.png')
    imatax = fig.add_axes([XC.atom_left_posr, XC.atom_bottom_posr, XC.atom_widthr, XC.atom_heightr], anchor='NE', zorder=-1)
    imatax.imshow(imat)
    imatax.axis('off')

    imre = plt.imread('Recoil.png')
    if (pid == 'NR'):
        imreax = fig.add_axes([XC.recoil_NR_left_posr, XC.recoil_NR_bottom_posr, XC.recoil_NR_widthr, XC.recoil_NR_heightr],
            anchor='NE', zorder=-1)
    elif (pid == 'ER' or pid == 'gamma' or pid == 'beta'):
        imreax = fig.add_axes([XC.recoil_ER_left_posr, XC.recoil_ER_bottom_posr, XC.recoil_ER_widthr, XC.recoil_ER_heightr],
            anchor='NE', zorder=-1)
    imreax.imshow(imre)
    imreax.axis('off')



### Rotate a vector (x, y) by an angle theta [in radians]
def Rotate(x, y, theta):
    
    xnew = x * np.cos(theta) - y * np.sin(theta)
    ynew = x * np.sin(theta) + y * np.cos(theta)
    
    return xnew, ynew



### Shift a vector (x,y) by a constant (Shift_x, Shift_y)
def Shift(x, y, shift_x, shift_y):
    
    return (x + shift_x), (y + shift_y)



### Sort arrays such that x is monotonically increasing, so that it is compatible with numpy.interp
### Arguments: two numpy arrays of shape (N,)
### Returns: if x is monotonically increasing, return x and y unchanged
###          if x is monotonically decreasing, return x and y in reverse order
###          if x is not monotonically changing, return x and y changed; print an error message
def GetXIncreasing(x, y):
    
    # Get sorting order of x. If sort = 0, it is unsorted. If sort = 1, it is forward sorted.
    # If sort = 2, it is reverse sorted.
    sort = 1
    for i in range(1, len(x)):
        if (x[i] >= x[i-1]):
            continue
        else:
            sort = 2
            for j in range(1, len(x)):
                if (x[i] <= x[i-1]):
                    continue
                else:
                    sort = 0
                    break
            break

    if sort == 0:
        print('Warning in GetXIncreasing() in XenimationHelper.py; array is not monotonic')
        return x, y
    elif sort == 1:
        return x, y
    else:
        return x[::-1], y[::-1]
