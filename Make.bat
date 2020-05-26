@ECHO off
SETLOCAL

SET WD=%CD%
SET "HOSPITAL_HMIS_BUILD_PATH=%WD%\win-build"

SET CMDOPTION=""
IF "%1" == "clean"  SET CMDOPTION="VALID"
IF "%1" == "x86"    SET CMDOPTION="VALID"

IF NOT %CMDOPTION%=="VALID" (
    GOTO USAGE
)

SET ARCHITECTURE=%1

IF "%ARCHITECTURE%"=="clean" (
    CALL :CLEAN
    EXIT /B %ERRORLEVEL%
)


REM Main build sequence
CALL :SET_ENVIRONMENT
CALL :VALIDATE_ENVIRONMENT || EXIT /B 1
CALL :CLEAN || EXIT /B 1
CALL :CREATE_VIRTUAL_ENV || EXIT /B 1
CALL :CREATE_RUNTIME_ENV || EXIT /B 1
CALL :CREATE_PYTHON_ENV || EXIT /B 1
CALL :CLEANUP_ENV || EXIT /B 1
CALL :CREATE_INSTALLER || EXIT /B 1
CALL :SIGN_INSTALLER || EXIT /B 1

EXIT /B %ERRORLEVEL%
REM Main build sequence Ends


:CLEAN
    ECHO Removing build directory...
    IF EXIST "%HOSPITAL_HMIS_BUILD_PATH%" RD "%HOSPITAL_HMIS_BUILD_PATH%" /S /Q > nul || EXIT /B 1

    ECHO Removing temp build directory...
    IF EXIST "%WD%\pkg\win32\Output" rd "%WD%\pkg\win32\Output" /S /Q > nul || EXIT /B 1

    ECHO Removing installer configuration script...
    IF EXIST DEL /q "%WD%\pkg\win32\installer.iss" > nul || EXIT /B 1

    EXIT /B 0


:SET_ENVIRONMENT
    ECHO Configuring the environment...
    IF "%PYTHON_HOME%" == ""   SET "PYTHON_HOME=C:\Python38-32"
    IF "%PYTHON_DLL%" == ""    SET "PYTHON_DLL=C:\Windows\SysWOW64\python38.dll"
    IF "%QTDIR%" == ""         SET "QTDIR=C:\Qt\5.9.1\mingw53_32"
    IF "%MAKE%" == ""          SET "MAKE=mingw32-make.exe"
    IF "%PGDIR%" == ""         SET "PGDIR=C:\Program Files (x86)\PostgreSQL\10"
    IF "%INNOTOOL%" == ""      SET "INNOTOOL=C:\Program Files (x86)\Inno Setup 5"
    IF "%VCREDIST%" == ""      SET "VCREDIST=C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\redist\1033\vcredist_x86.exe"
    IF "%SIGNTOOL%" == ""      SET "SIGNTOOL=C:\Program Files\Microsoft SDKs\Windows\v7.1A\Bin\signtool.exe"

    REM Set VCREDISTNAME (the filename)
    for /f "delims=" %%i in ("%VCREDIST%") do set "VCREDISTNAME=%%~nxi"

    REM Set additional variables we need
    SET "QMAKE=%QTDIR%\bin\qmake.exe"
    FOR /F "tokens=4,5 delims=. " %%a IN ('%QMAKE% -v ^| findstr /B /C:"Using Qt version "') DO SET QT_VERSION=%%a.%%b

    SET "VIRTUALENV=venv"
    SET "TARGET_DIR=%WD%\dist"

    FOR /F "tokens=3" %%a IN ('findstr /C:"APP_RELEASE =" %WD%\HospitalHMIS\config.py')    DO SET APP_MAJOR=%%a
    FOR /F "tokens=3" %%a IN ('findstr /C:"APP_REVISION =" %WD%\HospitalHMIS\config.py')   DO SET APP_MINOR=%%a
    FOR /F "tokens=3" %%a IN ('findstr /C:"APP_SUFFIX =" %WD%\HospitalHMIS\config.py')     DO SET APP_VERSION_SUFFIX=%%a
    REM remove single quote from the string
    SET APP_VERSION_SUFFIX=%APP_VERSION_SUFFIX:'=%
    SET APP_NAME=""
    FOR /F "tokens=2* DELims='" %%a IN ('findstr /C:"APP_NAME =" HospitalHMIS\config.py')   DO SET APP_NAME=%%a
    FOR /f "tokens=1 DELims=." %%G IN ('%PYTHON_HOME%/python.exe -c "print('%APP_NAME%'.lower().replace(' ', ''))"') DO SET APP_SHORTNAME=%%G
    SET APP_VERSION=%APP_MAJOR%.%APP_MINOR%
    SET INSTALLERNAME=%APP_SHORTNAME%-%APP_MAJOR%.%APP_MINOR%-%APP_VERSION_SUFFIX%-%ARCHITECTURE%.exe
    IF "%APP_VERSION_SUFFIX%" == "" SET INSTALLERNAME=%APP_SHORTNAME%-%APP_MAJOR%.%APP_MINOR%-%ARCHITECTURE%.exe

    REM get Python version for the runtime build ex. 2.7.1 will be 27
    FOR /f "tokens=1 DELims=." %%G IN ('%PYTHON_HOME%/python.exe -c "import sys; print(sys.version.split(' ')[0])"') DO SET PYTHON_MAJOR=%%G
    FOR /f "tokens=2 DELims=." %%G IN ('%PYTHON_HOME%/python.exe -c "import sys; print(sys.version.split(' ')[0])"') DO SET PYTHON_MINOR=%%G
    SET "PYTHON_VERSION=%PYTHON_MAJOR%%PYTHON_MINOR%"

    EXIT /B 0


