import numpy as np
import pymbar
from pymbar import timeseries

# Constants
kB = 1.381e-23 * 6.022e23 / 1000.0 # Boltzmann constant in kJ/mol/K
temperature = 300 # temperature in Kelvin
beta = 1.0 / (kB * temperature) # inverse temperature in 1/(kJ/mol)

# Parameters
K = 1  # Number of umbrella windows (for you, it's 1)
nbins = [36, 36]  # Number of bins for 2D PMF (adjust as needed)
dihedral_min = [-180.0, -180.0]  # Min values for dihedral 1 and dihedral 2
dihedral_max = [180.0, 180.0]  # Max values for dihedral 1 and dihedral 2

# Load dihedral coordinates, potential energy, and biased potential from files
# Assuming the file format contains Dihedral1, Dihedral2, PotentialEnergy, BiasedPotential
data = np.loadtxt('your_combined_data_file.dat')

chi1_kn = data[:, 0]  # Dihedral 1
chi2_kn = data[:, 1]  # Dihedral 2
potential_energy = data[:, 2]  # Total potential energy
biased_potential = data[:, 3]  # Biased potential (umbrella potential)

N_k = np.array([len(chi1_kn)])  # Number of snapshots

# Compute reduced potential energy (u_kn) without the umbrella restraint
u_kn = beta * (potential_energy - biased_potential)

# Binning the data for a 2D PMF
delta1 = (dihedral_max[0] - dihedral_min[0]) / float(nbins[0])
delta2 = (dihedral_max[1] - dihedral_min[1]) / float(nbins[1])

# Compute bin centers for 2D grid
bin_center_1 = np.linspace(dihedral_min[0] + delta1 / 2, dihedral_max[0] - delta1 / 2, nbins[0])
bin_center_2 = np.linspace(dihedral_min[1] + delta2 / 2, dihedral_max[1] - delta2 / 2, nbins[1])

# Bin the dihedral data into a 2D grid
bin_kn_1 = np.digitize(chi1_kn, np.linspace(dihedral_min[0], dihedral_max[0], nbins[0])) - 1
bin_kn_2 = np.digitize(chi2_kn, np.linspace(dihedral_min[1], dihedral_max[1], nbins[1])) - 1

# Create a single bin index combining the two dihedrals for the 2D case
bin_kn = bin_kn_1 * nbins[1] + bin_kn_2

# Set zero of u_kn (arbitrary)
u_kn -= np.min(u_kn)

# Now, set up the u_kln array
u_kln = np.zeros([K, K, N_k[0]])  # For 1 umbrella, this is just a 1x1xN array
u_kln[0, 0, :] = u_kn

# Initialize MBAR
print("Running MBAR...")
mbar = pymbar.MBAR(u_kln, N_k, verbose=True, method='adaptive')

# Compute PMF in unbiased potential (in units of kT)
(f_i, df_i) = mbar.computePMF(u_kn, bin_kn, np.prod(nbins))

# Reshape the PMF result to 2D grid
f_i_2D = f_i.reshape(nbins)
df_i_2D = df_i.reshape(nbins)

# Output the PMF for visualization or further analysis
print("PMF (in units of kT)")
for i in range(nbins[0]):
    for j in range(nbins[1]):
        print(f"{bin_center_1[i]:8.1f} {bin_center_2[j]:8.1f} {f_i_2D[i,j]:8.3f} {df_i_2D[i,j]:8.3f}")
