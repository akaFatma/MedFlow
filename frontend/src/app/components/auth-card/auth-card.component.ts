import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators ,ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
//import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './auth-card.component.html',
  styleUrls: ['./auth-card.component.scss'],
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule] ,
})
export class LoginComponent {
  loginForm!: FormGroup;

 /* constructor(private fb: FormBuilder, private authService: AuthService) {
    this.createForm();
  }*/
  constructor(private fb: FormBuilder) {
    this.createForm();
  }

  createForm() {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],  // Initialize with form controls
      password: ['', Validators.required]
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      const { username, password } = this.loginForm.value;
      console.log("fffffff");

      /*this.authService.login(username, password).subscribe(
        response => {
          console.log('Login successful', response);
          // Handle successful login, e.g., redirect to another page
        },
        error => {
          console.error('Login failed', error);
          // Handle login failure, show an error message
        }
      );*/
    }
  }
}
