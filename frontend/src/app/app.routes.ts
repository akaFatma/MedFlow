import { Routes } from '@angular/router';
import { RoleGuard } from './services/role.guard';
import { LoginPageComponent } from './pages/login-page/login-page.component';
import { UnauthorizedPageComponent } from './pages/unauthorized-page/unauthorized-page.component';
import { MedecinLandingPageComponent } from './pages/medecin-landing-page/medecin-landing-page.component';
import { ConsulterDPIPovPatientComponent } from './pages/consulter-dpipov-patient/consulter-dpipov-patient.component';
import { OrdonnanceComponent } from './components/ordonnance/ordonnance.component';
import { BilanComponent } from './components/bilan/bilan.component';
import { ResumeComponent } from './components/resume/resume.component';


 
export const routes: Routes = [
  //  { path: 'login', component: LoginPageComponent },
  //  { path: 'unauthorized', component: UnauthorizedPageComponent },
  //  { 
  //    path: 'medecin-landing', 
  //    component: MedecinLandingPageComponent, 
  //    canActivate: [RoleGuard], 
  //    data: { role: 'Médecin' }
  //  },
  //  { 
  //    path: 'dossier-patient/:nss', 
  //    component: ConsulterDPIPovPatientComponent,
  //    canActivate: [RoleGuard],
  //    data: { roles: ['Médecin', 'Patient'] }
  //  },
  //  { path: '**', redirectTo: 'login', pathMatch: 'full' }
  {path : 'test' , component : ResumeComponent}
 ];
