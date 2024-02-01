import pytest
from typer.testing import CliRunner
from metadspy.cli import app  # Updated import statement

runner = CliRunner()


def test_generate_module():
    result = runner.invoke(app, ["generate_module"])
    assert result.exit_code == 0
    assert (
        "This is the generate_module command." in result.output
    )  # Replace with specific expected output


def test_generate_signature():
    result = runner.invoke(app, ["generate_signature"])
    assert result.exit_code == 0
    assert (
        "This is the generate_signature command." in result.output
    )  # Replace with specific expected output


def test_generate_chainofthought():
    result = runner.invoke(app, ["generate_chainofthought"])
    assert result.exit_code == 0
    assert (
        "This is the generate_chainofthought command." in result.output
    )  # Replace with specific expected output


def test_generate_retrieve():
    result = runner.invoke(app, ["generate_retrieve"])
    assert result.exit_code == 0
    assert (
        "This is the generate_retrieve command." in result.output
    )  # Replace with specific expected output


def test_generate_teleprompter():
    result = runner.invoke(app, ["generate_teleprompter"])
    assert result.exit_code == 0
    assert (
        "This is the generate_teleprompter command." in result.output
    )  # Replace with specific expected output


def test_generate_example():
    result = runner.invoke(app, ["generate_example"])
    assert result.exit_code == 0
    assert (
        "This is the generate_example command." in result.output
    )  # Replace with specific expected output


def test_generate_assertion():
    result = runner.invoke(app, ["generate_assertion"])
    assert result.exit_code == 0
    assert (
        "This is the generate_assertion command." in result.output
    )  # Replace with specific expected output
