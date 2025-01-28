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
import { AddDPIComponent } from './pages/add-dpi/add-dpi.component';
import { HomePageComponent } from './pages/home-page/home-page.component';
import { ConsultPatientComponent } from './pages/consult-patient/consult-patient.component';
import { LaborantinComponent } from './pages/laborantin/laborantin.component';
import { SaisieBilanComponent } from './components/saisie-bilan/saisie-bilan.component';
import { SaisieBilanRadioComponent } from './components/saisie-bilan-radio/saisie-bilan-radio.component';
import { RadiologueComponent } from './pages/radiologue/radiologue.component';
export const routes: Routes = [
   { path: 'HomePage', component: HomePageComponent},
   { path: 'login', component: LoginPageComponent},
   { path: 'unauthorized', component: UnauthorizedPageComponent },

   { 
     path: 'medecin-landing', 
     component: MedecinLandingPageComponent, 
     canActivate: [RoleGuard], 
     data: { roles: ['Médecin'] }
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
    path: 'new-consultation',
    component: NouvelleConsultationComponent,
    canActivate: [RoleGuard],
    data: { roles: ['Médecin'] }
    },

  { 
    path: 'soins', 
    component: InfermierLandingPageComponent,
    canActivate: [RoleGuard],
    data: { roles: ['Infirmier'] },
  },

   { path: 'consult-patient', 
    component: ConsultPatientComponent, 
    canActivate: [RoleGuard],
    data: { roles: ['Médecin', 'Patient'] }
    },

    { path: 'laborantin', 
      component: LaborantinComponent, 
      canActivate: [RoleGuard],
      data: { roles: ['Laborantin'] }
    },

    { path: 'saisie-bilan', 
      component: SaisieBilanComponent,
      canActivate: [RoleGuard],
      data: { roles: ['Laborantin'] } },

    { path: 'saisie-bilan-radio', 
      component: SaisieBilanRadioComponent,
      canActivate: [RoleGuard],
      data: { roles: ['Radiologue'] }  },
    
      { path: 'radiologue', 
        component: RadiologueComponent, 
        canActivate: [RoleGuard],
        data: { roles: ['Radiologue'] } 
       },  
  

     { path: '**', redirectTo: 'HomePage', pathMatch: 'full' },
  

];
