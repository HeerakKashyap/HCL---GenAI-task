@echo off
echo Starting RAG Frontend...
echo.
cd /d "%~dp0"
cd client
call npm start
pause

