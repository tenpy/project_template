"""This file serves as an example how to extend TeNPy with custom classes.

Here, we add an extra model, but you can also implement other custom classes like a Lattice, Site
or Simulation class.
"""

import numpy as np

import tenpy
from tenpy.models.spins import SpinChain


class AlternatingHeisenbergChain(SpinChain):
    """Extension of the SpinChain"""

    def init_terms(self, model_params):
        J1 = model_params.get('J1', 1.)
        J2 = model_params.get('J2', 0.5)

        N_couplings = self.lat.Ls[0] - (self.lat.boundary_conditions[0] == 'open')
        J = ([J1, J2] * N_couplings)[:N_couplings]
        J = np.array(J)
        model_params['Jx'] = J
        model_params['Jy'] = J
        model_params['Jz'] = J
        model_params.touch('Jx', 'Jy', 'Jz')
        super().init_terms(model_params)

