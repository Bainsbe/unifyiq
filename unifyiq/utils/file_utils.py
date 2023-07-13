import os
from pathlib import Path

from utils.constants import SKIP_INDEX_FILE_SUFFIX


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
    file_list = get_files_glob(path, '*.jsonl')
    filtered_list = [file for file in file_list if not skip_index_file_name(file.name)]
    return filtered_list


def get_files_glob(path, glob):
    directory = Path(path)
    return directory.glob(glob)


def skip_index_file_name(file_name):
    """Adds the skip index file suffix to the file name. These files will not be indexed."""
    return file_name + SKIP_INDEX_FILE_SUFFIX


def is_skip_index_file(file_name):
    """Checks if the file is to be skipped for index file."""
    return SKIP_INDEX_FILE_SUFFIX in file_name
