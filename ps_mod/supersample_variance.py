from cosmosis.datablock import names, option_section
import numpy as np
from scipy.integrate import simps
matter_power_nl = names.matter_power_nl


def calculate_omega_L_tophat(pk, k, kmax):
    """Calculate the variance from supersample
    TODO: Docs
    Assumes fourier spherical tophat for W
    """
    # |W(k)|^2 pk(k)
    integrand = pk * 4 * np.pi * k ** 2 / (2 * np.pi) ** 3
    # V^2_W = 4 * pi / 3 * kmax ** 3; integral |W(k)|^2
    V2W = 4 * np.pi / 3 * kmax ** 3
    # implement spherical tophat
    omega_l = simps(integrand[k <= kmax], k[k <= kmax]) / V2W
    return omega_l


def calculate_omega_L(pk, k, mode, options):
    if mode == 'fourier_tophat':
        ### FIXME: Use the z dependence in P(k) correctly
        return calculate_omega_L_tophat(pk[0, :], k, **options)
    else:
        raise Exception('No such window function defined yet!')


def sample_delta_b(pk, k, window_mode, options, num_samples=1):
    """
    Given array pk and k and max window, sample delta_b assuming spherical
    top hat
    """
    # assume fourier spherical tophat for window
    omega_l = calculate_omega_L(pk, k, window_mode, options)
    delta_b = np.random.randn(num_samples) * omega_l
    return delta_b

# We have a collection of commonly used pre-defined block section names.
# If none of the names here is relevant for your calculation you can use any
# string you want instead.
cosmo = names.cosmological_parameters

def setup(options):
    #This function is called once per processor per chain.
    #It is a chance to read any fixed options from the configuration file,
    #load any data, or do any calculations that are fixed once.

    #Use this syntax to get a single parameter from the ini file section
    #for this module.  There is no type checking here - you get whatever the user
    #put in.

    delta_b_fixed = options[option_section, "delta_b_fixed"]

    window_mode = options[option_section, "window_mode"]
    if window_mode == 'fourier_tophat':
        options = {'kmax': options[option_section, "kmax"]}

    #Now you have the input options you can do any useful preparation
    #you want.  Maybe load some data, or do a one-off calculation.
    loaded_data = (window_mode, options, delta_b_fixed)

    #Whatever you return here will be saved by the system and the function below
    #will get it back.  You could return 0 if you won't need anything.
    return loaded_data


def execute(block, config):
    """
    :param block: data block
    """

    # Just a simple rename for clarity.
    window_mode, options, delta_b_fixed = config

    pk = block[matter_power_nl, 'p_k']
    k = block[matter_power_nl, 'k_h']

    ### FIXME: delta_b should be an array for different z values
    print "delta_b_fixed is {0}".format(delta_b_fixed)
    if delta_b_fixed:
        delta_b = sample_delta_b(pk, k, window_mode, options)
        block['ssc', 'delta_b'] = delta_b
    else:
        delta_b = block['ssc', 'delta_b']

    #We tell CosmoSIS that everything went fine by returning zero
    return 0


def cleanup(config):
    # Usually python modules do not need to do anything here.
    # We just leave it in out of pedantic completeness.
    pass
