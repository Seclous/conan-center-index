#include <xalanc/Include/PlatformDefinitions.hpp>
#include <iostream>
#include <xercesc/util/PlatformUtils.hpp>
#include <xalanc/XalanTransformer/XalanTransformer.hpp>

int main()
{
    try
    {
        xercesc::XMLPlatformUtils::Initialize();
        xalanc::XalanTransformer::initialize();

        {
            xalanc::XalanTransformer theXalanTransformer;
        }

        xalanc::XalanTransformer::terminate();
        xercesc::XMLPlatformUtils::Terminate();
        xalanc::XalanTransformer::ICUCleanUp();
    }
    catch(...)
    {
        std::cerr << "An unknown error occurred!" << std::endl;
        return 1;
    }

    return 0;
}
