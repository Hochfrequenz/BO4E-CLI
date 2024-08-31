from pathlib import Path

from typer.testing import CliRunner

from bo4e_cli import app
from bo4e_cli.models.meta import SchemaMeta


class TestPull:
    """
    A class with pytest unit tests.
    """

    def test_latest(self, tmp_path: Path, mock_github: None) -> None:
        result = CliRunner().invoke(app, ["pull", "-o", str(tmp_path), "--no-update-refs"])
        assert result.exit_code == 0

        version_file = tmp_path / ".version"
        angebot_schema = tmp_path / "bo/Angebot.json"
        assert version_file.exists()
        assert version_file.read_text() == "v202401.4.0"
        assert angebot_schema.exists()
        angebot = SchemaMeta(name="Angebot", module=("bo", "Angebot"), src=angebot_schema)
        angebot.set_schema_text(angebot_schema.read_text())
        assert angebot.get_schema_parsed().title == "Angebot"

    def test_excplicit_version(self, tmp_path: Path, mock_github: None) -> None:
        result = CliRunner().invoke(app, ["pull", "-o", str(tmp_path), "--no-update-refs", "-t", "v202401.4.0"])
        assert result.exit_code == 0

        version_file = tmp_path / ".version"
        angebot_schema = tmp_path / "bo/Angebot.json"
        assert version_file.exists()
        assert version_file.read_text() == "v202401.4.0"
        assert angebot_schema.exists()
        angebot = SchemaMeta(name="Angebot", module=("bo", "Angebot"), src=angebot_schema)
        angebot.set_schema_text(angebot_schema.read_text())
        assert angebot.get_schema_parsed().title == "Angebot"

    def test_update_refs(self, tmp_path: Path, mock_github: None) -> None:
        result = CliRunner().invoke(app, ["pull", "-o", str(tmp_path)])
        assert result.exit_code == 0

        version_file = tmp_path / ".version"
        angebot_schema = tmp_path / "bo/Angebot.json"
        assert version_file.exists()
        assert version_file.read_text() == "v202401.4.0"
        assert angebot_schema.exists()
        angebot = SchemaMeta(name="Angebot", module=("bo", "Angebot"), src=angebot_schema)
        angebot.set_schema_text(angebot_schema.read_text())
        assert angebot.get_schema_parsed().title == "Angebot"
        assert angebot.get_schema_parsed().properties["_typ"].any_of[0].ref == "../enum/Typ.json#"
