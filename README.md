# Guide Blocks

A Python library for creating guided installation and setup procedures, supporting both manual and automatic steps.

## Installation

```bash
pip install guide_blocks
```

## Usage

```python
from typing import Dict, Generator

from guide_blocks import ManualGuideBlock, Step


class SetupDatabase(ManualGuideBlock):
    def run(self, ctx: Dict) -> Generator[Step, None, None]:
        yield Step(
            f"Create database {ctx['db_name']}",
            [
                "Open psql command prompt",
                f"Run: CREATE DATABASE {ctx['db_name']};"
            ]
        )
        ctx['db_initialized'] = True


# Run the guide
SetupDatabase.run_all(SetupDatabase, ctx={
    'db_name': 'myapp',
})
```

## Features

- Manual and automatic step execution
- Context sharing between steps
- CI/CD environment detection
- Step-by-step progression with user confirmation
- Substep support for detailed instructions

## License

MIT License