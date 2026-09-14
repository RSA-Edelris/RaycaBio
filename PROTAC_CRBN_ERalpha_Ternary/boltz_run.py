"""
Wrapper that suppresses tensorboard import crashes before running boltz.

Root cause: boltz uses pytorch_lightning with a TensorBoardLogger. The venv has
an incompatible/absent tensorboard installation so every lazy import inside the
logger chain crashes. Rather than patching individual import paths one by one,
we (a) stub all tensorboard-related modules so imports resolve, then (b) replace
the pytorch_lightning TensorBoardLogger class with a complete no-op so no real
tensorboard code is ever called.
"""
import sys
import types


def _pkg_stub(name):
    m = types.ModuleType(name)
    m.__path__ = []
    m.__package__ = name
    sys.modules[name] = m
    return m


def _mod_stub(name):
    m = types.ModuleType(name)
    sys.modules[name] = m
    return m


# ---------------------------------------------------------------------------
# tensorboard package stubs (prevent import errors when PL inspects them)
# ---------------------------------------------------------------------------
tb = _pkg_stub("tensorboard")

tb_ver = _mod_stub("tensorboard.version")
tb_ver.VERSION = "2.17.0"
tb.version = tb_ver

for _name in [
    "tensorboard.compat",
    "tensorboard.compat.proto",
]:
    _pkg_stub(_name)

for _sub in ("event_pb2", "summary_pb2", "graph_pb2", "node_def_pb2",
             "attr_value_pb2", "tensor_pb2", "tensor_shape_pb2"):
    _mod_stub(f"tensorboard.compat.proto.{_sub}")

for _name in [
    "tensorboard.plugins",
    "tensorboard.plugins.custom_scalar",
    "tensorboard.summary",
]:
    _pkg_stub(_name)

_mod_stub("tensorboard.summary.v2")

# ---------------------------------------------------------------------------
# torch.utils.tensorboard stubs
# ---------------------------------------------------------------------------


class _NoOpWriter:
    """Complete no-op standing in for torch SummaryWriter + its FileWriter."""
    def __init__(self, *a, **kw): pass
    def __enter__(self): return self
    def __exit__(self, *a): pass
    # SummaryWriter API
    def add_scalar(self, *a, **kw): pass
    def add_scalars(self, *a, **kw): pass
    def add_histogram(self, *a, **kw): pass
    def add_image(self, *a, **kw): pass
    def add_graph(self, *a, **kw): pass
    def add_text(self, *a, **kw): pass
    def add_hparams(self, *a, **kw): pass
    def add_summary(self, *a, **kw): pass
    def flush(self): pass
    def close(self): pass
    def get_logdir(self): return ""
    # FileWriter API (called via _get_file_writer())
    def _get_file_writer(self): return self
    def file_writer(self): return self


def _noop_hparams(*a, **kw):
    return {}, {}, {}


tb_torch = _pkg_stub("torch.utils.tensorboard")
tb_torch.SummaryWriter = _NoOpWriter
tb_torch_writer = _mod_stub("torch.utils.tensorboard.writer")
tb_torch_writer.SummaryWriter = _NoOpWriter
tb_torch.writer = tb_torch_writer
tb_torch_summary = _mod_stub("torch.utils.tensorboard.summary")
tb_torch_summary.hparams = _noop_hparams
tb_torch.summary = tb_torch_summary
tb_torch_utils = _mod_stub("torch.utils.tensorboard._utils")
tb_torch.utils = tb_torch_utils

# ---------------------------------------------------------------------------
# Patch pytorch_lightning TensorBoardLogger with a complete no-op class.
# This is the decisive fix: instead of chasing individual method gaps in our
# writer stub, we replace the logger class itself so PL never calls real TB code.
# ---------------------------------------------------------------------------
import pytorch_lightning.loggers.tensorboard as _pl_tb
import lightning_fabric.loggers.tensorboard as _lf_tb


class _NoOpTBLogger:
    """No-op TensorBoardLogger replacement for both PL and lightning_fabric."""

    def __init__(self, *a, **kw):
        self._writer = _NoOpWriter()

    # --- Logger identity ---
    @property
    def name(self): return "tensorboard"

    @property
    def version(self): return 0

    @property
    def root_dir(self): return "."

    @property
    def log_dir(self): return "."

    @property
    def save_dir(self): return "."

    # --- Experiment (the SummaryWriter) ---
    @property
    def experiment(self): return self._writer

    # --- Core logging methods ---
    def log_hyperparams(self, *a, **kw): pass
    def log_metrics(self, *a, **kw): pass
    def log_graph(self, *a, **kw): pass
    def log_image(self, *a, **kw): pass

    # --- Lifecycle ---
    def save(self): pass
    def finalize(self, *a): pass
    def after_save_checkpoint(self, *a): pass

    # --- PL trainer integration ---
    def agg_and_log_metrics(self, *a, **kw): pass
    def update_agg_funcs(self, *a, **kw): pass

    # --- Allow attribute access to return no-ops for anything we missed ---
    def __getattr__(self, name):
        def _noop(*a, **kw): pass
        return _noop


# Replace the class in both modules so PL constructs our no-op logger
_pl_tb.TensorBoardLogger = _NoOpTBLogger
_lf_tb.TensorBoardLogger = _NoOpTBLogger

# Also patch the classes into the loggers namespace if already imported there
try:
    import pytorch_lightning.loggers as _pl_loggers
    _pl_loggers.TensorBoardLogger = _NoOpTBLogger
except Exception:
    pass

# ---------------------------------------------------------------------------
# Now run boltz CLI normally
# ---------------------------------------------------------------------------
from boltz.main import cli
cli()
