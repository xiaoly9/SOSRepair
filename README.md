# SOSRepair #

SOSRepair is an automatic program repair tool which tries to fix programs with the help of both generate-and-validate
and semantics-based techniques.

### Requirements ###

You can use `docker` to build a container that already has all the
requirements installed and ready to go. Simply run
`docker build -t squareslab/sosrepair:latest .`.

* KLEE - You need to have KLEE up and running in your system. Find the
instruction of how to install KLEE on your system [here](http://klee.github.io/build-llvm34/).
SOSRepair has been confirmed to work on KLEE version 1.2 on using llvm 3.
* llvm and clang - You need to install llvm and clang by source to be
able to modify and extend it later. [Instruction](http://llvm.org/docs/GettingStarted.html).
SOSORepair has been confirmed to work on llvm commit \(db55668\) and clang commit \(2a0e7716\).
Updating llvm and clang to their latest version should not have an effect on SOSRepair.
Before building llvm and clang from source, apply the patch in `docker/0001-Binary-operation.patch`
to clang. This patch will add a functionality to python bindings that
are needed for SOSRepair. After building llvm and clang, set your `PYTHONPATH`
to include clang python bindings.
* Postgres
We will use Postgres as our database. Make sure you also install it's python binding (psycopg). You can
 install it using pip.
* Z3 SMT solver
You can install it from [here](https://github.com/Z3Prover/z3).

### Set-up ###

* Create a database on postgres using the command `createdb <testdb>`. 
(**Note:** If you are receiving errors like `role “username” does not exist`
you need to create user and role for postgres. [Here](https://stackoverflow.com/questions/11919391/postgresql-error-fatal-role-username-does-not-exist)
you can find the instruction on how to do that.)
* Edit `settings.py` file and edit based on your settings.
    * LIBCLANG_PATH: The path to libclang build. It should be either a .so or .dylib file.
    * GENERATE_DB_PATH: The path where the DB should be built from. SOSRepair will enumerate all C files in this path to build the DB.
    * Z3_COMMAND: The z3 command on this machine.
    * LARGEST_SNIPPET: The maximum number of lines that is considered as a snippet.
    * SMALLEST_SNIPPET: The minimum number of lines that is considered as a snippet.
    * DATABASE: Information about the database.
    * ALL_PATCHES: If False, SR will return the first found patch, otherwise it will try to find more.
    * LOGGING: Settings for logging.
    * MAX_SUSPICIOUS_LINES: The number of suspicious lines tried before giving up.
    * VALID_TYPES: The variable types that are right now supported by SOSRepair.
    * ------ Settings related to file under repair -------
    * TESTS_LIST: The path to a list of the tests that could be run on the file
    * TEST_SCRIPT: The path to a script that will run the test
    * COMPILE_SCRIPT: The path to a script that will compile the code
    * FAULTY_CODE: The path to the faulty code (a C file)
    * COMPILE_EXTRA_ARGS: The list of necessary arguments that should be passed to clang to properly parse the code
    * MAKE_OUTPUT: The output of running `make` stored in a file (for the purpose of finding necessary arguments for compilation
    automatically)
    * METHOD_RANGE: The tuple of beginning and end of method with the fault (limits the search to the area)
    * SOSREPAIR: If set to False it will only run SearchRepair features

An example of `settings.py` file for a simple defect exists in `docker/settings.py`.

### Running ###

* Run `python2.7 run.py -h` to see all the options of running SOSRepair. Overall, there are two modes for running (specified by `--run_mode`): `normal` and `bulk_run`. By default, the run mode is set to `normal` which will attempt to repair the file specified as `FAULTY_CODE` in the `settings.py` file. On `bulk_run` mode, SOSRepair attempts to repair all `.C` files in the `GENERATE_DB_PATH` directory and report how many of those it was able to repair.
There are three options for interacting with the database (specified by `--db`): `none`, `build_and_run`, `build`. By default this option is set to `none` which means it will not rebuild the database and will only read from it. Option `build` specifies that you only want to rebuild the database and you do not want to start the repair. Option `build_and_run` specifies that the repair will automatically start after rebuilding the database. Pay attention that `build` and `build_and_run` options automatically wipe out the data currently in the database and repopulate it with new data. 
* If you wish to remove logs from previous runs delete `logs/repair.log`.
* Whenever tool finds a patch it will put the patch inside folder `patches`
that is created at runtime

