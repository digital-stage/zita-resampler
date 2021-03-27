from conans import ConanFile, CMake, tools


class ZitaResamplerConan(ConanFile):
    name = "zita-resampler"
    version = "1.8.0"
    license = "GNU General Public License v3.0"
    author = "Fons Adriaensen <fons@linuxaudio.org>, conan recipe author: Christof Ruch <christof.ruch@gmx.de>"
    url = "https://github.com/christofmuc/zita-resampler"
    exports_sources = "*"
    description = "Zita-resampler is a C++ library for sample rate conversion of audio signals."
    topics = ("signal processing", "audio conversion")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = ["cmake", "cmake_find_package"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def requirements(self):
        if self.settings.os == "Windows":
            self.requires("pthreads4w/3.0.0")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=".")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include/zita-resampler", src="source/zita-resampler", keep_path=False)
        self.copy("*zita-resampler.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["zita-resampler"]
