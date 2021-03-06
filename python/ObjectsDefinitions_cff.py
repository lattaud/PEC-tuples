"""Definitions of reconstructed physics objects.

The module is exploited by cmsRun configuration MiniAOD_cfg.py.  It
exports several functions define_* that define different reconstructed
objects.
"""

import FWCore.ParameterSet.Config as cms


def define_electrons(process):
    """Define reconstructed electrons.
    
    Configure reconstructed electrons to be used in an analysis,
    together with the relevant identification requirements.
    
    Arguments:
        process: The process to which relevant electron producers are
            added.
    
    Return value:
        Return a tuple with the following elements:
        eleQualityCuts: List of string-based quality selections whose
            decisions are to be saved.
        eleEmbeddedCutBasedIDLabels: Labels of boolean electron IDs
            embedded in pat::Electron whose decisions are to be saved.
        eleCutBasedIDMaps: Tags to access maps with boolean electron IDs
            whose decisions are to be saved.
        eleMVAIDMaps: Tags to access maps with continuous electron IDs
            whose decisions are to be saved.
    
    In addition to constructing the return values, add producers that
    create the following collections of electrons:
        analysisPatElectrons: Collection of loosely identified
            non-isolated electrons to be saved.
        patElectronsForEventSelection: Collection of loosely identified
            non-isolated electrons that pass a realistically tight
            kinematic selection.  Exploited in the loose event selection
            applied in the main configuration.
    """
    
    # Collection of electrons that will be stored in tuples
    process.analysisPatElectrons = cms.EDFilter('PATElectronSelector',
        src = cms.InputTag('slimmedElectrons'),
        cut = cms.string('pt > 20. & (abs(eta) < 2.5 | abs(superCluster.eta) < 2.5)')
    )
    
    
    # Labels to access embedded cut-based ID.  They are not used at the
    # moment, and all IDs are evaluated on the fly.
    eleEmbeddedCutBasedIDLabels = []
    
    
    # Setup VID for cut-based ID and trigger-emulating preselection [1]
    # and MVA-based ID [2]
    # [1] https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2?rev=41
    # [2] https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2?rev=30#VID_based_recipe_provides_pass_f
    from PhysicsTools.SelectorUtils.tools.vid_id_tools import (
        switchOnVIDElectronIdProducer, setupAllVIDIdsInModule, setupVIDElectronSelection,
        DataFormat
    )
    switchOnVIDElectronIdProducer(process, DataFormat.MiniAOD)
    
    for idModule in [
        'cutBasedElectronID_Summer16_80X_V1_cff',
        'cutBasedElectronHLTPreselecition_Summer16_V1_cff',
        'mvaElectronID_Spring16_GeneralPurpose_V1_cff'
    ]:
        setupAllVIDIdsInModule(
            process,
            'RecoEgamma.ElectronIdentification.Identification.' +
            idModule, setupVIDElectronSelection
        )
    
    process.egmGsfElectronIDs.physicsObjectSrc = 'analysisPatElectrons'
    process.electronMVAValueMapProducer.srcMiniAOD = 'analysisPatElectrons'
    
    
    # Add also customized cut-based ID without requirements on isolation
    setupAllVIDIdsInModule(
        process,
        'Analysis.PECTuples.cutBasedElectronID_nonIso_cff',
        setupVIDElectronSelection
    )
    
    
    # Labels of maps with electron ID
    eleIDProducer = 'egmGsfElectronIDs'
    eleCutBasedIDMaps = [eleIDProducer + ':cutBasedElectronID-Summer16-80X-V1-' + p
        for p in ['veto', 'loose', 'medium', 'tight']] + \
        [eleIDProducer + ':cutBasedElectronHLTPreselection-Summer16-V1'] + \
        [eleIDProducer + ':cutBasedElectronID-nonIso-tight']
    eleMVAIDMaps = ['electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values']
    
    
    # Additional selections to be evaluated (nothing at the moment)
    eleQualityCuts = cms.vstring()
    
    
    # Define electrons to be used for the loose event selection in the
    # main configuration.  Tighter kinematical cuts are applied to them.
    process.patElectronsForEventSelection = cms.EDFilter('PATElectronSelector',
        src = cms.InputTag('analysisPatElectrons'),
        cut = cms.string('pt > 23. & (abs(eta) < 2.5 | abs(superCluster.eta) < 2.5)')
    )
    
    
    # Return values
    return eleQualityCuts, eleEmbeddedCutBasedIDLabels, eleCutBasedIDMaps, eleMVAIDMaps



