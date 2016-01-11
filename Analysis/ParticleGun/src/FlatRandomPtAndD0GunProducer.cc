/*
 *  $Date: 2011/11/28 13:32:58 $
 *  $Revision: 1.2 $
 *  \author Julia Yarba
 */

#include <ostream>

#include "Analysis/ParticleGun/interface/FlatRandomPtAndD0GunProducer.h"

#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"


using namespace edm;
using namespace std;

FlatRandomPtAndD0GunProducer::FlatRandomPtAndD0GunProducer(const ParameterSet& pset) :
  BaseFlatGunProducer(pset)
{
  ParameterSet pgun_params = pset.getParameter<ParameterSet>("PGunParameters") ;
  
  fMinPt = pgun_params.getParameter<double>("MinPt");
  fMaxPt = pgun_params.getParameter<double>("MaxPt");
  d0Min_ = pgun_params.getParameter<double>("D0Min");
  d0Max_ = pgun_params.getParameter<double>("D0Max");

  produces<HepMCProduct>();
  produces<GenEventInfoProduct>();
}

FlatRandomPtAndD0GunProducer::~FlatRandomPtAndD0GunProducer()
{
   // no need to cleanup GenEvent memory - done in HepMCProduct
}

void FlatRandomPtAndD0GunProducer::produce(Event &e, const EventSetup& es)
{
  if ( fVerbosity > 0 ) {
    cout << " FlatRandomPtAndD0GunProducer : Begin New Event Generation" << endl ;
  }
  // event loop (well, another step in it...)
  // no need to clean up GenEvent memory - done in HepMCProduct
  //
  // here re-create fEvt (memory)
  //
  fEvt = new HepMC::GenEvent();

  // now actualy, cook up the event from PDGTable and gun parameters
  //
  // 1st, primary vertex
  //
  HepMC::GenVertex* Vtx = 0;
  if( d0Min_ == d0Max_ ) {
    Vtx = new HepMC::GenVertex(HepMC::FourVector(d0Min_,0.,0.));
  }
  else {
    double d0 = fRandomGenerator->fire(d0Min_, d0Max_);
    Vtx = new HepMC::GenVertex(HepMC::FourVector(d0,0.,0.));
  }

  // loop over particles
  //
  int barcode = 1 ;
  for (unsigned int ip=0; ip<fPartIDs.size(); ++ip) {
    double pt     = fRandomGenerator->fire(fMinPt, fMaxPt);
    double eta    = fRandomGenerator->fire(fMinEta, fMaxEta);
    double phi    = fRandomGenerator->fire(fMinPhi, fMaxPhi);
    int PartID = fPartIDs[ip];
    const HepPDT::ParticleData * PData = fPDGTable->particle(HepPDT::ParticleID(abs(PartID))) ;
    double mass   = PData->mass().value() ;
    double theta  = 2.*atan(exp(-eta)) ;
    double mom    = pt/sin(theta) ;
    double px     = pt*cos(phi) ;
    double py     = pt*sin(phi) ;
    double pz     = mom*cos(theta) ;
    double energy2= mom*mom + mass*mass ;
    double energy = sqrt(energy2) ;
    HepMC::FourVector p(px,py,pz,energy) ;
    HepMC::GenParticle* Part = new HepMC::GenParticle(p,PartID,1);
    Part->suggest_barcode( barcode ) ;
    barcode++ ;
    Vtx->add_particle_out(Part);

    if ( fAddAntiParticle ) {
      HepMC::FourVector ap(-px,-py,-pz,energy) ;
      int APartID = -PartID ;
      if ( PartID == 22 || PartID == 23 ) {
        APartID = PartID ;
      }
      HepMC::GenParticle * APart = new HepMC::GenParticle(ap,APartID,1);
      APart->suggest_barcode( barcode ) ;
      barcode++ ;
      Vtx->add_particle_out(APart) ;
    }
  }

  fEvt->add_vertex(Vtx) ;
  fEvt->set_event_number(e.id().event()) ;
  fEvt->set_signal_process_id(20) ;

  if ( fVerbosity > 0 ) {
    fEvt->print();
  }

  auto_ptr<HepMCProduct> BProduct(new HepMCProduct()) ;
  BProduct->addHepMCData( fEvt );
  e.put(BProduct);

  auto_ptr<GenEventInfoProduct> genEventInfo(new GenEventInfoProduct(fEvt));
  e.put(genEventInfo);
    
  if ( fVerbosity > 0 ) {
    // for testing purpose only
    // fEvt->print() ; // prints empty info after it's made into edm::Event
    cout << " FlatRandomPtAndD0GunProducer : Event Generation Done " << endl;
  }
}
//#include "FWCore/Framework/interface/MakerMacros.h"
//DEFINE_FWK_MODULE(FlatRandomPtAndD0GunProducer);
