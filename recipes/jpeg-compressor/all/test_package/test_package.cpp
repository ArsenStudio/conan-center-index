#include <iostream>

#include "jpgd.h"


int main(int argc, char *argv[])
{
    if (argc < 2) {
        std::cerr << "Need at least two arguments" << std::endl;
    }
    const int req_components = 4;
    int w, h, components;
    unsigned char* image_data = jpgd::decompress_jpeg_image_from_file(argv[1], &w, &h, &components, req_components);
    free(image_data);

    return 0;
}
