import nox
from laminci import move_built_docs_to_docs_slash_project_slug, upload_docs_artifact
from laminci.nox import build_docs, login_testuser1, run_pre_commit, run_pytest

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
def build(session: nox.Session):
    session.run(*"pip install .[dev,test]".split())
    session.run(*"pip install git+https://github.com/laminlabs/lamindb".split())
    login_testuser1(session)
    session.run(*"lamin init --storage ./test-bionty --schema bionty".split())
    run_pytest(session)
    build_docs(session)
    upload_docs_artifact()
    move_built_docs_to_docs_slash_project_slug()
