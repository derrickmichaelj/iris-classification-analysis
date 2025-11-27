FROM quay.io/jupyter/minimal-notebook:latest

COPY conda-lock.yml conda-lock.yml

RUN mamba update --quiet --file conda-lock.yml \
	&& mamba clean --all -y -f \
	&& fix-permissions "${CONDA_DIR}" \
	&& fix-permissions "/home/${NB_USER}"