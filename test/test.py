# placeholder, temporary test

# test import
import matpower

# test print version
matpower.__version__

# test path
matpower.__path__[0] == matpower.path_matpower

# test start instante
m = matpower.start_instance(engine='lala')