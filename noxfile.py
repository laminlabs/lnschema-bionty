import nox
import requests  # type: ignore
from laminci import move_built_docs_to_docs_slash_project_slug, upload_docs_dir
from laminci.nox import (
    build_docs,
    login_testuser1,
    run_pre_commit,
    run_pytest,
    setup_test_instances_from_main_branch,
)

nox.options.reuse_existing_virtualenvs = True


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"])
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"])
def build(session):
    login_testuser1(session)
    setup_test_instances_from_main_branch(session)
    session.install(".[dev,test]")
    response = requests.get("https://github.com/laminlabs/lamindb/tree/staging")
    if response.status_code < 400:
        session.install("git+https://github.com/laminlabs/lamindb@staging")
    else:
        session.install("git+https://github.com/laminlabs/lamindb")
    run_pytest(session)
    build_docs(session)
    upload_docs_dir()
    move_built_docs_to_docs_slash_project_slug()
