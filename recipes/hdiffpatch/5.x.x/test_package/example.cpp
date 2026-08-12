#include <iostream>

#include <HDiffPatch/HDiff/diff.h>

using TByte = unsigned char;

int main() {
    std::cout << "Hello World!" << std::endl;

    const auto newStr = "";
    const auto oldStr = "1";

    const auto *newData = reinterpret_cast<const TByte *>(newStr);
    const auto *oldData = reinterpret_cast<const TByte *>(oldStr);
    auto diffData = std::vector<TByte>{};
    create_diff(newData, newData + strlen(newStr), oldData, oldData + strlen(oldStr), diffData);

    return 0;
}
