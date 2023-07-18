import nox
from laminci.nox import login_testuser1, run_pre_commit, run_pytest

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
def install(session: nox.Session):
    session.run(*"pip install .[dev,test]".split())


@nox.session
def build(session: nox.Session):
    login_testuser1(session)
    run_pytest(session, coverage=False)
