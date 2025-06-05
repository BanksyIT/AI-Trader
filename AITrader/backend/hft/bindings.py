# Placeholder for bindings.py
"""
bindings.py
-----------
Python bindings and async interface to interact with high-speed C++/Rust-based HFT execution engine.
"""

import ctypes
import os

# Assuming compiled shared object (.so or .dll) is in the same folder
LIB_PATH = os.path.join(os.path.dirname(__file__), 'engine.so')

class HFTEngine:
    """
    Thin wrapper around native HFT execution engine.
    """

    def __init__(self):
        if not os.path.exists(LIB_PATH):
            raise FileNotFoundError(f"HFT engine not found at: {LIB_PATH}")

        self.lib = ctypes.CDLL(LIB_PATH)

        # Example function signatures
        self.lib.init_engine.restype = ctypes.c_int
        self.lib.send_order.argtypes = [ctypes.c_char_p, ctypes.c_double, ctypes.c_int]
        self.lib.send_order.restype = ctypes.c_int

    def init(self):
        return self.lib.init_engine()

    def send_order(self, symbol: str, price: float, quantity: int):
        return self.lib.send_order(symbol.encode('utf-8'), price, quantity)


# Async example usage (to be called from event loop)
async def async_send_order(symbol: str, price: float, quantity: int):
    engine = HFTEngine()
    engine.init()
    result = engine.send_order(symbol, price, quantity)
    return result
