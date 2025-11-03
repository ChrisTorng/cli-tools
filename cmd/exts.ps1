param(
    [Parameter(Position=0)]
    [string]$Path = "."
)

if (-not (Test-Path -Path $Path)) {
    Write-Error "Path not found: $Path"
    exit 1
}

Get-ChildItem -Path $Path -Recurse -File | Group-Object Extension | Select-Object Name, Count | Sort-Object Count -Descending