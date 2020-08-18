import os
from conans import ConanFile, tools


class BazelConan(ConanFile):
    name = "bazel"
    description = "A fast, scalable, multi-language and extensible build system"
    license = "Apache-2.0"
    homepage = "https://www.bazel.build/"
    url = "https://github.com/conan-io/conan-center-index"
    topics = ("conan", "bazel", "build", "bzl")
    settings = "os_build", "arch_build"
    no_copy_source = True

    def config_options(self):
        # Checking against self.settings.* would prevent cross-building profiles from working
        if self.settings.arch_build not in ["x86_64"]:
            raise ConanInvalidConfiguration("Unsupported Architecture.  This package currently only supports x86_64.")
        if self.settings.os_build not in ["Windows", "Macos", "Linux"]:
            raise ConanInvalidConfiguration("Unsupported System. This package currently only support Linux, Macos or Windows")

    def source(self):
        for source in self.conan_data["sources"][self.version]:
            url = source["url"]
            filename = url[url.rfind("/") + 1:]
            tools.download(url, filename)
            tools.check_sha256(filename, source["sha256"])

    def _convert_os_name(self, os_name):
        os_names = {
            "Windows": "windows",
            "Linux": "linux",
            "Macos": "darwin",
        }
        return os_names[os_name]

    def package(self):
        out_executable_name = "bazel"
        executable_name = "bazel-{version}-{os_name}-{arch}".format(version=self.version, os_name=self._convert_os_name(str(self.settings.os_build)), arch=self.settings.arch_build)
        if self.settings.os_build == "Windows":
            executable_name += ".exe"
            out_executable_name += ".exe"
        os.rename(os.path.join(self.source_folder, executable_name), os.path.join(self.source_folder, out_executable_name))
        self.copy(pattern=out_executable_name, dst="bin")
        self.copy("LICENSE", dst="licenses")

    def package_info(self):
        bin_path = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable: {}".format(bin_path))
        self.env_info.PATH.append(bin_path)
