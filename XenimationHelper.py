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
        box0_x = box0_x_unrot * np.cos(XC.arrow_properties['theta'][a]) - box0_y_unrot * np.sin(XC.arrow_properties['theta'][a])
        box0_y = box0_x_unrot * np.sin(XC.arrow_properties['theta'][a]) + box0_y_unrot * np.cos(XC.arrow_properties['theta'][a])
        box0_x += XC.arrow_properties['x'][a]
        box0_y += XC.arrow_properties['y'][a]
        box1_x_unrot = np.full(npts, XC.arrow_properties['l'][a] / 2)
        box1_y_unrot = np.linspace(-1 * XC.arrow_properties['w'][a] / 2, XC.arrow_properties['w'][a] / 2, npts)
        box1_x = box1_x_unrot * np.cos(XC.arrow_properties['theta'][a]) - box1_y_unrot * np.sin(XC.arrow_properties['theta'][a])
        box1_y = box1_x_unrot * np.sin(XC.arrow_properties['theta'][a]) + box1_y_unrot * np.cos(XC.arrow_properties['theta'][a])
        box1_x += XC.arrow_properties['x'][a]
        box1_y += XC.arrow_properties['y'][a]
        box2_x_unrot = np.linspace(-1 * XC.arrow_properties['l'][a] / 2, XC.arrow_properties['l'][a] / 2, npts)
        box2_y_unrot = np.full(npts, -1 * XC.arrow_properties['w'][a] / 2)
        box2_x = box2_x_unrot * np.cos(XC.arrow_properties['theta'][a]) - box2_y_unrot * np.sin(XC.arrow_properties['theta'][a])
        box2_y = box2_x_unrot * np.sin(XC.arrow_properties['theta'][a]) + box2_y_unrot * np.cos(XC.arrow_properties['theta'][a])
        box2_x += XC.arrow_properties['x'][a]
        box2_y += XC.arrow_properties['y'][a]
        box3_x_unrot = np.full(npts, -1 * XC.arrow_properties['l'][a] / 2)
        box3_y_unrot = np.linspace(-1 * XC.arrow_properties['w'][a] / 2, XC.arrow_properties['w'][a] / 2, npts)
        box3_x = box3_x_unrot * np.cos(XC.arrow_properties['theta'][a]) - box3_y_unrot * np.sin(XC.arrow_properties['theta'][a])
        box3_y = box3_x_unrot * np.sin(XC.arrow_properties['theta'][a]) + box3_y_unrot * np.cos(XC.arrow_properties['theta'][a])
        box3_x += XC.arrow_properties['x'][a]
        box3_y += XC.arrow_properties['y'][a]
        
        # Draw the three lines corresponding to the arrow head
        # The lines are, in order: base, top diagonal, bottom diagonal (imagine arrow pointing right)
        head0_x_unrot = np.full(npts, XC.arrow_properties['l'][a] / 2)
        head0_y_unrot = np.linspace(-1 * XC.arrow_properties['head_b'][a] / 2, XC.arrow_properties['head_b'][a] / 2, npts)
        head0_x = head0_x_unrot * np.cos(XC.arrow_properties['theta'][a]) - head0_y_unrot * np.sin(XC.arrow_properties['theta'][a])
        head0_y = head0_x_unrot * np.sin(XC.arrow_properties['theta'][a]) + head0_y_unrot * np.cos(XC.arrow_properties['theta'][a])
        head0_x += XC.arrow_properties['x'][a]
        head0_y += XC.arrow_properties['y'][a]
        head1_x_unrot = np.linspace(XC.arrow_properties['l'][a] / 2, XC.arrow_properties['l'][a] / 2 + XC.arrow_properties['head_h'][a], npts)
        head1_y_unrot = np.linspace(XC.arrow_properties['head_b'][a] / 2, 0, npts)
        head1_x = head1_x_unrot * np.cos(XC.arrow_properties['theta'][a]) - head1_y_unrot * np.sin(XC.arrow_properties['theta'][a])
        head1_y = head1_x_unrot * np.sin(XC.arrow_properties['theta'][a]) + head1_y_unrot * np.cos(XC.arrow_properties['theta'][a])
        head1_x += XC.arrow_properties['x'][a]
        head1_y += XC.arrow_properties['y'][a]
        head2_x_unrot = np.linspace(XC.arrow_properties['l'][a] / 2, XC.arrow_properties['l'][a] / 2 + XC.arrow_properties['head_h'][a], npts)
        head2_y_unrot = np.linspace(-1 * XC.arrow_properties['head_b'][a] / 2, 0, npts)
        head2_x = head2_x_unrot * np.cos(XC.arrow_properties['theta'][a]) - head2_y_unrot * np.sin(XC.arrow_properties['theta'][a])
        head2_y = head2_x_unrot * np.sin(XC.arrow_properties['theta'][a]) + head2_y_unrot * np.cos(XC.arrow_properties['theta'][a])
        head2_x += XC.arrow_properties['x'][a]
        head2_y += XC.arrow_properties['y'][a]

        for arr in [box0_x, box1_x, box2_x, box3_x]:
            sort = 1
            for i in range(1, len(arr)):
                if (arr[i] >= arr[i-1]):
                    continue
                else:
                    sort = 2
                    break
            if (sort == 1):
                print('Array is forward sorted')
            else:
                for i in range(1, len(arr)):
                    if (arr[i] <= arr[i-1]):
                        continue
                    else:
                        sort = 0
                if (sort == 2):
                    print('Array is reverse sorted')
                else:
                    print('Array is not sorted')
                
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
            box_y_lo[p] = min(box0_y_int[p], box1_y_int[p], box2_y_int[p], box3_y_int[p])
            box_y_hi[p] = max(box0_y_int[p], box1_y_int[p], box2_y_int[p], box3_y_int[p])

        # Plot arrow
        ax.plot(box0_x, box0_y, '-', color=XC.NR_color, lw=3)
        ax.plot(box1_x, box1_y, '-', color=XC.NR_color, lw=3)
        ax.plot(box2_x, box2_y, '-', color=XC.NR_color, lw=3)
        ax.plot(box3_x, box3_y, '-', color=XC.NR_color, lw=3)
        ax.plot(head0_x, head0_y, '-', color=XC.NR_color, lw=3)
        ax.plot(head1_x, head1_y, '-', color=XC.NR_color, lw=3)
        ax.plot(head2_x, head2_y, '-', color=XC.NR_color, lw=3)
        ax.fill_between(box_x, box_y_lo, box_y_hi, color=XC.NR_color)
    
    im = plt.imread('Atom.png')
    newax = fig.add_axes([0.2, 0.4, 0.1, 0.1], anchor='NE', zorder=-1)
    newax.imshow(im)
    newax.axis('off')

    ax.axis('off')
    fig.tight_layout()
    fig.savefig('test.png')



def rotate(x, y, theta):
    
    xnew = x * np.cos(theta) - y * np.sin(theta)
    ynew = x * np.sin(theta) + y * np.cos(theta)
    
    return xnew, ynew



def shift(x, y, shift_x, shift_y):
    
    return (x + shift_x), (y + shift_y)