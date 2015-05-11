import numpy as np
from cosmosis.datablock import names as section_names
from cosmosis.datablock import option_section
from scipy.integrate import quad
from scipy.interpolate import InterpolatedUnivariateSpline

cosmo = section_names.cosmological_parameters

k_hubble_scaling = 2.99792458e+05 ### From cosmosis/postprocessing/cosmology_theory_plots.py

def setup(options):
	Mth = options[option_section, "Mth"]
	survey_area_sq_deg = options[option_section, "survey_area_sq_deg"]
	survey_area_steradians = survey_area_sq_deg * (np.pi/180.) ** 2
	return Mth, survey_area_steradians

def execute(block, config):
	Mth, survey_area_steradians = config

	### Parameters describing the tomographic redshift bins
	zmin = block['tomography', 'z_bin_min']
	zmax = block['tomography', 'z_bin_max']
	z = block['tomography', 'z_bin_means']

	### Volumes of each tomographic bin
	### TODO: Move volumes calculation to a 'tomography' module because needed for other modules.
	z_d = block["distances", "z"][::-1] 	### Redshifts
	d = block["distances", "d_m"][::-1] ### Comoving distance h^(-1)Mpc
	h0 = block[cosmo, "h0"]
	h = block["distances", "h"][::-1] * k_hubble_scaling / h0 ### H(z)/c (h^(-1) Mpc)^(-1)
	volumes = np.array([InterpolatedUnivariateSpline(z_d, d**2 /h).integral(zmin[i], zmax[i])
		for i in xrange()]) * survey_area_steradians

	### Load the mass function
	r_h, z_mf, dndlnRh = get_grid(section_names.mass_function, 'r_h', 'z', 'dndlnrh')
	dndlnm = dndlnRh / 3.
	nz_mf = len(z_mf)
	### Get the halo bias as a grid in M and z
	b_h = get_double_array_nd(section_names.mass_function, 'b_h')

	### Mh := (4 pi / 3) rho_m Rh^3
	###   from the mass_function module: rho_m = 2.775e11 (omega_matter h^2) M_sun Mpc^-3
	omega_m = block[cosmo, 'omega_m']	
	lnm_h = 3. * np.log(r_h) + np.log(omega_m) + 27.7815

	### Check if Mth(z) is present in the data block and discard the config value if so.
	try:
		Mth_z = get_double_array_1d("cluster_counts", "Mth")
		z_mth = get_double_array_1d("cluster_counts", "z_Mth")
		lnMth = InterpolatedUnivariateSpline(z_mth, np.log(Mth_z))(z_mf)
	except:
		lnMth = np.ones(nz_mf, dtype=float) * np.log(Mth)
	if np.min(lnMth) < np.min(lnm_h):
		raise ValueError("Threshold mass in cluster_counts must be larger than minimum mass in the mass_function.")

	### Load the delta_b parameters
	delta_b = block['ssc', 'delta_b']

	### Compute the cluster counts
	### First, integrate the mass function and the halo bias times the mass function over the
	### chosen halo mass range.
	### Then, re-weight with the delta_b values for each tomographic bin.

	### Integral of the mass function over halo mass range for each z
	Imass = [InterpolatedUnivariateSpline(lnm_h, dndlnm[:, iz]).integral(
			lnMth[iz], lnM_max)
		for iz in xrange(nz_mf)]
	Imass_spl = InterpolatedUnivariateSpline(z_mf, Imass)
	### Integral of the halo bias times the mass function over halo mass for each z
	Ihalos = [InterpolatedUnivariateSpline(lnm_h, dndlnm[:, iz] * b_h[:, iz]).integral(
			lnMth[iz], lnM_max)
		for iz in xrange(nz_mf)]
	Ihalos_spl = InterpolatedUnivariateSpline(z_mf, Ihalos)
	### The cluster counts are a linear combination of the 2 preceding integrals, weighted by the
	### delta_b values for each tomographic bin.
	###
	### This gives number of clusters per unit volume. 
	### Need to multiply by the volume of each tomographic bin, assuming we can neglect the 
	### evolution in the mass function and halo bias over the width of each bin.
	counts = np.array([Imass_spl(z[i]) + bh * Ihalos_spl(z[i]) for i, bh in enumerate(delta_b)])

	### Save cluster counts to the data block
	block["cluster_counts", "z"] = z ### Same as SSC block z values, copied here for convenience
	block["cluster_counts", "counts"] = counts * volumes

	return 0

def cleanup(config):
	pass


