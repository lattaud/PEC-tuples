#include <Analysis/PECTuples/interface/Lepton.h>

#include <stdexcept>


pec::Lepton::Lepton() noexcept:
    CandidateWithID(),
    charge(false), relIso(0)
{}


void pec::Lepton::Reset()
{
    CandidateWithID::Reset();
    
    charge = false;
    relIso = 0;
}


void pec::Lepton::SetCharge(int charge_)
{
    if (charge_ == 0)
        throw std::logic_error("Lepton::SetCharge: The class is meant for charged leptons only.");
    
    charge = (charge_ < 0);
}


void pec::Lepton::SetRelIso(float relIso_)
{
    relIso = relIso_;
}


int pec::Lepton::Charge() const
{
    return ((charge) ? -1 : 1);
}


float pec::Lepton::RelIso() const
{
    return relIso;
}
