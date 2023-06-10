import nox
from laminci.nox import build_docs, run_pre_commit, run_pytest

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
def install(session: nox.Session):
    session.run(*"pip install .[dev,test]".split())
    session.run(*"pip install lamindb".split())


@nox.session
def build(session: nox.Session):
    run_pytest(session)
    build_docs(session)
