import os
from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict, Generator, List, Optional


@dataclass
class Step:
    description: str
    substeps: Optional[List[str]] = None


class GuideBlock:
    @abstractmethod
    def run(self, ctx: Dict) -> Generator[Step, None, None]:
        raise NotImplementedError

    @classmethod
    def run_all(cls, *blocks, ctx=None):
        if ctx is None:
            ctx = dict()

        manual_blocks_exist = any(isinstance(b(), ManualGuideBlock) for b in blocks)
        if os.environ.get("CI_ENV") and manual_blocks_exist:
            raise RuntimeError("Manual steps cannot be run in CI environment")

        instantiated_blocks = [b() for b in blocks]
        for idx, block in enumerate(instantiated_blocks):
            print(f"Step {idx}: {block.name}")

            for step in block.run(ctx):
                print(f"\n{step.description}")
                if step.substeps:
                    for substep in step.substeps:
                        print(f"   - {substep}")

                if isinstance(block, ManualGuideBlock):
                    input("\nPress Enter to continue to the next step...")
            print()

        return ctx

    @classmethod
    @property
    def name(cls):
        return cls.__name__


class ManualGuideBlock(GuideBlock):
    pass


class AutomaticGuideBlock(GuideBlock):
    pass
