
# Check alchemlyb version and API before writing the analysis script
import subprocess
result = subprocess.run([PYTHON, "-c", "import alchemlyb; print(alchemlyb.__version__)"],
                       capture_output=True, text=True)
print("alchemlyb version:", result.stdout.strip(), result.stderr.strip()[:200])

# Also check what extract_dHdl returns in terms of units
result2 = subprocess.run([PYTHON, "-c", """
from alchemlyb.parsing.gmx import extract_dHdl
from alchemlyb.estimators import MBAR
from alchemlyb.preprocessing.subsampling import statistical_inefficiency
print("imports OK")
# Check MBAR output units
import inspect
src = inspect.getsource(MBAR.fit)
# Just print a snippet
for line in src.split('\\n')[:30]:
    print(line)
"""], capture_output=True, text=True)
print(result2.stdout[:1000])
print(result2.stderr[:300])
