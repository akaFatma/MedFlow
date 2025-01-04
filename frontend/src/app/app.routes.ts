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
import { LaborantinComponent } from './pages/laborantin/laborantin.component';  // Import Laborantin component
import { SaisieBilanComponent } from './components/saisie-bilan/saisie-bilan.component';
import { GrapheComponent } from './components/graphe/graphe.component';

export const routes: Routes = [
  { path: '', redirectTo: 'laborantin', pathMatch: 'full' },  // Redirect root path to Laborantin
  { path: 'login', component: LoginPageComponent },
  { path: 'unauthorized', component: UnauthorizedPageComponent },
  { path: 'graph', component: GrapheComponent },
  {
    path: 'medecin-landing',
    component: MedecinLandingPageComponent,
    data: { role: 'Médecin' },
  },
  {
    path: 'dossier-patient/:nss',
    component: ConsulterDPIPovPatientComponent,
    data: { roles: ['Médecin', 'Patient'] },
  },
  { path: 'add-dpi', component: AddDPIComponent, canActivate: [RoleGuard], data: { roles: ['Médecin', 'Administratif'] } },
  { path: 'soins', component: InfermierLandingPageComponent, canActivate: [RoleGuard], data: { roles: ['Infirmier'] } },
  
  // Laborantin route
  { path: 'laborantin', component: LaborantinComponent, data: { role: 'Laborantin' } },
  { path: 'saisie-bilan', component: SaisieBilanComponent }, // Add this route
  // Redirect all invalid paths to Laborantin
  { path: '**', redirectTo: 'laborantin', pathMatch: 'full' },
];
