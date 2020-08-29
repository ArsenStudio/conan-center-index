import os
import glob
from conans import ConanFile, CMake, tools


class JpegCompressorConan(ConanFile):
    name = "jpeg-compressor"
    description = "C++ JPEG compression/fuzzed low-RAM JPEG decompression codec."
    topics = ("conan", "jpeg", "compression", "decompression")
    homepage = "https://github.com/richgel999/jpeg-compressor"
    url = "https://github.com/conan-io/conan-center-index"
    license = "Unlicense", "Apache-2.0"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = ["CMakeLists.txt"]
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
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

    def build_requirements(self):
        self.build_requires("stb/20200203")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = glob.glob(self.name + "-*/")[0]
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def _extract_licenses(self):
        header = tools.load(os.path.join(self._source_subfolder, "jpge.cpp"))
        unlicense_content = header[header.find("License 1: "):header.find("License 2:")]
        tools.save("LICENSE_UNLICENSE", unlicense_content)
        apache_content = header[header.find("License 2:"):header.rfind("limitations under the License.")]
        tools.save("LICENSE_APACHE2.0", apache_content)

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self._extract_licenses()
        self.copy("LICENSE_APACHE2.0", dst="licenses")
        self.copy("LICENSE_UNLICENSE", dst="licenses")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
