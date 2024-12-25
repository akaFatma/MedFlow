import { Routes } from '@angular/router';
import { LoginPageComponent } from './pages/login-page/login-page.component';
import { AddDPIComponent } from './pages/add-dpi/add-dpi.component';
import { MedicalHistoryComponent } from './components/medical-history/medical-history.component';
import { PersonalInfoCardComponent } from './components/personal-info-card/personal-info-card.component';
import { BienvenuComponentComponent } from './components/bienvenu-component/bienvenu-component.component';

export const routes: Routes = [
  { path: 'users/login', component: LoginPageComponent },
  { path: 'add-dpi', component: AddDPIComponent },
  { path: 'ConsulterDPI', component: MedicalHistoryComponent },
  { path: 'ConsulterPersonalInfo', component: PersonalInfoCardComponent },
  { path: 'bienvenue', component: BienvenuComponentComponent },

];
