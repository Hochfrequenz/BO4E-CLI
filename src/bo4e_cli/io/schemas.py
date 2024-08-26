"""
This module provides functions to read and write the schemas to and from a directory.
"""

from pathlib import Path

from rich.progress import track

from bo4e_cli.io.version_file import create_version_file, read_version_file
from bo4e_cli.models.meta import SchemaMeta, Schemas


def write_schemas(schemas: Schemas, output_dir: Path) -> None:
    """
    Write the schemas to the output directory.
    """
    for schema in track(schemas, description="Writing schemas...", total=len(schemas)):
        file_path = output_dir / schema.relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(schema.get_schema_text(), encoding="utf-8")
    create_version_file(output_dir, schemas.version)


def read_schemas(output_dir: Path) -> Schemas:
    """
    Read the schemas from the output directory.
    """
    schemas = Schemas(version=read_version_file(output_dir))
    all_files = list(output_dir.rglob("*.json"))
    for schema_path in track(all_files, description="Reading schemas...", total=len(all_files)):
        relative_path = schema_path.relative_to(output_dir).with_suffix("")
        schema = SchemaMeta(name=schema_path.name, module=relative_path.parts)
        schema.set_schema_text(schema_path.read_text(encoding="utf-8"))
        schemas.add(schema)
    return schemas