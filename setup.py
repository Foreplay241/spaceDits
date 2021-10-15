import cx_Freeze

build_exe_options = {
            "packages": ["pygame"],
            "included_files": []
        }

cx_Freeze.setup(
    name="spaceDits",
    version="0.1",
    description="Space shooter from reddit.",
    options={"build_exe": build_exe_options},
    executables=[cx_Freeze.Executable("main.py")]
)
