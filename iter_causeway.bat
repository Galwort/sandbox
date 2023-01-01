@echo off

for /L %%i in (1, 1, 100) do (
    python causeway.pyw
    timeout /t 1
)