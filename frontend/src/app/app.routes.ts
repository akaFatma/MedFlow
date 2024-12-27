import { Routes } from '@angular/router';
import { RoleGuard } from './services/role.guard';
import { MedecinLandingPageComponent } from './pages/medecin-landing-page/medecin-landing-page.component';
import { UnauthorizedPageComponent } from './pages/unauthorized-page/unauthorized-page.component';

export const routes: Routes = [
  { path: 'LandingPage', component : MedecinLandingPageComponent },
  { path: 'medecin-landing', component: MedecinLandingPageComponent, canActivate: [RoleGuard], data: { role: 'medecin' }},
  { path: 'unauthorized', component: UnauthorizedPageComponent },
  { path: '**', redirectTo: '/login' } 
];
