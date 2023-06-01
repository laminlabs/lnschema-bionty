# from pathlib import Path

# from lndb._migrate import generate_module_files
# from lndb.test import (
#     get_package_name,
#     migrate_clones,
#     migration_id_is_consistent,
#     model_definitions_match_ddl,
# )

# from lnschema_bionty import _schema_id as schema_id

# package_name = get_package_name()
# migrations_path = Path(__file__).parent.parent / package_name / "migrations"


# def test_migration_id_is_consistent():
#     assert migration_id_is_consistent(package_name)


# def test_model_definitions_match_ddl_postgres():
#     generate_module_files(package_name=package_name, migrations_path=migrations_path, schema_id=schema_id)
#     model_definitions_match_ddl(package_name, dialect_name="postgresql")


# def test_migrate_clones_sqlite():
#     results = migrate_clones(package_name, n_instances=1, dialect_name="sqlite")
#     if "migrate-failed" in results:
#         raise RuntimeError("Migration e2e test failed.")


# def test_migrate_clones_postgres():
#     results = migrate_clones(package_name, n_instances=1, dialect_name="postgresql")
#     if "migrate-failed" in results:
#         raise RuntimeError("Migration e2e test failed.")
