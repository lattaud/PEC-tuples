#include <UserCode/SingleTop/interface/Candidate.h>
#include <UserCode/SingleTop/interface/CandidateWithID.h>
#include <UserCode/SingleTop/interface/Lepton.h>
#include <UserCode/SingleTop/interface/Muon.h>
#include <UserCode/SingleTop/interface/Electron.h>
#include <UserCode/SingleTop/interface/Jet.h>
#include <UserCode/SingleTop/interface/GenParticle.h>
#include <UserCode/SingleTop/interface/GenJet.h>

#include <UserCode/SingleTop/interface/EventID.h>
#include <UserCode/SingleTop/interface/PileUpInfo.h>
#include <UserCode/SingleTop/interface/GeneratorInfo.h>

#include <vector>


// Instantiate templates
template class std::vector<pec::Candidate>;
template class std::vector<pec::CandidateWithID>;
template class std::vector<pec::Lepton>;
template class std::vector<pec::Muon>;
template class std::vector<pec::Electron>;
template class std::vector<pec::Jet>;
template class std::vector<pec::GenParticle>;
template class std::vector<pec::GenJet>;
