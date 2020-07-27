import numpy as np
from scipy.special import erf
import DetectorConfig as DC
from NESThelper import *



### Global variables that should not be changed
DensityRef = 2.90
XeAtomNumber = 54.



### Get the yields for the NEST NR model.
### Args:    total recoil energy in keV, drift field in V/cm, liquid xenon density in g/cm3,
###          boolean variable deciding whether to draw a specific atomic isotope,
###          atomic mass number to be used if specificIsotope = True (if massNumber = 0, draws a random isotope)
### Returns: number of ions produced, number of excitons produced, number of photons
###          leaving the recoil site, number of electrons leaving the recoil site,
###          Lindhard factor, singlet-to-triplet ratio
### NOTE: This function is deprecated. It remains in the code for backwards compatibility,
### but Xenimation now uses NESTpy to get the ER and NR yields. NESTpy allows changes in the NEST model
### to be propagated into Xenimation.
### NOTE: the Xenimation GetYieldNR() function might not exactly match output from NESTpy,
### because the C++ code randomly draws an atomic isotope to calculate the yields, and the
### NESTpy bindings propagate this stochasticity.

def GetYieldNR(energy, dfield, density, specificIsotope=0, massNumber=0):

    NuisParam = np.array([11., 1.1, 0.0480, -0.0533, 12.6, 0.3, 2., 0.3, 2., 0.5, 1., 1.])
    if (energy > 330):
        print("\nWARNING: No data out here, you are beyond the AmBe endpoint of about 300 keV.\n")
    
    ScaleFactor = np.zeros(2)
    if (specificIsotope):
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



### Get the yields for the NEST beta model.
### Args:    total recoil energy in keV, drift field in V/cm, liquid xenon density in g/cm3,
### Returns: number of ions produced, number of excitons produced, number of photons
###          leaving the recoil site, number of electrons leaving the recoil site,
###          Lindhard factor, singlet-to-triplet ratio
### NOTE: This function is deprecated. It remains in the code for backwards compatibility,
### but Xenimation now uses NESTpy to get the ER and NR yields. NESTpy allows changes in the NEST model
### to be propagated into Xenimation.
### NOTE: This function was originally called GetYieldER(). If you are using older code, you may
### have to rename the function calls.

def GetYieldBeta(energy, dfield, density):

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



### Get the yields for the NEST gamma model.
### Args:    total recoil energy in keV, drift field in V/cm, liquid xenon density in g/cm3,
### Returns: number of ions produced, number of excitons produced, number of photons
###          leaving the recoil site, number of electrons leaving the recoil site,
###          Lindhard factor, singlet-to-triplet ratio
### NOTE: This function is deprecated. It remains in the code for backwards compatibility,
### but Xenimation now uses NESTpy to get the ER and NR yields. NESTpy allows changes in the NEST model
### to be propagated into Xenimation.
### NOTE: This function was originally called GetYieldER(). If you are using older code, you may
### have to rename the function calls.

def GetYieldGamma(energy, dfield, density):
    
    Wq_eV, alpha = WorkFunction(density)
    
    m1 = 33.951 + (3.3284 - 33.951) / (1. + pow(dfield / 165.34, 0.72665))
    m2 = 1000. / Wq_eV
    m3 = 2.
    m4 = 2.
    m5 = 23.156 + (10.737 - 23.156) / (1. + pow(dfield / 34.195, 0.87459))
    m6 = 0.
    densCorr = 240720. / pow(density, 8.2076)
    m7 = 66.825 + (829.25 - 66.825) / (1. + pow(dfield / densCorr, 0.83344))
    m8 = 2.

    Nq = energy * 1000. / Wq_eV
    Qy = m1 + (m2 - m1) / (1. + pow(energy / m3, m4)) + m5 + (m6 - m5) / (1. + pow(energy / m7, m8))
    Ly = Nq / energy - Qy
    Ne = Qy * energy
    Nph = Ly * energy
    
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



### Get the work function for liquid xenon.
### Args:    liquid xenon density in g/cm3
### Returns: W-value in eV, alpha (used for calculating Nex/Ni for ER's)
### NOTE: This function is deprecated. It remains in the code for backwards compatibility,
### but Xenimation now uses NESTpy to get the ER and NR yields. NESTpy allows changes in the NEST model
### to be propagated into Xenimation.

def WorkFunction(density):

    xi_se = 9. / (1. + pow(density / 2., 2.))
    alpha = 0.067366 + density * 0.039693
    I_ion = 9. + (12.13 - 9.) / (1. + pow(density / 2.953, 65.))
    I_exc = I_ion / 1.46
    Wq_eV = I_exc * (alpha / (1. + alpha)) + I_ion / (1. + alpha) + xi_se / (1. + alpha)
    eDensity = (density / DC.DetectorMolarMass) * 6.022e23 * XeAtomNumber
    Wq_eV = 20.7 - 1.01e-23 * eDensity
    
    return Wq_eV, alpha
