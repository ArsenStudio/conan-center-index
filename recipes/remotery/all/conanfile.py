import os
import glob
from conans import CMake, ConanFile, tools
from conans.errors import ConanInvalidConfiguration


class RemoteryConan(ConanFile):
    name = "remotery"
    description = "Single C file, Realtime CPU/GPU Profiler with Remote Web Viewer"
    license = "Apache-2.0"
    homepage = "https://github.com/Celtoys/Remotery"
    url = "https://github.com/conan-io/conan-center-index"
    topics = ("conan", "cpu", "gpu", "profiling")
    exports_sources = ['CMakeLists.txt']
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_cuda": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_cuda": False,
    }

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd
        if self.options.with_cuda:
            self.output.warn("Conan package for CUDA is not available, this package will be used from system.")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = glob.glob('Remotery-*/')[0]
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["REMOTERY_USE_CUDA"] = self.options.with_cuda
        self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Windows":
            self.cpp_info.system_libs = ["ws2_32"]
        else:
            self.cpp_info.system_libs = ["pthread", "m"]
