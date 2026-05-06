# ============================================================
# PyBatGym Docker Image
# Python runtime with pre-installed libraries (PyTorch, SB3)
# ============================================================

FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && apt-get install -y \
    python3 python3-pip python3-venv \
    libboost-all-dev libzmq3-dev libczmq-dev \
    git curl \
    && rm -rf /var/lib/apt/lists/*



# Create Python venv
RUN python3 -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH
ENV VIRTUAL_ENV=/opt/venv

# Install Python dependencies (cached layer — runs BEFORE copying code)
WORKDIR /workspace
COPY pyproject.toml ./
COPY pybatgym/__init__.py ./pybatgym/__init__.py

RUN pip install --upgrade pip setuptools wheel && \
    pip install -e . && \
    pip install stable-baselines3 sb3-contrib tensorboard pytest pybatsim

# Copy full project (changes more often → last layer)
COPY . .
RUN pip install -e . --no-build-isolation

# Startup environment check
RUN python3 -c "import pybatgym; print('✅ pybatgym OK')" && \
    python3 -c "import stable_baselines3; print('✅ SB3 OK')" && \
    echo "✅ Environment OK"

WORKDIR /workspace

# Default: open bash (override with docker-compose command)
CMD ["bash"]
