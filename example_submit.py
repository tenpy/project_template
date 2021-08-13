"""Example how to create a `config` for a job array and submit it using cluster_jobs.py."""

import cluster_jobs
import copy

config = {
    'jobname': 'MyJob',
    'task': {
        'type': 'PythonFunctionCall',
        'module': 'tenpy',
        'function': 'run_simulation',
        'extra_imports': ['custom_model'],
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
        # 'mail': 'no@example.com',
        'cores_per_task': 4,
    }
}

tenpy_sim_params = {
    'log_params': {'to_stdout': 'WARNING',
                   'to_file': 'INFO'},

    'simulation_class_name': 'GroundStateSearch',

    'model_class': 'AlternatingHeisenbergChain',
    'model_params': {'J1': 1.0,
                     'J2': None, # filled below
                     'L': 32,
                     'bc_MPS': 'finite'},

    'initial_state_params': {'method': 'lat_product_state',
                             'product_state': [['up'], ['down']]},

    'algorithm_class': 'TwoSiteDMRGEngine',
    'algorithm_params': {'trunc_params': {'chi_max': None, # filled below
                                          'svd_min': 1e-08}},
}


for chi in [128, 256]:
    for J2 in [0.25, 0.5, 0.75]:
        tenpy_sim_params['model_params']['J2'] = J2
        tenpy_sim_params['algorithm_params']['trunc_params']['chi_max'] = chi
        tenpy_sim_params['output_filename'] = f"result_chi_{chi:d}_J2_{J2:.2f}.h5"
        config['task_parameters'].append(copy.deepcopy(tenpy_sim_params))

# cluster_jobs.TaskArray(**config).run_local(task_ids=[2, 3], parallel=2) # run selected tasks
cluster_jobs.JobConfig(**config).submit()  # run all tasks locally by creating a bash job script
# cluster_jobs.SlurmJob(**config).submit()  # submit to SLURM
# cluster_jobs.SGEJob(**config).submit()  # submit to SGE
