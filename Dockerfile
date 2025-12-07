FROM quay.io/jupyter/minimal-notebook:latest

USER root
RUN apt-get update \
    && apt-get install -y make \
    && rm -rf /var/lib/apt/lists/*

USER ${NB_USER}

# Copy lock file and install conda-lock
COPY conda-lock.yml /tmp/conda-lock.yml
RUN conda install -n base -c conda-forge conda-lock -y \
    && conda-lock install --name 522_group_project_env /tmp/conda-lock.yml \
    && conda clean -afy \
    && fix-permissions "${CONDA_DIR}" \
    && fix-permissions "/home/${NB_USER}"

