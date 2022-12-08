import nox
from lndb_setup.test.nox import (
    build_docs,
    install_and_run_pytest,
    login_testuser1,
    run_pre_commit,
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
    install_and_run_pytest(session)
    build_docs(session)
