# amberdata

## Poetry

We assume you share already the love for [Poetry](https://python-poetry.org). Once you have installed poetry you can perform

```bash
make install
```

to replicate the virtual environment we have defined in pyproject.toml.

## Kernel

We install [JupyterLab](https://jupyter.org) within your new virtual environment. Executing

```bash
make kernel
```

constructs a dedicated [Kernel](https://docs.jupyter.org/en/latest/projects/kernels.html) for the project.