:VALIDATE_ENVIRONMENT
    ECHO ****************************************************************
    ECHO                        S U M M A R Y
    ECHO ****************************************************************
    ECHO Build path:                %HOSPITAL_HMIS_BUILD_PATH%
    ECHO Output directory:          %TARGET_DIR%
    ECHO Installer name:            %INSTALLERNAME%
    ECHO.
    ECHO Python home:               %PYTHON_HOME%
    ECHO Python DLL:                %PYTHON_DLL%
    ECHO Python version:            %PYTHON_VERSION%
    ECHO Python major version:      %PYTHON_MAJOR%
    ECHO Python minor version:      %PYTHON_MINOR%
    ECHO.
    ECHO Qt home:                   %QTDIR%
    ECHO qmake executable:          %QMAKE%
    ECHO Qt version:                %QT_VERSION%
    ECHO.
    ECHO PostgreSQL home:           %PGDIR%
    ECHO.
    ECHO VC++ redistributable:      %VCREDIST%
    ECHO VC++ redistributable file: %VCREDISTNAME%
    ECHO.
    ECHO innotool executable:       %INNOTOOL%
    ECHO signtool executable:       %SIGNTOOL%
    ECHO.
    ECHO App major version:         %APP_MAJOR%
    ECHO App minor version:         %APP_MINOR%
    ECHO App version:               %APP_VERSION%
    ECHO App version suffix:        %APP_VERSION_SUFFIX%
    ECHO App short name:            %APP_SHORTNAME%
    ECHO App name:                  %APP_NAME%
    ECHO ****************************************************************

    ECHO Checking the environment...
    IF NOT EXIST "%INNOTOOL%" (
        ECHO !INNOTOOL! does not exist
        ECHO Please install Innotool and set the INNOTOOL environment variable.
        EXIT /B 1
    )

    IF NOT EXIST "%VCREDIST%" (
        ECHO !VCREDIST! does not exist
        ECHO Please install Microsoft Visual studio and set the VCREDIST environment variable.
        EXIT /B 1
    )

    IF NOT EXIST "%QTDIR%" (
        ECHO !QTDIR! does not exist.
        ECHO Please install Qt and set the QTDIR environment variable.
        EXIT /B 1
    )

    IF NOT EXIST "%QMAKE%" (
        ECHO !QMAKE! does not exist.
        ECHO Please install Qt and set the QTDIR environment variable.
        EXIT /B 1
    )

    IF NOT EXIST "%PYTHON_HOME%" (
        ECHO !PYTHON_HOME! does not exist.
        ECHO Please install Python and set the PYTHON_HOME environment variable.
        EXIT /B 1
    )

    IF NOT EXIST "%PYTHON_DLL%" (
        ECHO !PYTHON_DLL! does not exist.
        ECHO Please install Python and set the PYTHON_DLL environment variable.
        EXIT /B 1
    )

    IF NOT EXIST "%PGDIR%" (
        ECHO !PGDIR! does not exist.
        ECHO Please install PostgreSQL and set the PGDIR environment variable.
        EXIT /B 1
    )

    IF NOT EXIST "%PYTHON_HOME%\Scripts\virtualenv.exe" (
        ECHO !PYTHON_HOME!\Scripts\virtualenv.exe does not exist.
        ECHO Please install the virtualenv package in Python.
        EXIT /B 1
    )

    SET "PATH=%PGDIR%\bin;%PATH%"

    EXIT /B 0


