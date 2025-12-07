FROM quay.io/jupyter/minimal-notebook:latest

USER root

# Install OS-level dependency
RUN apt-get update \
    && apt-get install -y make \
    && rm -rf /var/lib/apt/lists/*

USER ${NB_USER}

# Copy the conda-lock file (make sure it’s the correct platform)
COPY conda-linux-64.lock /tmp/conda-lock.yml

# Install mamba in base (needed for conda-lock)
RUN conda install mamba -n base -c conda-forge -y

# Create the environment from the lock file
RUN conda-lock install --name 522_group_project_env /tmp/conda-lock.yml \
    && conda clean -afy \
    && fix-permissions "${CONDA_DIR}" \
    && fix-permissions "/home/${NB_USER}"

# Make the environment default for all subsequent commands
SHELL ["conda", "run", "-n", "522_group_project_env", "/bin/bash", "-c"]

# Copy your project
COPY . /home/jovyan/work
WORKDIR /home/jovyan/work
