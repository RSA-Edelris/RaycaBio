
from modulon.engine import dispatch as dmod
import inspect
dsrc = inspect.getsource(dmod)
print(dsrc[:4000])
