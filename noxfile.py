import os

import nox
from lndb_setup._clone import setup_local_test_postgres
from lndb_setup.test._nox import get_schema_handle
from lndb_setup.test.nox import (  # setup_test_instances_from_main_branch,
    build_docs,
    install_and_run_pytest,
    login_testuser1,
    run_pre_commit,
)

nox.options.reuse_existing_virtualenvs = True


def setup_test_instances_from_main_branch(session):
    session.install("lndb_setup")
    # spin up a postgres test instance
    pgurl = setup_local_test_postgres()
    # switch to the main branch
    if "GITHUB_BASE_REF" in os.environ and os.environ["GITHUB_BASE_REF"] != "":
        session.run("git", "checkout", os.environ["GITHUB_BASE_REF"], external=True)
    session.install(".[test]")  # install current package from main branch
    # init a postgres instance
    init_instance = f"lndb init --storage pgtest --db {pgurl}"
    schema_handle = get_schema_handle()
    if schema_handle not in {None, "core"}:
        init_instance += f" --schema {schema_handle}"
    session.run(*init_instance.split(" "), external=True)
    # go back to the PR branch
    if "GITHUB_HEAD_REF" in os.environ and os.environ["GITHUB_HEAD_REF"] != "":
        session.run("git", "checkout", os.environ["GITHUB_HEAD_REF"], external=True)


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"])
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"])
def build(session):
    login_testuser1(session)
    setup_test_instances_from_main_branch(session)
    install_and_run_pytest(session)
    build_docs(session)
