import { Routes } from '@angular/router';
import { RoleGuard } from './services/role.guard';
import { MedecinLandingPageComponent } from './pages/medecin-landing-page/medecin-landing-page.component';
import { UnauthorizedPageComponent } from './pages/unauthorized-page/unauthorized-page.component';
import { LoginComponent } from './components/auth-card/auth-card.component';

export const routes: Routes = [
   { path: 'medecin-landing', component: MedecinLandingPageComponent, canActivate: [RoleGuard], data: { role: 'Médecin' }},
   { path: 'unauthorized', component: UnauthorizedPageComponent },
   { path: 'login', component: LoginComponent },
   { path: '', redirectTo: '/login' } ,
   
];
