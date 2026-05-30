from __future__ import annotations

from pathlib import Path

from part1 import export_part1
from part2 import create_app, export_part2
from part3 import export_part3
from shared import load_data


def build_all_assets(output_dir: str | Path = ".") -> dict[str, Path]:
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    part1_path = export_part1(target_dir / "part1.png")
    part2_path = export_part2(path=target_dir / "part2.png")
    part3_path = export_part3(target_dir / "part3.png")

    return {"part1": part1_path, "part2": part2_path, "part3": part3_path}


def main() -> None:
    build_all_assets()
    dash_app = create_app(load_data())
    dash_app.run(debug=True, host="0.0.0.0", port=8050)


app = create_app(load_data())
server = app.server


if __name__ == "__main__":
    main()
