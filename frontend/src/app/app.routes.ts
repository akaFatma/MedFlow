import {AddDPIComponent} from './pages/add-dpi/add-dpi.component';
import { Routes } from '@angular/router';
import { RoleGuard } from './services/role.guard';
import { MedecinLandingPageComponent } from './pages/medecin-landing-page/medecin-landing-page.component';
import { UnauthorizedPageComponent } from './pages/unauthorized-page/unauthorized-page.component';
import { LoginPageComponent } from './pages/login-page/login-page.component';
import {ConsulterDPIPovPatientComponent} from './pages/consulter-dpipov-patient/consulter-dpipov-patient.component';

export const routes: Routes = [
  { path: '', redirectTo: 'add-dpi', pathMatch: 'full' },
  { path: 'users/login', component: LoginPageComponent },
  { path: 'add-dpi', component: AddDPIComponent },
  { path: 'test', component: ConsulterDPIPovPatientComponent },
  { path: '**', redirectTo: 'add-dpi' },
];
