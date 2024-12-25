import { Routes } from '@angular/router';
import { ConsulterDPIPovPatientComponent } from './pages/consulter-dpipov-patient/consulter-dpipov-patient.component';
import { SideBarComponent } from './components/side-bar/side-bar.component';
import { MedecinTableComponent } from './components/medecin-table/medecin-table.component';


export const routes: Routes = [
  { path: 'test', component: ConsulterDPIPovPatientComponent },
  { path: 'testt', component: SideBarComponent},
  {path: 'testtt', component: MedecinTableComponent},

];
