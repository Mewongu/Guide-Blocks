from typing import Dict, Generator

import pytest

from guide_blocks import (
    AutomaticGuideBlock,
    GuideBlock,
    ManualGuideBlock,
    Step,
)


class SimpleManualBlock(ManualGuideBlock):
    def run(self, ctx: Dict) -> Generator[Step, None, None]:
        yield Step("Test step", ["Substep 1", "Substep 2"])
        ctx["test_completed"] = True


class SimpleAutomaticBlock(AutomaticGuideBlock):
    def run(self, ctx: Dict) -> Generator[Step, None, None]:
        ctx["auto_completed"] = True
        yield Step("Automatic step completed")


def test_manual_block_fails_in_ci(monkeypatch):
    monkeypatch.setenv("CI_ENV", "true")
    with pytest.raises(RuntimeError, match="Manual steps cannot be run in CI environment"):
        GuideBlock.run_all(SimpleManualBlock)


def test_automatic_block_execution(capsys):
    ctx = {}
    GuideBlock.run_all(SimpleAutomaticBlock, ctx=ctx)

    captured = capsys.readouterr()
    assert "Automatic step completed" in captured.out
    assert ctx["auto_completed"] is True


def test_mixed_blocks_fail_in_ci(monkeypatch):
    monkeypatch.setenv("CI_ENV", "true")
    with pytest.raises(RuntimeError, match="Manual steps cannot be run in CI environment"):
        GuideBlock.run_all(SimpleManualBlock, SimpleAutomaticBlock)


def test_context_sharing():
    class BlockOne(AutomaticGuideBlock):
        def run(self, ctx: Dict) -> Generator[Step, None, None]:
            ctx["shared_value"] = "test"
            yield Step("Set value")

    class BlockTwo(AutomaticGuideBlock):
        def run(self, ctx: Dict) -> Generator[Step, None, None]:
            assert ctx["shared_value"] == "test"
            yield Step("Read value")

    ctx = {}
    GuideBlock.run_all(BlockOne, BlockTwo, ctx=ctx)


def test_empty_context_initialization():
    ctx = GuideBlock.run_all(SimpleAutomaticBlock)
    assert isinstance(ctx, dict)


def test_step_without_substeps():
    class NoSubstepsBlock(AutomaticGuideBlock):
        def run(self, ctx: Dict) -> Generator[Step, None, None]:
            yield Step("Simple step")

    block = NoSubstepsBlock()
    steps = list(block.run({}))
    assert steps[0].substeps is None
