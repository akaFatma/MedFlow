import { Routes } from '@angular/router';
import { LoginPageComponent } from './pages/login-page/login-page.component';
import { MedecinLandingPageComponent } from './pages/medecin-landing-page/medecin-landing-page.component';


export const routes: Routes = [
    { path: '', redirectTo: 'users/medecin', pathMatch: 'full' },
  { path: 'users/medecin', component: MedecinLandingPageComponent },
  { path: 'users/login', component: LoginPageComponent },
];
