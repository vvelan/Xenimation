from NESThelper import *
import DetectorConfig as DC
import numpy as np



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
    ThomasImel = NuisParam[2] * pow(dfield, NuisParam[3]) * pow(density / DC.DensityRef, 0.3)
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

    return Ni, Nex, Nph, Ne



def WorkFunction(density):

    xi_se = 9. / (1. + pow(density / 2., 2.))
    alpha = 0.067366 + density * 0.039693
    I_ion = 9. + (12.13 - 9.) / (1. + pow(density / 2.953, 65.))
    I_exc = I_ion / 1.46
    Wq_eV = I_exc * (alpha / (1. + alpha)) + I_ion / (1. + alpha) + xi_se / (1. + alpha)
    eDensity = (density / DC.DetectorMolarMass) * 6.022e23 * DC.XeAtomNumber
    Wq_eV = 20.7 - 1.01e-23 * eDensity
    
    return Wq_eV, alpha
    