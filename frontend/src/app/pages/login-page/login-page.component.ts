import { Component } from '@angular/core';
import { LoginComponent } from '../../components/auth-card/auth-card.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login-page',
  standalone:true,
  imports: [LoginComponent,CommonModule],
  templateUrl: './login-page.component.html',
  styleUrl: './login-page.component.scss'
})
export class LoginPageComponent {

}
