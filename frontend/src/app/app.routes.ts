// import { Routes } from '@angular/router';
// import { LoginPageComponent } from './pages/login-page/login-page.component';
// import { AddDPIComponent } from './pages/add-dpi/add-dpi.component';

// export const routes: Routes = [
//   { path: 'users/login', component: LoginPageComponent },
//   { path: 'add-dpi', component: AddDPIComponent },
//   { path: '', redirectTo: 'users/login', pathMatch: 'full' },
// ];

import { Routes } from '@angular/router';
import { LoginPageComponent } from './pages/login-page/login-page.component';
import { AddDPIComponent } from './pages/add-dpi/add-dpi.component';
import { ConsultPatientComponent } from './pages/consult-patient/consult-patient.component';

export const routes: Routes = [
  { path: '', component: ConsultPatientComponent },
  { path: 'add-dpi', component: AddDPIComponent },
  { path: 'users/login', component: LoginPageComponent },
  { path: 'consult-patient', component: ConsultPatientComponent },
  { path: '**', redirectTo: '' },
];
