import nox
from laminci import move_built_docs_to_docs_slash_project_slug, upload_docs_artifact
from laminci.nox import build_docs, login_testuser1, run_pre_commit, run_pytest

nox.options.reuse_existing_virtualenvs = True


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"])
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"])
def build(session):
    session.install(".[dev,test]")
    session.install("git+https://github.com/laminlabs/lamindb")
    login_testuser1(session)
    session.run(*"lamin init --storage ./test-bionty --schema bionty".split())
    run_pytest(session)
    build_docs(session)
    upload_docs_artifact()
    move_built_docs_to_docs_slash_project_slug()
