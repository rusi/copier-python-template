from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def copier_project_defaults():
    return {
        "package_name": "test_package",
        "version": "0.1.0",
        "full_name": "Jane Smith",
        "copyright_holder": "Jane Smith",
        "package_short_description": "test package short description",
        "github_organization": "rusi",
        "email": "jsmith@example.com",
    }


def check_template_resolved(project_file: Path, expected_lines: list[str]):
    assert project_file.exists()
    content = project_file.read_text()
    for line in expected_lines:
        assert line in content, f"{project_file} should contain '{line}'"


def test_project_folder(copie, copier_project_defaults):
    project_defaults = copier_project_defaults
    project = copie.copy(extra_answers=project_defaults)

    assert project.exit_code == 0
    assert project.exception is None
    assert project.project_dir.is_dir()

    assert (project.project_dir / ".vscode" / "test_package.code-snippets").exists()

    check_template_resolved(
        project.project_dir / "README.md",
        ["# test_package", "test package short description"],
    )
    check_template_resolved(
        project.project_dir / "pyproject.toml",
        [
            'name = "test_package"',
            'description = "test package short description"',
            'version = "0.1.0"',
            'authors = ["Jane Smith <jsmith@example.com>"]',
        ],
    )
    check_template_resolved(
        project.project_dir / ".vscode" / "test_package.code-snippets",
        [
            "// Place your test_package workspace snippet",
            "Copyright (c) 2024 Jane Smith",
            "Insert test_package copyright block",
        ],
    )
    check_template_resolved(
        project.project_dir / ".vscode" / "launch.json",
        ['"name": "Python: test_package"'],
    )
