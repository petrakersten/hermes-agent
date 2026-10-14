"""Regression: the [edge-tts] extra must stay at >= 7.3.0 (#137944).

Microsoft rotated the Edge Voice DRM token scheme (Sec-MS-GEC) on
2026-10-12. Every edge-tts release before 7.3.0 fails every synthesis
with HTTP 403 against the live endpoint, which kills the default TTS
provider for all installs. This tripwire makes a dependency refresh that
silently rolls the extra back below 7.3.0 go red.
"""

from pathlib import Path
import tomllib


def _edge_tts_pin():
    root = Path(__file__).resolve().parents[1]
    metadata = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8-sig"))
    specs = metadata["project"]["optional-dependencies"]["edge-tts"]
    return next(spec for spec in specs if spec.startswith("edge-tts=="))


def test_edge_tts_extra_pin_clears_the_drm_rotation():
    pin = _edge_tts_pin()
    version = pin.split("==", 1)[1]
    assert tuple(int(part) for part in version.split(".")) >= (7, 3, 1), (
        "edge-tts < 7.3.1 lacks the complete Sec-MS-GEC v2 repair "
        "for the 2026-10-12 token rotation (#137944)"
    )

