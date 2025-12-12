FROM quay.io/jupyter/minimal-notebook:latest

USER root

# Install system dependencies
RUN apt-get update \
    && apt-get install -y make wget tar \
    && rm -rf /var/lib/apt/lists/*

# Install Quarto CLI (architecture-aware)
ARG QUARTO_VERSION=1.8.26
RUN ARCH=$(dpkg --print-architecture) \
    && if [ "$ARCH" = "amd64" ]; then \
           URL="https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.tar.gz"; \
       elif [ "$ARCH" = "arm64" ]; then \
           URL="https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-arm64.tar.gz"; \
       else \
           echo "Unsupported architecture $ARCH"; exit 1; \
       fi \
    && wget $URL -O /tmp/quarto.tar.gz \
    && mkdir -p /opt/quarto \
    && tar -xzf /tmp/quarto.tar.gz -C /opt/quarto --strip-components=1 \
    && rm /tmp/quarto.tar.gz \
    && ln -s /opt/quarto/bin/quarto /usr/local/bin/quarto

# Switch back to jovyan
USER ${NB_USER}

# Copy conda-lock file and install environment
COPY conda-lock.yml /tmp/conda-lock.yml
RUN conda install -n base -c conda-forge conda-lock -y \
    && conda-lock install --name 522_group_project_env /tmp/conda-lock.yml \
    && conda clean -afy \
    && fix-permissions "${CONDA_DIR}" \
    && fix-permissions "/home/${NB_USER}" \
    && conda run -n 522_group_project_env python -m ipykernel install --user --name 522_group_project_env --display-name "522_group_project_env"
