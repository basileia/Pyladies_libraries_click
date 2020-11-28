from pathlib import Path
from collections import defaultdict
import click
import json


@click.command()
@click.option("--folder-path", "-p", required="true",
              type=click.Path(exists=True),
              help="Path to the folder.")
@click.option("--convert", "-c", is_flag="True",
              help="Use it if you want unit conversion.")
@click.option("--want-json", "-j", is_flag="True",
              help="Adds statistics to json file")
def file_size_statistics(folder_path, convert, want_json):
    """
    Returns file size statistics
    """
    path = Path(folder_path)
    files_info = get_files_info(path)  # in bytes
    result = group_by_suffixes(files_info)
    if convert:
        result = convert_size(dict(result))
    click.echo(result)
    if want_json:
        create_json(result)
        click.echo("Output in json file")


def get_files_info(folderPath):
    """
    Returns list of tuples - file suffix or empty string and its size -
    information about the files that are in the folder
    """
    files_info = []
    for file in folderPath.iterdir():

        if file.is_file():
            suffix = file.suffix
            files_info.append((suffix, Path(file).stat().st_size))
        else:
            files_info.extend(get_files_info(file))
    return files_info


def group_by_suffixes(files_info):
    """
    Returns tuples grouped by suffixes (suffix, sum of file sizes)
    """
    dictionary = defaultdict(int)
    for suffix, size in files_info:
        dictionary[suffix] = dictionary[suffix] + size
    tuples = (list(dictionary.items()))
    return tuples


def convert_size(size_bytes_in_dict):
    """
    Converts size from bytes to more human readable. Input and output is
    dictionary.
    """
    unit_list = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")
    i = 0
    for suffix in size_bytes_in_dict:
        while size_bytes_in_dict[suffix] >= 1024 and i < len(unit_list) - 1:
            size_bytes_in_dict[suffix] /= 1024.
            i += 1
        f = ('%.2f' % size_bytes_in_dict[suffix]).rstrip('0').rstrip('.')
        size_bytes_in_dict[suffix] = '%s %s' % (f, unit_list[i])
        i = 0
    return size_bytes_in_dict


def create_json(data):
    """
    Creates json file with data
    """
    with open("file_size_statistics.txt", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    file_size_statistics()
