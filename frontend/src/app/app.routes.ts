import { Routes } from '@angular/router';
import { ConsulterDPIPovPatientComponent } from './pages/consulter-dpipov-patient/consulter-dpipov-patient.component';
import { SideBarComponent } from './components/side-bar/side-bar.component';


export const routes: Routes = [
  { path: 'test', component: ConsulterDPIPovPatientComponent },
  { path: 'testt', component: SideBarComponent},

];
