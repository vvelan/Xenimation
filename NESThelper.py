import numpy as np
from scipy.special import erf
import DetectorConfig as DC
from NESThelper import *



### Global variables that should not be changed
DensityRef = 2.90
XeAtomNumber = 54.



def GetYieldNR(energy, dfield, density, randomIsotope=0, massNumber=0, detectorMolarMass=0):

    NuisParam = np.array([11., 1.1, 0.0480, -0.0533, 12.6, 0.3, 2., 0.3, 2., 0.5, 1., 1.])
    if (energy > 330):
        print("\nWARNING: No data out here, you are beyond the AmBe endpoint of about 300 keV.\n")
    
    ScaleFactor = np.zeros(2)
    if (randomIsotope):
        if (massNumber == 0):
            massNumber = SelectRanXeAtom()
        ScaleFactor[0] = np.sqrt(DC.DetectorMolarMass / massNumber)
        ScaleFactor[1] = ScaleFactor[0]
    else:
        ScaleFactor[0] = 1.
        ScaleFactor[1] = 1.
        
    Nq = NuisParam[0] * pow(energy, NuisParam[1])
    ThomasImel = NuisParam[2] * pow(dfield, NuisParam[3]) * pow(density / DensityRef, 0.3)
    Qy = 1. / (ThomasImel * pow(energy + NuisParam[4], NuisParam[9]))
    Qy *= 1. - 1. / pow(1. + pow((energy / NuisParam[5]), NuisParam[6]), NuisParam[10])
    Ly = Nq / energy - Qy
    
    if (Qy < 0.0):
        Qy = 0.0
    if (Ly < 0.0):
        Ly = 0.0
    
    Ne = Qy * energy * ScaleFactor[1]
    Nph = Ly * energy * ScaleFactor[0] * \
        (1. - 1. / pow(1. + pow((energy / NuisParam[7]), NuisParam[8]), NuisParam[11]))
    Nq = Nph + Ne
    Ni = (4. / ThomasImel) * (np.exp(Ne * ThomasImel / 4.) - 1.)
    Nex = (-1. / ThomasImel) * (4. * np.exp(Ne * ThomasImel / 4.) - (Ne + Nph) * ThomasImel - 4.)
    
    if (Nex <= 0.):
        print("\nCAUTION: You are approaching the border of NEST's " +
            "validity for high-energy NR, or are beyond it, at %f keV.\n" % energy)
    if (abs(Nex + Ni - Nq) > 2e-6):
        print("\nERROR: Quanta not conserved. Tell Vetri immediately!\n")
        sys.exit()
  
    NexONi = Nex / Ni
    Wq_eV, alpha = WorkFunction(density)
    L = (Nq / energy) * Wq_eV * 1e-3
    SingTripRatio = (0.21 - 0.0001 * dfield) * pow(energy, 0.21 - 0.0001 * dfield)

    return Ni, Nex, Nph, Ne, L, SingTripRatio



def GetYieldER(energy, dfield, density):

    Wq_eV, alpha = WorkFunction(density)

    QyLvllowE = 1e3 / Wq_eV + 6.5 * (1. - 1. / (1. + pow(dfield / 47.408, 1.9851)))
    HiFieldQy = 1. + 0.4607 / pow(1. + pow(dfield / 621.74, -2.2717), 53.502)
    QyLvlmedE = 32.988 - 32.988 / (1. + pow(dfield / (0.026715 * np.exp(density / 0.33926)), 0.6705))
    QyLvlmedE *= HiFieldQy;
    DokeBirks = 1652.264 + (1.415935e10 - 1652.264) / (1. + pow(dfield / 0.02673144, 1.564691))
    Nq = energy * 1e3 / Wq_eV
    LET_power = -2.
    QyLvlhighE = 28.
    if (density > 3.100):
        QyLvlhighE = 49.
    Qy = QyLvlmedE + (QyLvllowE - QyLvlmedE) / pow(1. + 1.304 * pow(energy, 2.1393), 0.35535) + \
        QyLvlhighE / (1. + DokeBirks * pow(energy, LET_power))
    if (Qy > QyLvllowE and energy > 1. and dfield > 1e4):
        Qy = QyLvllowE;
    Ly = Nq / energy - Qy;
    Ne = Qy * energy;
    Nph = Ly * energy;
    
    NexONi =  alpha * erf(0.05 * energy)
    Ni = Nq / NexONi / (1 + 1 / NexONi)
    Nex = Nq - Ni

    if (Nex <= 0.):
        print("\nCAUTION: You are approaching the border of NEST's " +
            "validity for high-energy NR, or are beyond it, at %f keV.\n" % energy)
    if (abs(Nex + Ni - Nq) > 2e-6):
        print("\nERROR: Quanta not conserved. Tell Vetri immediately!\n")
        sys.exit()

    L = 1.
    SingTripRatio = 0.20 * pow(energy, -0.45 + 0.0005 * dfield)
    
    return Ni, Nex, Nph, Ne, L, SingTripRatio



def WorkFunction(density):

    xi_se = 9. / (1. + pow(density / 2., 2.))
    alpha = 0.067366 + density * 0.039693
    I_ion = 9. + (12.13 - 9.) / (1. + pow(density / 2.953, 65.))
    I_exc = I_ion / 1.46
    Wq_eV = I_exc * (alpha / (1. + alpha)) + I_ion / (1. + alpha) + xi_se / (1. + alpha)
    eDensity = (density / DC.DetectorMolarMass) * 6.022e23 * XeAtomNumber
    Wq_eV = 20.7 - 1.01e-23 * eDensity
    
    return Wq_eV, alpha
