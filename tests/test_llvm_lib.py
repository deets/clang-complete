import os
from unittest import TestCase
from clangcomplete.llvm import setup_llvm_lib




class TestLLVMLib(TestCase):

    LLVM_LIB_CANDIDATES = [
        "/usr/local/Cellar/llvm//3.3/lib/libLLVM-3.3.dylib",
        ]

    def setUp(self):
        super(TestLLVMLib, self).setUp()
        for candidate in self.LLVM_LIB_CANDIDATES:
            if os.path.exists(candidate):
                self.llvm_lib_path = candidate
                break


    def test_llvm_lib_loading(self):
        setup_llvm_lib(self.llvm_lib_path)
