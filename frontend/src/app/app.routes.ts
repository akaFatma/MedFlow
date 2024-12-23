// import { Routes } from '@angular/router';
// import { LoginPageComponent } from './pages/login-page/login-page.component';
// import {AddDPIComponent} from './pages/add-dpi/add-dpi.component';
// export const routes: Routes = [
//     { path: 'users/login', component: LoginPageComponent },
//     { path: 'test', component: LoginPageComponent },
//     { path: 'add-dpi', component: AddDPIComponent }
// ];

import { Routes } from '@angular/router';
import { LoginPageComponent } from './pages/login-page/login-page.component';
import { AddDPIComponent } from './pages/add-dpi/add-dpi.component';

export const routes: Routes = [
  { path: '', redirectTo: 'add-dpi', pathMatch: 'full' },
  { path: 'users/login', component: LoginPageComponent },
  { path: 'add-dpi', component: AddDPIComponent },
  { path: '**', redirectTo: 'add-dpi' },
];
