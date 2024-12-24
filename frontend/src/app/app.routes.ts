import { Routes } from '@angular/router';
import { LoginPageComponent } from './pages/login-page/login-page.component';
import { AddDPIComponent } from './pages/add-dpi/add-dpi.component';
import { MedicalHistoryComponent } from './components/medical-history/medical-history.component';

export const routes: Routes = [
  { path: 'users/login', component: LoginPageComponent },
  { path: 'add-dpi', component: AddDPIComponent },
  { path: 'ConsulterDPI', component: MedicalHistoryComponent },
];
