import {AddDPIComponent} from './pages/add-dpi/add-dpi.component';
import { Routes } from '@angular/router';
import { LoginPageComponent } from './pages/login-page/login-page.component';
import {ConsulterDPIPovPatientComponent} from './pages/consulter-dpipov-patient/consulter-dpipov-patient.component';

export const routes: Routes = [
  { path: 'login', component: LoginPageComponent },
  { path: 'add-dpi', component: AddDPIComponent },
  { path: 'test', component: ConsulterDPIPovPatientComponent },
  { path: '**', redirectTo: 'test' },
  { path: '', redirectTo: 'login', pathMatch: 'full' },
];
