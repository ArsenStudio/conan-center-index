#include "Remotery.h"

int main()
{
    Remotery* rmt;
    rmt_CreateGlobalInstance(&rmt);

    {
        rmt_BeginCPUSample(LogText, 0);
        rmt_LogText("Time me, please!");
        rmt_EndCPUSample();
    }

    {
        rmt_ScopedCPUSample(LogText, 0);
        rmt_LogText("Time me, too!");
    }

    rmt_DestroyGlobalInstance(rmt);

    return 0;
}
