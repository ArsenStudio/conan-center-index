import os
from conans import ConanFile, tools


class RenderdocConan(ConanFile):
    name = "renderdoc"
    description = ("RenderDoc is a stand-alone graphics debugging tool")
    homepage = "https://renderdoc.org"
    url = "https://github.com/conan-io/conan-center-index"
    topics = ("conan", "graphics", "debugging")
    license = "MIT"
    no_copy_source = True

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "renderdoc-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def package(self):
        self.copy("*", dst="include", src=os.path.join(self._source_subfolder, "renderdoc", "api", "app"))
        self.copy("*", dst="include", src=os.path.join(self._source_subfolder, "renderdoc", "api", "replay"))
        self.copy("LICENSE.md", dst="licenses", src=self._source_subfolder)

    def package_id(self):
        self.info.header_only()
