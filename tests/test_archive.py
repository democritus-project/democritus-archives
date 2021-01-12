# -*- coding: utf-8 -*-

import os

import pytest

from democritus_archives import archive_create, archive_read, url_unarchive
from .files import file_write, file_delete
from .directories import directory_create, directory_delete

TEST_DIRECTORY_PATH = './_test_data/archive/'
TEST_DIRECTORY_BASE_PATH = './_test_data/'
DEFAULT_FILE_CONTENTS = 'abc'


# TODO: Sept, 2020 - this raises an not implemented error
def test_url_unarchive_1():
    result = url_unarchive('https://hightower.space/foo')
    assert result == ''


@pytest.fixture(autouse=True)
def clear_testing_directory():
    """This function is run after every test."""
    directory_delete(TEST_DIRECTORY_PATH)
    directory_create(TEST_DIRECTORY_PATH)


def setup_module():
    """This function is run before all of the tests in this file are run."""
    directory_create(TEST_DIRECTORY_PATH)


def teardown_module():
    """This function is run after all of the tests in this file are run."""
    directory_delete(TEST_DIRECTORY_BASE_PATH)


def _create_sample_file(path, contents=DEFAULT_FILE_CONTENTS):
    full_path = os.path.join(TEST_DIRECTORY_PATH, path)
    result = file_write(full_path, contents)
    assert result == True
    return full_path


def test_archive_read():
    file_path = _create_sample_file('a')
    output_dir = '_test_data/archive/a.zip'

    archive_create(file_path, output_dir)
    assert list(archive_read(output_dir)) == [('a', DEFAULT_FILE_CONTENTS)]
    assert list(archive_read(output_dir, archive_name='a')) == [('a', DEFAULT_FILE_CONTENTS)]


def test_archive_read_password_encrypted():
    from subprocess_wrapper import subprocess_run

    password = 'foo'

    file_path = _create_sample_file('a')
    zip_path = os.path.join(TEST_DIRECTORY_PATH, 'a.zip')
    command = f'zip -P foo {zip_path} {file_path}'
    subprocess_run(command, input_=password)

    results = list(archive_read(zip_path, password=password))
    assert results == [('_test_data/archive/a', 'abc')]