:CREATE_VIRTUAL_ENV
    ECHO Creating virtual environment...
    IF NOT EXIST "%HOSPITAL_HMIS_BUILD_PATH%"  MKDIR "%HOSPITAL_HMIS_BUILD_PATH%"
    
    CD "%HOSPITAL_HMIS_BUILD_PATH%"
    "%PYTHON_HOME%\Scripts\virtualenv.exe" "%VIRTUALENV%"

    XCOPY /S /I /E /H /Y "%PYTHON_HOME%\DLLs" "%HOSPITAL_HMIS_BUILD_PATH%\%VIRTUALENV%\DLLs" > nul || EXIT /B 1
    XCOPY /S /I /E /H /Y "%PYTHON_HOME%\Lib" "%HOSPITAL_HMIS_BUILD_PATH%\%VIRTUALENV%\Lib" > nul || EXIT /B 1

    ECHO Activating virtual environment -  %HOSPITAL_HMIS_BUILD_PATH%\%VIRTUALENV%...
    CALL "%HOSPITAL_HMIS_BUILD_PATH%\%VIRTUALENV%\Scripts\activate" || EXIT /B 1

    ECHO Installing dependencies...
    CALL pip install -r "%WD%\requirements.txt" || EXIT /B 1
    CALL pip install sphinx || EXIT /B 1

    REM If we're using VC++, and this is Python 3.6+, we need to remove the hack
    REM above or it will break qmake. Sigh.
    IF "%MAKE%" == "nmake" (
        IF %PYTHON_VERSION% GEQ 36 SET CL=
    )

    CD %WD%
    EXIT /B 0


