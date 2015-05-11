# from numpy import log, pi
from cosmosis.datablock import names as section_names
# from cosmosis.datablock import option_section
cosmo = section_names.cosmological_parameters
matter_power_nl = section_names.matter_power_nl


def dP_d_delta(ps, k):
    """take derivative of P(k) with respect to delta_b
    equation 39 in takada and hu
    """
    return 68. / 21.


def setup(options):
    return 0


def execute(block, config):
    # FIXME: Use the z dependence in P(k) correctly
    print "name of section matter_power_nl is {0}".format(matter_power_nl)
    PS = block[matter_power_nl, 'p_k']
    k = block[matter_power_nl, 'k_h']
    delta_b = block['ssc', 'delta_b']
    dPd_delta = dP_d_delta(PS[0, :], k)
    ps_mod = PS * (1 + dPd_delta * delta_b)
    print 'ps_mode scaling factor: ', dPd_delta * delta_b
    block['ssc', 'ps_mod'] = ps_mod
    block['ssc', 'k'] = k
    block[matter_power_nl, 'p_k'] = ps_mod
    return 0


def cleanup(config):
    return 0
