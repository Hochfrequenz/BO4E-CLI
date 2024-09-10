"""
This module provides functions to read and write the schemas to and from a directory.
"""

from pathlib import Path

from pydantic import TypeAdapter
from rich.progress import track

from bo4e_cli.io.console import CONSOLE
from bo4e_cli.io.version_file import create_version_file, read_version_file
from bo4e_cli.models.meta import SchemaMeta, Schemas
from bo4e_cli.models.schema import SchemaRootType


def write_schemas(schemas: Schemas, output_dir: Path) -> None:
    """
    Write the schemas to the output directory.
    """
    for schema in track(schemas, description="Writing schemas...", total=len(schemas), console=CONSOLE):
        file_path = output_dir / schema.relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(schema.schema_text, encoding="utf-8")
    create_version_file(output_dir, schemas.version)


def read_schemas(input_dir: Path) -> Schemas:
    """
    Read the schemas from the input directory.
    """
    schemas = Schemas(version=read_version_file(input_dir))
    all_files = list(input_dir.rglob("*.json"))
    for schema_path in track(all_files, description="Reading schemas...", total=len(all_files), console=CONSOLE):
        relative_path = schema_path.relative_to(input_dir).with_suffix("")
        schema = SchemaMeta(name=relative_path.name, module=relative_path.parts, src=schema_path)
        schema.set_schema_text(schema_path.read_text(encoding="utf-8"))
        schemas.add(schema)
    return schemas


def read_parsed_schema(file: Path) -> SchemaRootType:
    """
    Load a parsed schema from a file.
    """
    return TypeAdapter(SchemaRootType).validate_json(file.read_text(encoding="utf-8"))
