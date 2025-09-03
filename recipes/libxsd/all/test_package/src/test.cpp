#include <xsd/cxx/config.hxx>
int main() {
    // Just verify headers are present and compile
    return LIBXSD_VERSION >= 0 ? 0 : 1;
}