def define_muons(process):
    """Define reconstructed muons.
    
    Configure reconstructed muons to be used in an analysis, together
    with the relevant identification requirement.
    
    Arguments:
        process: The process to which relevant muon producers are added.
    
    Return value:
        A list of string-based quality selections whose decisions are to
            be saved.
    
    Also add producers that create the following collections of muons:
        analysisPatMuons: Collection of loosely identified non-isolated
            muons to be saved.
        patMuonsForEventSelection: Collection of loosely identified
            non-isolated muons that pass a realistically tight
            kinematic selection.  Exploited in the loose event selection
            applied in the main configuration.
    """
    
    # Define a collection of muons to be used in the analysis.  It
    # includes also non-isolated muons.
    process.analysisPatMuons = cms.EDFilter('PATMuonSelector',
        src = cms.InputTag('slimmedMuons'),
        cut = cms.string('pt > 10. & abs(eta) < 2.5')
    )
    
    
    # Specify additional selection cuts to be evaluated.  The list is
    # actually empty as the selection has been moved to the C++ code.
    muQualityCuts = cms.vstring()
    
    
    # A collection to be used for the loose event selection in the main
    # configuration.  Realistically tight kinematic cuts are applied.
    process.patMuonsForEventSelection = cms.EDFilter('PATMuonSelector',
        src = cms.InputTag('analysisPatMuons'),
        cut = cms.string('pt > 20. & abs(eta) < 2.5')
    )
    
    
    # Return values
    return muQualityCuts


def define_photons(process):
    """Define reconstructed photons.
    
    Configure reconstructed photons to be used in an analysis.
    
    Arguments:
        process: The process to which relevant photon producers are
            added.
    
    Return value:
        Return a tuple with the following elements:
        phoQualityCuts: List of string-based quality selections whose
            decisions are to be saved.
        phoCutBasedIDMaps: Tags to access maps with boolean photon IDs
            whose decisions are to be saved.
    
    In addition to constructing the return values, add producers that
    create the following collections of photons:
        analysisPatPhotons: Collection of loosely identified
            non-isolated photons to be saved.
    """
    
    # Collection of photons satisfying a basic kinematic selection
    process.analysisPatPhotons = cms.EDFilter('PATPhotonSelector',
        src = cms.InputTag('slimmedPhotons'),
        cut = cms.string('pt > 20. & abs(eta) < 2.5')
    )
    
    
    # Decisions of cut-based identification algorithm [1]
    # [1] https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedPhotonIdentificationRun2?rev=28
    from PhysicsTools.SelectorUtils.tools.vid_id_tools import (
        switchOnVIDPhotonIdProducer, setupAllVIDIdsInModule, setupVIDPhotonSelection,
        DataFormat
    )
    switchOnVIDPhotonIdProducer(process, DataFormat.MiniAOD)
    
    for idModule in ['cutBasedPhotonID_Spring15_25ns_V1_cff']:
        setupAllVIDIdsInModule(
            process,
            'RecoEgamma.PhotonIdentification.Identification.' +
            idModule, setupVIDPhotonSelection
        )
    
    process.photonIDValueMapProducer.srcMiniAOD = 'analysisPatPhotons'
    process.egmPhotonIDs.physicsObjectSrc = 'analysisPatPhotons'
    
    
    # Labels of maps with photon ID
    phoCutBasedIDMaps = ['egmPhotonIDs:cutBasedPhotonID-Spring15-25ns-V1-standalone-' + p
        for p in ['loose', 'medium', 'tight']]
    
    
    # Additional selections to be evaluated
    phoQualityCuts = cms.vstring(
        # EE-EB gap
        '(abs(superCluster.eta) < 1.4442 | abs(superCluster.eta) > 1.5660)'
    )
    
    return phoQualityCuts, phoCutBasedIDMaps



