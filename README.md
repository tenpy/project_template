# My awesome project using TeNPy

## Initial setup to get started

This is a small template repository to simplify setting up projects that use TeNPy.
To get started:

- [ ] Visit https://github.com/tenpy/project_template/ and click on the big green 
	"Use this template" button to create a custom fork of the repository.
	You can keep that fork private, if you want to!
- [ ] `git clone` your new fork repository onto your computer/on the cluster.
   After the `git clone`, call `git submodule init` and `git submodule update`
   to download TeNPy.
- [ ] Setup your Python environment, e.g. `module load python/3.8` on a cluster or
	`conda activate custom_env` to activate a conda environment.
	You might find it usefull to set up a custom module based on the provided `module_example`.
	Adjust the files in `cluster_templates/*.sh` to set correct paths/load the modules etc, as needed.
- [ ] Once you have the correct Python environment loaded, `cd TeNPy/` and `bash ./compile.sh` to compile TeNPy.

## Implement custom models and other classes

There's a `model_custom.py` which serves as an example how to implement a new model class;
you can add further classes (structured in other python modules, if desired), as much as you like!

## Submitting a job / running simulations

- Activate your python environment.
- Create a subfolder where you want to have the output files and `cd` there.
- Create a yaml file with the simulation parameters, for example the `example_submit.yml`.
  (You can also have multiple yaml files, which then get "merged" together; this allows to have a "default_parameters.yml" file which is always the same, 
  and a "changing_parameters.yml" which contains what you changed compared to previous runs...)
- Call `cluster_jobs.py submit example_submit.yml`.
  This will create a job script (e.g. `MyJob.slurm.sh`) and job config (`MyJob.config.yml`) containing all the parameters which you just submitted.
  Finally, it will submit that job to the cluster (if you use the `SlurmJob` or `SGEJob` for `job_config.class` in the yaml file) 
  or directly run everything (if you use `JobConfig` instead).
  The examples are set up such that you only see warnings/errors in the terminal output (or `MyJob.job*.out` on a cluster), but you get the lengthy log files with the same name as the output files (also containing error messages/warnings).
- You can immediately update the `example_submit.yml` after job submission and submit slightly different parameters as a separate job, if desired.

## Profit!!!

Do some awesome science and write a great paper about it :)
