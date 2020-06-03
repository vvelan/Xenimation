import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import interpolate
from PIL import Image
import XenimationConfig as XC
import DetectorConfig as DC
import NESThelper as nest



def getFlowImage(pid, eDep, field):
    
    fig, ax = plt.subplots(1, 1, figsize=(XC.fig_width, XC.fig_height))

    Ni, Nex, Nph, Ne = nest.GetYieldNR(eDep, field, DC.Density)
    XC.arrow_properties['w'][1] = XC.arrow_properties['w'][0] * Nex / (Nex + Ni) * (1 - XC.NR_heat_fraction)
    XC.arrow_properties['w'][2] = XC.arrow_properties['w'][0] * Ni / (Nex + Ni) * (1 - XC.NR_heat_fraction)
    XC.arrow_properties['w'][3] = XC.arrow_properties['w'][0] * XC.NR_heat_fraction
    XC.arrow_properties['w'][4] = (Ni - Ne) / Ni * XC.arrow_properties['w'][2]
    XC.arrow_properties['w'][5] = Nph / Nex * XC.arrow_properties['w'][1] * 0.05
    XC.arrow_properties['w'][6] = Nph / Nex * XC.arrow_properties['w'][1] * 0.95
    XC.arrow_properties['w'][7] = Ne / Ni * XC.arrow_properties['w'][2]
    XC.arrow_properties['w'][8] = Ne / Ni * XC.arrow_properties['w'][2]
    XC.arrow_properties['head_b'] = np.maximum(XC.arrow_properties['w'] * 1.25, XC.arrow_properties['min_head_b'])
    
    for a in range(len(XC.arrow_properties['name'])):

        # Draw the four lines corresponding to the main rectangular box of the arrow
        # The lines are, in order: top, right, bottom, left, in unrotated space
        npts = 200
        box0_x_unrot = np.linspace(-1 * XC.arrow_properties['l'][a] / 2, XC.arrow_properties['l'][a] / 2, npts)
        box0_y_unrot = np.full(npts, XC.arrow_properties['w'][a] / 2)
        box0_x, box0_y = rotate(box0_x_unrot, box0_y_unrot, XC.arrow_properties['theta'][a])
        box0_x, box0_y = shift(box0_x, box0_y, XC.arrow_properties['x'][a], XC.arrow_properties['y'][a])
        box0_x, box0_y = getXIncreasing(box0_x, box0_y)
        box1_x_unrot = np.full(npts, XC.arrow_properties['l'][a] / 2)
        box1_y_unrot = np.linspace(-1 * XC.arrow_properties['w'][a] / 2, XC.arrow_properties['w'][a] / 2, npts)
        box1_x, box1_y = rotate(box1_x_unrot, box1_y_unrot, XC.arrow_properties['theta'][a])
        box1_x, box1_y = shift(box1_x, box1_y, XC.arrow_properties['x'][a], XC.arrow_properties['y'][a])
        box1_x, box1_y = getXIncreasing(box1_x, box1_y)
        box2_x_unrot = np.linspace(-1 * XC.arrow_properties['l'][a] / 2, XC.arrow_properties['l'][a] / 2, npts)
        box2_y_unrot = np.full(npts, -1 * XC.arrow_properties['w'][a] / 2)
        box2_x, box2_y = rotate(box2_x_unrot, box2_y_unrot, XC.arrow_properties['theta'][a])
        box2_x, box2_y = shift(box2_x, box2_y, XC.arrow_properties['x'][a], XC.arrow_properties['y'][a])
        box2_x, box2_y = getXIncreasing(box2_x, box2_y)
        box3_x_unrot = np.full(npts, -1 * XC.arrow_properties['l'][a] / 2)
        box3_y_unrot = np.linspace(-1 * XC.arrow_properties['w'][a] / 2, XC.arrow_properties['w'][a] / 2, npts)
        box3_x, box3_y = rotate(box3_x_unrot, box3_y_unrot, XC.arrow_properties['theta'][a])
        box3_x, box3_y = shift(box3_x, box3_y, XC.arrow_properties['x'][a], XC.arrow_properties['y'][a])
        box3_x, box3_y = getXIncreasing(box3_x, box3_y)
        
        # Draw the three lines corresponding to the arrow head
        # The lines are, in order: base, top diagonal, bottom diagonal (imagine arrow pointing right)
        head0_x_unrot = np.full(npts, XC.arrow_properties['l'][a] / 2)
        head0_y_unrot = np.linspace(-1 * XC.arrow_properties['head_b'][a] / 2, XC.arrow_properties['head_b'][a] / 2, npts)
        head0_x, head0_y = rotate(head0_x_unrot, head0_y_unrot, XC.arrow_properties['theta'][a])
        head0_x, head0_y = shift(head0_x, head0_y, XC.arrow_properties['x'][a], XC.arrow_properties['y'][a])
        head0_x, head0_y = getXIncreasing(head0_x, head0_y)
        head1_x_unrot = np.linspace(XC.arrow_properties['l'][a] / 2, XC.arrow_properties['l'][a] / 2 + XC.arrow_properties['head_h'][a], npts)
        head1_y_unrot = np.linspace(XC.arrow_properties['head_b'][a] / 2, 0, npts)
        head1_x, head1_y = rotate(head1_x_unrot, head1_y_unrot, XC.arrow_properties['theta'][a])
        head1_x, head1_y = shift(head1_x, head1_y, XC.arrow_properties['x'][a], XC.arrow_properties['y'][a])
        head1_x, head1_y = getXIncreasing(head1_x, head1_y)
        head2_x_unrot = np.linspace(XC.arrow_properties['l'][a] / 2, XC.arrow_properties['l'][a] / 2 + XC.arrow_properties['head_h'][a], npts)
        head2_y_unrot = np.linspace(-1 * XC.arrow_properties['head_b'][a] / 2, 0, npts)
        head2_x, head2_y = rotate(head2_x_unrot, head2_y_unrot, XC.arrow_properties['theta'][a])
        head2_x, head2_y = shift(head2_x, head2_y, XC.arrow_properties['x'][a], XC.arrow_properties['y'][a])
        head2_x, head2_y = getXIncreasing(head2_x, head2_y)
                
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
        if (a == 0):
            ax.fill_between(box_x, box_y_lo, box_y_hi, color=XC.EDep_color)
            ax.fill_between(head_x, head_y_lo, head_y_hi, color=XC.EDep_color)
        else:
            ax.fill_between(box_x, box_y_lo, box_y_hi, color=XC.NR_color)
            ax.fill_between(head_x, head_y_lo, head_y_hi, color=XC.NR_color)

    if (pid == 'NR'):
        im = plt.imread('Atom_NR.png')
    elif (pid == 'ER'):
        im = plt.imread('Atom_ER.png')
    newax = fig.add_axes([0.2, 0.4, 0.1, 0.1], anchor='NE', zorder=-1)
    newax.imshow(im)
    newax.axis('off')

    ax.axis('off')
    fig.tight_layout()
    fig.savefig('test.png')



### Rotate a vector (x, y) by an angle theta [in radians]
def rotate(x, y, theta):
    
    xnew = x * np.cos(theta) - y * np.sin(theta)
    ynew = x * np.sin(theta) + y * np.cos(theta)
    
    return xnew, ynew



### Shift a vector (x,y) by a constant (shift_x, shift_y)
def shift(x, y, shift_x, shift_y):
    
    return (x + shift_x), (y + shift_y)



### Sort arrays such that x is monotonically increasing, so that it is compatible with numpy.interp
### Arguments: two numpy arrays of shape (N,)
### Returns: if x is monotonically increasing, return x and y unchanged
###          if x is monotonically decreasing, return x and y in reverse order
###          if x is not monotonically changing, return x and y changed; print an error message
def getXIncreasing(x, y):
    
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
        print('Warning in getXIncreasing() in XenimationHelper.py; array is not monotonic')
        return x, y
    elif sort == 1:
        return x, y
    else:
        return x[::-1], y[::-1]