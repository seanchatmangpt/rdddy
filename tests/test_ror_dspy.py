
import pytest
from typer.testing import CliRunner
from experiments.ror_dspy import app
runner = CliRunner()


def test_new():
    result = runner.invoke(app, ["new"])
    assert result.exit_code == 0
    assert "This is the new command." in result.output  # Replace with specific expected output


def test_generate():
    result = runner.invoke(app, ["generate"])
    assert result.exit_code == 0
    assert "This is the generate command." in result.output  # Replace with specific expected output


def test_server():
    result = runner.invoke(app, ["server"])
    assert result.exit_code == 0
    assert "This is the server command." in result.output  # Replace with specific expected output


def test_test():
    result = runner.invoke(app, ["test"])
    assert result.exit_code == 0
    assert "This is the test command." in result.output  # Replace with specific expected output


def test_deploy():
    result = runner.invoke(app, ["deploy"])
    assert result.exit_code == 0
    assert "This is the deploy command." in result.output  # Replace with specific expected output


def test_db():
    result = runner.invoke(app, ["db"])
    assert result.exit_code == 0
    assert "This is the db command." in result.output  # Replace with specific expected output


def test_data():
    result = runner.invoke(app, ["data"])
    assert result.exit_code == 0
    assert "This is the data command." in result.output  # Replace with specific expected output


def test_eval():
    result = runner.invoke(app, ["eval"])
    assert result.exit_code == 0
    assert "This is the eval command." in result.output  # Replace with specific expected output


def test_help():
    result = runner.invoke(app, ["help"])
    assert result.exit_code == 0
    assert "This is the help command." in result.output  # Replace with specific expected output


