"""
LSST-DESC hack
"""
from __future__ import division
from cosmosis.datablock import names, option_section
mass_function = names.mass_function


def n(n_mean, x, z, b, delta_b):
    """ eqn (3) of Lima and Hu
    """
    return n_mean * (1. + b * delta_b)


def N_mean(M, m_h, x, z, b, delta_b):
    """ work with mass function and halo bias to compute the average number of
    clusters with mass above a certain threshold

    :param M: float,
        we are integrating all the number density above this mass threshold
    :param m_h: numpy array of floats
        which is the maks
    :param x: numpy array
        shape = (obs, 3) particular location?
    :param z: float, redshift
    :param b: bias term which depends on mass and z
    :param delta_b: some term from Chris' term
    """
    return 0


def setup(options):
    """ debug outputs from mf_pressschechter function """
    return 0


def execute(block, config):
    # load all the data for the calculation
    delta_b = block["ssc", "delta_b"]

    # get data outputted from mf_pressschector
    # right now m_h is missing ...
    # k_h = block["mass_function", "k_h"]
    if block.has_value(mass_function, "m_h"):
        m_h = block[mass_function, "m_h"]
    else:
        # the entry m_h is missing even though
        block.save_to_directory("./debug_data/")

    # n_mean = block["mass_function", "dndlnmh"] / m_h
    r_h = block[mass_function, "r_h"]

    # N_mean = N_mean(m, x, z, r_h, b, delta_b)
    # block["ssc", "N_mean"] = N_mean()

    return 0


def cleanup(config):
    pass

