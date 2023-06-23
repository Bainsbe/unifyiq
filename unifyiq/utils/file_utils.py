import os
from pathlib import Path


def get_output_path_from_config(config, version):
    """Returns the output path from the config and version."""
    return f"{config.dest_path}/unifyiq/{config.name}/{version}"


def get_fetcher_output_path_from_config(config, version):
    """Returns the fetcher output path from the config and version."""
    output_path = f"{get_output_path_from_config(config, version)}/fetchers"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    return output_path


def get_core_output_path_from_config(config, version):
    """Returns the core output path from the config and version."""
    output_path = f"{get_output_path_from_config(config, version)}/core"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    return output_path


def get_jsonl_files(path):
    return get_files_glob(path, '*.jsonl')


def get_files_glob(path, glob):
    directory = Path(path)
    return directory.glob(glob)
