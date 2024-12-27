import { Routes } from '@angular/router';
import { RoleGuard } from './services/role-guard';
import { MedecinLandingPageComponent } from './pages/medecin-landing-page/medecin-landing-page.component';
import { UnauthorizedPageComponent } from './pages/unauthorized-page/unauthorized-page.component';
import { LoginPageComponent } from './pages/login-page/login-page.component';

export const routes: Routes = [
  { 
    path: 'medecin-landing', 
    component: MedecinLandingPageComponent, 
    canActivate: [RoleGuard], 
    data: { role: 'Médecin' }
  },
  { 
    path: 'unauthorized', 
    component: UnauthorizedPageComponent 
  },
  { 
    path: 'login', 
    component: LoginPageComponent 
  },
  { 
    path: '', 
    redirectTo: 'login', 
    pathMatch: 'full'
  },
  { 
    path: '**', 
    redirectTo: 'login'
  }
];
