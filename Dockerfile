FROM quay.io/jupyter/minimal-notebook:latest

USER root

# Install make, wget, gdebi-core (for Quarto)
RUN apt-get update \
    && apt-get install -y make wget gdebi-core \
    && wget https://quarto.org/download/latest/quarto-linux-arm64.deb -O /tmp/quarto.deb \
    && gdebi -n /tmp/quarto.deb \
    && rm /tmp/quarto.deb \
    && rm -rf /var/lib/apt/lists/*

# Copy conda-lock.yml and install environment
COPY conda-lock.yml /tmp/conda-lock.yml
RUN conda install -n base -c conda-forge conda-lock -y \
    && conda-lock install --name 522_group_project_env /tmp/conda-lock.yml \
    && conda clean -afy \
    && /opt/conda/envs/522_group_project_env/bin/python -m ipykernel install \
         --prefix=/opt/conda \
         --name 522_group_project_env \
         --display-name "Python (522_group_project_env)" \
    && fix-permissions "/opt/conda"

# Switch back to jovyan
USER ${NB_USER}

# Pre-create cache directories in /tmp (writable)
RUN mkdir -p /tmp/.cache/matplotlib /tmp/.cache/quarto /tmp/.cache/deno

# Set environment variables for caches
ENV MPLCONFIGDIR=/tmp/.cache/matplotlib
ENV QUARTO_CACHE_DIR=/tmp/.cache/quarto
ENV DENO_DIR=/tmp/.cache/deno