def define_jets(process, reapplyJEC=False, runOnData=False):
    """Define reconstructed jets.
    
    Configure reconstructed jets to be used in an analysis.  In
    particular, reapply JEC if requested.
    
    Arguments:
        process: The process to which relevant jet producers are added.
        reapplyJEC: Flag determining if JEC are to be reapplied or not.
        runOnData: Flag to distinguish processing of data and
            simulation.
    
    Return value:
        Return a tuple with the following elements:
        recorrectedJetsLabel: Label to access collection of jets with
            up-to-date JEC (reapplied or not, depending on the
            configuration) and no kinematic or quality selection.
        jetQualityCuts: List of string-based quality selections whose
            decisions are to be saved.
    
    Create the following jet collections:
        analysisPatJets: Jets with up-to-date JEC and a loose quality
            selection to be used in an analysis.
    """
    
    # Reapply JEC [1] and evaluate DeepCSV b-taggers [2].  Jet
    # collection is updated regardless of the value of parameter
    # reapplyJEC because of the b-taggers.
    # [1] https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections?rev=139#CorrPatJets
    # [2] https://twiki.cern.ch/twiki/bin/viewauth/CMS/DeepFlavour?rev=6
    jecLevels = ['L1FastJet', 'L2Relative', 'L3Absolute']
    if runOnData:
        jecLevels.append('L2L3Residual')
    
    from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
    updateJetCollection(
        process, labelName = 'UpdatedJECBTags',
        jetSource = cms.InputTag('slimmedJets'),
        jetCorrections = ('AK4PFchs', cms.vstring(jecLevels), 'None'),
        btagDiscriminators = [
            'pfDeepCSVJetTags:probbb', 'pfDeepCSVJetTags:probb',
            'pfDeepCSVJetTags:probcc', 'pfDeepCSVJetTags:probc',
            'pfDeepCSVJetTags:probudsg'
        ]
    )
    
    # When b-tagging is rerun, JEC are first undone, b-taggind is
    # discriminators are evaluated, and then another jet collection is
    # produced.  This is the name that is used for the final collection.
    recorrectedJetsLabel = 'updatedPatJetsTransientCorrectedUpdatedJECBTags'
    
    
    # Define analysis-level jets.  The produced collection will contain
    # all jets that have a chance to pass the given pt threshold thanks
    # to JEC and JER variations.
    process.analysisPatJets = cms.EDFilter('JERCJetSelector',
        src = cms.InputTag(recorrectedJetsLabel),
        jetTypeLabel = cms.string('AK4PFchs'),
        preselection = cms.string(''),
        minPt = cms.double(15.),
        includeJERCVariations = cms.bool(not runOnData),
        genJets = cms.InputTag('slimmedGenJets'),
        rho = cms.InputTag('fixedGridRhoFastjetAll')
    )
    
    
    # Additional selection to be evaluated (empty at the moment)
    jetQualityCuts = cms.vstring()
    
    
    return recorrectedJetsLabel, jetQualityCuts


def define_METs(process, runOnData=False):
    """Define reconstructed MET.
    
    Configure recalculation of corrected MET and its systematic
    uncertainties.  Only type-1 corrections are applied.  Due to
    limitations of MET tools, uncertainties are calculated even when
    running over data, while this is not needed.  Moreover, they include
    uncertainties corresponding to variations in energies of leptons,
    taus, and photons, although these variations are not considered in
    targeted analyses.
    
    Arguments:
        process: The process to which relevant MET producers are added.
        runOnData: Flag to distinguish processing of data and
            simulation.
    
    Return value:
        InputTag that defines MET collection to be used.
    """
    
    # Recalculate MET corrections [1]
    # [1] https://twiki.cern.ch/twiki/bin/view/CMS/MissingETUncertaintyPrescription?rev=64#Instructions_for_8_0_X_X_26_patc
    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import \
        runMetCorAndUncFromMiniAOD
    runMetCorAndUncFromMiniAOD(process, isData=runOnData, postfix='')
    
    
    # In data apply an additional correction for the ECAL gain switch
    # issue [1]
    # [1] https://twiki.cern.ch/twiki/bin/view/CMSPublic/ReMiniAOD03Feb2017Notes?rev=19#MET_Recipes
    if runOnData:
        from PhysicsTools.PatUtils.tools.corMETFromMuonAndEG import corMETFromMuonAndEG
        corMETFromMuonAndEG(
            process,
            pfCandCollection='',
            electronCollection='slimmedElectronsBeforeGSFix',
            photonCollection='slimmedPhotonsBeforeGSFix',
            corElectronCollection='slimmedElectrons',
            corPhotonCollection='slimmedPhotons',
            allMETEGCorrected=True,
            muCorrection=False,
            eGCorrection=True,
            runOnMiniAOD=True,
            postfix='MuEGClean'
        )
        
        process.slimmedMETsMuEGClean = process.slimmedMETs.clone(
            src = cms.InputTag('patPFMetT1MuEGClean'),
            rawVariation = cms.InputTag('patPFMetRawMuEGClean'),
            t1Uncertainties = cms.InputTag('patPFMetT1%sMuEGClean')
        )
        del process.slimmedMETsMuEGClean.caloMET
    
    
    if runOnData:
        metTag = cms.InputTag('slimmedMETsMuEGClean', processName=process.name_())
    else:
        metTag = cms.InputTag('slimmedMETs', processName=process.name_())
    
    return metTag
