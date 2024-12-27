import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators ,ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './auth-card.component.html',
  styleUrls: ['./auth-card.component.scss'],
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule] ,
})
export class LoginComponent {
  loginForm!: FormGroup;

    constructor(
          private fb: FormBuilder,
          private authService: AuthService,  
          private router: Router
        ) {
          this.loginForm = this.fb.group({
            username: ['', Validators.required],
            password: ['', Validators.required]
          });
        }
      
        onSubmit() {
          if (this.loginForm.valid) {
            const { username, password } = this.loginForm.value;
            this.authService.login(username, password).subscribe({
              next: (response) => {
                console.log('Connexion réussie', response);
                const redirectUrl = this.authService.getRedirectUrl(response.role);
                this.router.navigate([redirectUrl]);
              },
              error: (error) => {
                console.error('Échec de la connexion', error);
              }
            });
          } else {
            console.error('Formulaire non valide');
          }
        }
}


