cmake_minimum_required(VERSION 3.4)
project(jpeg-compressor)

include(conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

set(jpegcompressor_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder")

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(MSVC AND BUILD_SHARED_LIBS)
	set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
endif()

# jgpe lib

set(JPGD_SRC_LIST ${jpegcompressor_SOURCE_DIR}/jpgd.cpp)
set(JPGD_HDR_LIST ${jpegcompressor_SOURCE_DIR}/jpgd.h ${jpegcompressor_SOURCE_DIR}/jpgd_idct.h)
add_library(jpgd ${JPGD_SRC_LIST} ${JPGD_HDR_LIST})
target_include_directories(jpgd PUBLIC ${jpegcompressor_SOURCE_DIR})


# jgpd lib

set(JPGE_SRC_LIST ${jpegcompressor_SOURCE_DIR}/jpge.cpp)
set(JPGE_HDR_LIST ${jpegcompressor_SOURCE_DIR}/jpge.h)
add_library(jpge ${JPGE_SRC_LIST} ${JPGE_HDR_LIST})
target_include_directories(jpge PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})


# jgpe executable

set(JPGEEXE_SRC_LIST ${jpegcompressor_SOURCE_DIR}/tga2jpg.cpp ${jpegcompressor_SOURCE_DIR}/timer.h ${jpegcompressor_SOURCE_DIR}/timer.cpp)

add_executable(jpge_exe ${JPGEEXE_SRC_LIST})
set_target_properties(jpge_exe PROPERTIES OUTPUT_NAME "jpge")
target_include_directories(jpge_exe PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(jpge_exe jpgd jpge CONAN_PKG::stb)

# installation

install(TARGETS jpge_exe jpgd jpge
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR})
install(FILES ${JPGE_HDR_LIST} ${JPGD_HDR_LIST} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
