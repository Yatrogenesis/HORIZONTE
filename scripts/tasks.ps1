param([string]$Task="help")

function Install-Dev {
  python -m pip install --upgrade pip
  pip install -e .[dev,api]
}

function Lint { ruff check src }
function Type { mypy src }
function Test { pytest -q }
function Api { uvicorn horizonte.api.server:app --reload }
function Sim { python -m horizonte.cli }

switch ($Task) {
  'install' { Install-Dev }
  'lint' { Lint }
  'type' { Type }
  'test' { Test }
  'api' { Api }
  'sim' { Sim }
  default { Write-Output "Tasks: install|lint|type|test|api|sim" }
}

