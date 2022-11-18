"""Example how to create a `config` for a job array and submit it using cluster_jobs.py."""

import cluster_jobs
import copy

config = {
    'jobname': 'MyJob',
    'task': {
        'type': 'PythonFunctionCall',
        'module': 'tenpy',
        'function': 'run_simulation',
        'extra_imports': ['model_custom'],
    },
    'task_parameters': [],  # list of dict containing the **kwargs given to the `function`
    'requirements_slurm': {  # passed on to SLURM
        # 'memory': '4G',
        'time': '0:30:00',  # d-hh:mm:ss
        'nodes': 1,  # number of nodes
        # 'mail-user': "no@example.com",
    },
    #  'requirements_sge': {  # for SGE
    #      'l': 'h_cpu=0:30:00,h_vmem=4G',
    #      'q': 'queue',
    #      # 'M': "no@example.com"
    #  },
    'options': {  # further replacements for the job script; used to determine extra requirements
        'cores_per_task': 4,
    }
}

tenpy_sim_params = {
    'log_params': {'to_stdout': 'WARNING',
                   'to_file': 'INFO'},

    'simulation_class_name': 'GroundStateSearch',

    'directory': 'results',
    'output_filename_params': {'prefix': 'dmrg',
                               'parts': {'algorithm_params.trunc_params.chi_max': 'chi_{0:04d}',
                                         'model_params.B': 'B_{0:.1f}',
                                         'model_params.D': 'D_{0:.1f}'},
                               'suffix': '.h5'},
    'skip_if_output_exists': True,
    # 'overwrite_output': True,
    # 'save_every_x_seconds': 1800,
    # 'save_psi': False,

    'model_class': 'AnisotropicSpin1Chain',
    'model_params': {'L': 2,
                     'bc_MPS': 'infinite',
                     'J': 1.,
                     'B': 0.,
                     'D': None, # filled below
                     },

    'initial_state_params': {'method': 'lat_product_state',
                             'product_state': [['up'], ['down']]},

    'algorithm_class': 'TwoSiteDMRGEngine',
    'algorithm_params': {'trunc_params': {'chi_max': None, # filled below
                                          'svd_min': 1e-08}},

    'connect_measurements': [['tenpy.simulations.measurement',
                              'm_onsite_expectation_value',
                              {'opname': 'Sz'}],
                             ['psi_method',
                              'wrap correlation_function'
                              {'results_key': '<Sp_i Sm_j>',
                               'ops1': 'Sp',
                               'ops2': 'Sm'}],
                             ['model_custom',
                              'm_pollmann_turner_inversion']],
}


for chi in [128, 256]:
    for D in np.arange(-1., 1.5, 0.5):
        tenpy_sim_params['model_params']['D'] = D
        tenpy_sim_params['algorithm_params']['trunc_params']['chi_max'] = chi
        # instead of using the `output_filename_params`, you can also explicitly format the
        # output_filename here, if you wish:
        # tenpy_sim_params['output_filename'] = f"result_chi_{chi:d}_D_{D:.1f}.h5"
        config['task_parameters'].append(copy.deepcopy(tenpy_sim_params))

# cluster_jobs.TaskArray(**config).run_local(task_ids=[2, 3], parallel=2) # run selected tasks
cluster_jobs.JobConfig(**config).submit()  # run all tasks locally by creating a bash job script
# cluster_jobs.SlurmJob(**config).submit()  # submit to SLURM
# cluster_jobs.SGEJob(**config).submit()  # submit to SGE
