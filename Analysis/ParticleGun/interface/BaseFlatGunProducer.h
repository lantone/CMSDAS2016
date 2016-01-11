#ifndef BaseFlatGunProducer_H
#define BaseFlatGunProducer_H

/** \class FlatRandomEGunProducer
 *
 * Generates single particle gun in HepMC format
 * Julia Yarba 10/2005 
 ***************************************/
#include <string>

#include "HepPDT/defs.h"
#include "HepPDT/TableBuilder.hh"
#include "HepPDT/ParticleDataTable.hh"

#include "HepMC/GenEvent.h"

#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Run.h"

#include "CLHEP/Random/JamesRandom.h"
#include "CLHEP/Random/RandFlat.h"

#include <memory>
#include "boost/shared_ptr.hpp"

namespace edm
{
  
  class BaseFlatGunProducer : public EDProducer
  {
  
  public:
    BaseFlatGunProducer(const ParameterSet &);
    virtual ~BaseFlatGunProducer();
    void beginRun( edm::Run & r, const edm::EventSetup& ) ;
    void endRun( edm::Run& r, const edm::EventSetup& ) ;

  private:
   
  protected:
  
    // non-virtuals ! this and only way !
    //
    // data members
    
    // gun particle(s) characteristics
    std::vector<int> fPartIDs ;
    double           fMinEta ;
    double           fMaxEta ;
    double           fMinPhi ;
    double           fMaxPhi ;

    // the event format itself
    HepMC::GenEvent* fEvt;

    // HepMC/HepPDT related things 
    // (for particle/event construction)
    //std::string      fPDGTablePath ;
    //std::string      fPDGTableName ; 
    // DefaultConfig::ParticleDataTable* fPDGTable;
    // DefaultConfig::ParticleDataTable* fTestTable ;
    // ESHandle<DefaultConfig::ParticleDataTable> fPDGTable ;
    ESHandle<HepPDT::ParticleDataTable> fPDGTable ;
            	    	
    int              fVerbosity ;

    CLHEP::HepRandomEngine& fRandomEngine ;
    CLHEP::RandFlat*        fRandomGenerator; 
    
    bool             fAddAntiParticle;
    
  };
} 

#endif
