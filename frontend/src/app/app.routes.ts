import { Routes } from '@angular/router';
import { LoginPageComponent } from './pages/login-page/login-page.component';

export const routes: Routes = [
    { path: 'users/login', component: LoginPageComponent },
    { path: 'test', component: LoginPageComponent }
];