:CREATE_RUNTIME_ENV
    MKDIR "%HOSPITAL_HMIS_BUILD_PATH%\runtime"

    CD "%WD%\HospitalHMIS"

    ECHO Installing javascript dependencies...
    CALL yarn install || EXIT /B 1

    ECHO Bundling javascript...
    CALL yarn run bundle || EXIT /B 1

    ECHO Removing HospitalHMISpack caches...
    RD /Q /S "%WD%\HospitalHMIS\static\js\generated\.cache" 1> nul 2>&1

    ECHO Copying HospitalHMIS directory...
    XCOPY /S /I /E /H /Y "%WD%\HospitalHMIS" "%HOSPITAL_HMIS_BUILD_PATH%\HospitalHMIS" > nul || EXIT /B 1

    ECHO Cleaning up unnecessary .pyc and .pyo files...
    FOR /R "%HOSPITAL_HMIS_BUILD_PATH%\HospitalHMIS" %%f in (*.pyc *.pyo) do DEL /q "%%f" 1> nul 2>&1
    ECHO Removing tests, Python caches and node modules...
    FOR /R "%HOSPITAL_HMIS_BUILD_PATH%\HospitalHMIS" %%f in (tests feature_tests __pycache__ node_modules) do RD /Q /S "%%f" 1> nul 2>&1
    ECHO Removing the test framework...
    RD /Q /S "%HOSPITAL_HMIS_BUILD_PATH%\HospitalHMIS\regression" 1> nul 2>&1
    ECHO Removing tools...
    RD /Q /S "%HOSPITAL_HMIS_BUILD_PATH%\HospitalHMIS\tools" 1> nul 2>&1
    ECHO Removing any existing configurations...
    DEL /q "%HOSPITAL_HMIS_BUILD_PATH%\HospitalHMIS\HospitalHMIS.db" 1> nul 2>&1
    DEL /q "%HOSPITAL_HMIS_BUILD_PATH%\HospitalHMIS\config_local.py" 1> nul 2>&1
    
    ECHO Creating config_distro.py
    ECHO SERVER_MODE = False > "%HOSPITAL_HMIS_BUILD_PATH%\HospitalHMIS\config_distro.py"
    ECHO HELP_PATH = '../../../docs/en_US/html/' >> "%HOSPITAL_HMIS_BUILD_PATH%\HospitalHMIS\config_distro.py"
    ECHO DEFAULT_BINARY_PATHS = { >> "%HOSPITAL_HMIS_BUILD_PATH%\HospitalHMIS\config_distro.py"
    ECHO     'pg':   '$DIR/../runtime', >> "%HOSPITAL_HMIS_BUILD_PATH%\HospitalHMIS\config_distro.py"
    ECHO     'ppas': '' >> "%HOSPITAL_HMIS_BUILD_PATH%\HospitalHMIS\config_distro.py"
    ECHO } >> "%HOSPITAL_HMIS_BUILD_PATH%\HospitalHMIS\config_distro.py"

    ECHO Building docs...
    MKDIR "%HOSPITAL_HMIS_BUILD_PATH%\docs\en_US\html"
    CD "%WD%\docs\en_US"
    CALL "%HOSPITAL_HMIS_BUILD_PATH%\%VIRTUALENV%\Scripts\python.exe" build_code_snippet.py || EXIT /B 1
    CALL "%HOSPITAL_HMIS_BUILD_PATH%\%VIRTUALENV%\Scripts\sphinx-build.exe"   "%WD%\docs\en_US" "%HOSPITAL_HMIS_BUILD_PATH%\docs\en_US\html" || EXIT /B 1

    ECHO Removing Sphinx
    CALL pip uninstall -y sphinx Pygments alabaster colorama docutils imagesize requests snowballstemmer

    ECHO Assembling runtime environment...
    CD "%WD%\runtime"

    ECHO Running qmake...
    CALL set "PGADMIN_PYTHON_DIR=%PYTHON_HOME%" && "%QMAKE%" || EXIT /B 1

    ECHO Cleaning the build directory...
    CALL %MAKE% clean || EXIT /B 1

    ECHO Running make...
    CALL %MAKE% || EXIT /B 1

    ECHO Staging pgAdmin4.exe...
    COPY "%WD%\runtime\release\pgAdmin4.exe" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1

    ECHO Staging Qt components...
    COPY "%QTDIR%\bin\Qt5Core.dll"   "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1
    COPY "%QTDIR%\bin\Qt5Gui.dll"    "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1
    COPY "%QTDIR%\bin\Qt5Widgets.dll" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul  || EXIT /B 1
    COPY "%QTDIR%\bin\Qt5Network.dll" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1
    COPY "%QTDIR%\bin\Qt5Svg.dll" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1
    IF EXIST "%QTDIR%\bin\libgcc_s_dw2-1.dll" COPY "%QTDIR%\bin\libgcc_s_dw2-1.dll" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1
    IF EXIST "%QTDIR%\bin\libstdc++-6.dll" COPY "%QTDIR%\bin\libstdc++-6.dll" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1
    IF EXIST "%QTDIR%\bin\libwinpthread-1.dll" COPY "%QTDIR%\bin\libwinpthread-1.dll" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1
    MKDIR "%HOSPITAL_HMIS_BUILD_PATH%\runtime\platforms" > nul || EXIT /B 1
    COPY "%QTDIR%\plugins\platforms\qwindows.dll" "%HOSPITAL_HMIS_BUILD_PATH%\runtime\platforms" > nul || EXIT /B 1
    MKDIR "%HOSPITAL_HMIS_BUILD_PATH%\runtime\imageformats" > nul || EXIT /B 1
    COPY "%QTDIR%\plugins\imageformats\qsvg.dll" "%HOSPITAL_HMIS_BUILD_PATH%\runtime\imageformats" > nul || EXIT /B 1
    ECHO [Paths] > "%HOSPITAL_HMIS_BUILD_PATH%\runtime\qt.conf"
    ECHO Plugins=plugins >> "%HOSPITAL_HMIS_BUILD_PATH%\runtime\qt.conf"

    ECHO Staging PostgreSQL components...
    COPY "%PGDIR%\bin\libpq.dll" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1
    IF EXIST "%PGDIR%\bin\libcrypto-1_1.dll" (
        REM OpenSSL 1.1.1
        COPY "%PGDIR%\bin\libcrypto-1_1.dll" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1
        COPY "%PGDIR%\bin\libssl-1_1.dll" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1
    ) ELSE (
        REM OpenSSL 1.0.2
        COPY "%PGDIR%\bin\ssleay32.dll" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1
        COPY "%PGDIR%\bin\libeay32.dll" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1
    )
    IF EXIST "%PGDIR%\bin\libintl-*.dll" COPY "%PGDIR%\bin\libintl-*.dll" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1
    IF EXIST "%PGDIR%\bin\libiconv-*.dll" COPY "%PGDIR%\bin\libiconv-*.dll" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1
    IF EXIST "%PGDIR%\bin\zlib.dll" COPY "%PGDIR%\bin\zlib.dll" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1
    IF EXIST "%PGDIR%\bin\zlib1.dll" COPY "%PGDIR%\bin\zlib1.dll" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1
    COPY "%PGDIR%\bin\pg_dump.exe" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1
    COPY "%PGDIR%\bin\pg_dumpall.exe" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1L%
    COPY "%PGDIR%\bin\pg_restore.exe" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1
    COPY "%PGDIR%\bin\psql.exe" "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1

    ECHO Staging VC++ runtime...
    MKDIR "%HOSPITAL_HMIS_BUILD_PATH%\installer" || EXIT /B 1
    COPY "%VCREDIST%" "%HOSPITAL_HMIS_BUILD_PATH%\installer" > nul || EXIT /B 1

    CD %WD%
    EXIT /B 0
    

