import { Component, OnInit } from '@angular/core';
import {FormBuilder , FormGroup , Validators } from '@angular/forms'

@Component({
  selector: 'app-auth-card',
  templateUrl: './auth-card.component.html',
  styleUrl: './auth-card.component.scss'
})
export class AuthCardComponent implements OnInit {

  loginForm !: FormGroup;    

  constructor(private fb : FormBuilder){}

  ngOnInit(): void {
      this.loginForm=this.fb.group({
        username : ['',[Validators.required]], // Username is required
        password : ['',[Validators.required,Validators.minLength(8)]],  // Password is required with min length of 8
      });
  }
  onSubmit():void{
    if (this.loginForm.valid){
      console.log(this.loginForm.value);
    }
  }


}
