import { Routes } from '@angular/router';
import { RoleGuard } from './services/role.guard';
import { LoginPageComponent } from './pages/login-page/login-page.component';
import { UnauthorizedPageComponent } from './pages/unauthorized-page/unauthorized-page.component';
import { MedecinLandingPageComponent } from './pages/medecin-landing-page/medecin-landing-page.component';
import { ConsulterDPIPovPatientComponent } from './pages/consulter-dpipov-patient/consulter-dpipov-patient.component';
import { OrdonnanceComponent } from './components/ordonnance/ordonnance.component';
import { BilanComponent } from './components/bilan/bilan.component';
import { ResumeComponent } from './components/resume/resume.component';
import { NouvelleConsultationComponent } from './pages/nouvelle-consultation/nouvelle-consultation.component';
import { InfermierTableComponent } from './components/infermier-table/infermier-table.component';
import { InfermierLandingPageComponent } from './pages/infermier-landing-page/infermier-landing-page.component';
import {AddDPIComponent} from './pages/add-dpi/add-dpi.component';
import { ConsultPatientComponent } from './pages/consult-patient/consult-patient.component';

 
export const routes: Routes = [
   { path: 'login', component: LoginPageComponent },
   { path: 'unauthorized', component: UnauthorizedPageComponent },
   { 
     path: 'medecin-landing', 
     component: MedecinLandingPageComponent, 
     canActivate: [RoleGuard], 
     data: { role: 'Médecin' }
   },
   { 
     path: 'dossier-patient/:nss', 
     component: ConsulterDPIPovPatientComponent,
     canActivate: [RoleGuard],
     data: { roles: ['Médecin', 'Patient'] }
   },
   { 
    path: 'add-dpi', 
    component: AddDPIComponent,
    canActivate: [RoleGuard],
    data: { roles: ['Médecin', 'Administratif'] }
  },
  {
    path : 'new-consultation' ,
    component : NouvelleConsultationComponent,
    canActivate: [RoleGuard],
    data: { roles: ['Médecin'] }
    },
  { 
    path: 'soins', 
    component: InfermierLandingPageComponent,
    canActivate: [RoleGuard],
    data: { roles: ["Infirmier"] }
  },
   { path: 'consult-patient', 
    component: ConsultPatientComponent, 
    canActivate: [RoleGuard],
    data: { roles: ['Médecin', 'Patient'] }
    },
  
   { path: '**', redirectTo: 'login', pathMatch: 'full' }
  
 ];

