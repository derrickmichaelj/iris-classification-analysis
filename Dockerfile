FROM quay.io/jupyter/minimal-notebook:latest

COPY conda-lock.yml /tmp/conda-lock.yml

RUN mamba install -n base conda-lock -c conda-forge

RUN conda-lock install --mamba --name myenv /tmp/conda-lock.yml \
    && mamba clean --all -y -f \
    && fix-permissions "${CONDA_DIR}" \
    && fix-permissions "/home/${NB_USER}"

RUN mamba run -n myenv python -m ipykernel install \
    --name "myenv" --display-name "Python (myenv)"

CMD ["bash", "-c", "mamba run -n myenv jupyter lab --ip=0.0.0.0 --no-browser --ServerApp.token=''"]