:CREATE_PYTHON_ENV
    ECHO Staging Python...
    COPY %PYTHON_DLL% "%HOSPITAL_HMIS_BUILD_PATH%\runtime"  > nul || EXIT /B 1
    COPY %PYTHON_HOME%\python.exe "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1
    COPY %PYTHON_HOME%\pythonw.exe "%HOSPITAL_HMIS_BUILD_PATH%\runtime" > nul || EXIT /B 1

    ECHO Cleaning up unnecessary .pyc and .pyo files...
    FOR /R "%HOSPITAL_HMIS_BUILD_PATH%\%VIRTUALENV%" %%f in (*.pyc *.pyo) do DEL /q "%%f" 1> nul 2>&1
    ECHO Removing tests...
    FOR /R "%HOSPITAL_HMIS_BUILD_PATH%\%VIRTUALENV%\Lib" %%f in (test tests) do RD /Q /S "%%f" 1> nul 2>&1
    ECHO Removing TCL...
    RD /Q /S "%HOSPITAL_HMIS_BUILD_PATH%\%VIRTUALENV%\tcl" 1> nul 2>&1

    EXIT /B 0


:CREATE_INSTALLER
    ECHO Preparing for creation of windows installer...
    IF NOT EXIST "%TARGET_DIR%" MKDIR "%TARGET_DIR%"

    ECHO Copying icon file...
    COPY "%WD%\pkg\win32\Resources\pgAdmin4.ico" "%HOSPITAL_HMIS_BUILD_PATH%" > nul || EXIT /B 1

    CD "%WD%\pkg\win32"

    ECHO Processing installer configuration script...
    CALL "%PYTHON_HOME%\python" "%WD%\pkg\win32\replace.py" "-i" "%WD%\pkg\win32\installer.iss.in" "-o" "%WD%\pkg\win32\installer.iss.in_stage1" "-s" MYAPP_NAME -r """%APP_NAME%"""
    CALL "%PYTHON_HOME%\python" "%WD%\pkg\win32\replace.py" "-i" "%WD%\pkg\win32\installer.iss.in_stage1" "-o" "%WD%\pkg\win32\installer.iss.in_stage2" "-s" MYAPP_FULLVERSION -r """%APP_VERSION%"""
    CALL "%PYTHON_HOME%\python" "%WD%\pkg\win32\replace.py" "-i" "%WD%\pkg\win32\installer.iss.in_stage2" "-o" "%WD%\pkg\win32\installer.iss.in_stage3" "-s" MYAPP_VERSION -r """v%APP_MAJOR%"""

    SET ARCMODE=
    IF "%ARCHITECTURE%"=="amd64" (
        set ARCMODE="x64"
    )
    CALL "%PYTHON_HOME%\python" "%WD%\pkg\win32\replace.py" "-i" "%WD%\pkg\win32\installer.iss.in_stage3" "-o" "%WD%\pkg\win32\installer.iss.in_stage4" "-s" MYAPP_ARCHITECTURESMODE -r """%ARCMODE%"""
    CALL "%PYTHON_HOME%\python" "%WD%\pkg\win32\replace.py" "-i" "%WD%\pkg\win32\installer.iss.in_stage4" "-o" "%WD%\pkg\win32\installer.iss" "-s" MYAPP_VCDIST -r """%VCREDISTNAME%"""

    ECHO Cleaning up...
    DEL /s "%WD%\pkg\win32\installer.iss.in_stage*" > nul

    ECHO Creating windows installer using INNO tool...
    CALL "%INNOTOOL%\ISCC.exe" /q "%WD%\pkg\win32\installer.iss" || EXIT /B 1

    ECHO Renaming installer...
    MOVE "%WD%\pkg\win32\Output\Setup.exe" "%TARGET_DIR%\%INSTALLERNAME%" > nul || EXIT /B 1

    ECHO Location - %TARGET_DIR%\%INSTALLERNAME%
    ECHO Installer generated successfully.

    CD %WD%
    EXIT /B 0


:SIGN_INSTALLER
    ECHO Attempting to sign the installer...
    CALL "%SIGNTOOL%" sign  /t http://timestamp.verisign.com/scripts/timstamp.dll "%TARGET_DIR%\%INSTALLERNAME%"
    IF %ERRORLEVEL% NEQ 0 (
        ECHO.
        ECHO ************************************************************
        ECHO * Failed to sign the installer
        ECHO ************************************************************
        PAUSE
    )

    EXIT /B 0


:CLEANUP_ENV
    ECHO Cleaning the build environment...
    RD "%HOSPITAL_HMIS_BUILD_PATH%\%VIRTUALENV%\Include" /S /Q 1> nul 2>&1
    DEL /s "%HOSPITAL_HMIS_BUILD_PATH%\%VIRTUALENV%\pip-selfcheck.json" 1> nul 2>&1

    EXIT /B 0


:USAGE
    ECHO Invalid command line options.
    ECHO Usage: "Make.bat <x86 | clean>"
    ECHO.

    EXIT /B 1

