#include <Analysis/PECTuples/interface/PileUpInfo.h>


using namespace pec;


PileUpInfo::PileUpInfo():
    numPV(0),
    rho(0),
    trueNumPU(0),
    inTimeNumPU(0)
{}


PileUpInfo::PileUpInfo(PileUpInfo const &src):
    numPV(src.numPV),
    rho(src.rho),
    trueNumPU(src.trueNumPU),
    inTimeNumPU(src.inTimeNumPU)
{}


PileUpInfo &PileUpInfo::operator=(PileUpInfo const &src)
{
    numPV = src.numPV;
    rho = src.rho;
    trueNumPU = src.trueNumPU;
    inTimeNumPU = src.inTimeNumPU;
    
    return *this;
}


void PileUpInfo::Reset()
{
    numPV = 0;
    rho = 0;
    trueNumPU = 0;
    inTimeNumPU = 0;
}


void PileUpInfo::SetNumPV(unsigned numPV_)
{
    numPV = numPV_;
}


void PileUpInfo::SetRho(float rho_)
{
    rho = rho_;
}


void PileUpInfo::SetTrueNumPU(float lambda)
{
    trueNumPU = lambda;
}


void PileUpInfo::SetInTimePU(unsigned n)
{
    inTimeNumPU = n;
}


unsigned PileUpInfo::NumPV() const
{
    return numPV;
}


float PileUpInfo::Rho() const
{
    return rho;
}


float PileUpInfo::TrueNumPU() const
{
    return trueNumPU;
}


unsigned PileUpInfo::InTimePU() const
{
    return inTimeNumPU;
}
