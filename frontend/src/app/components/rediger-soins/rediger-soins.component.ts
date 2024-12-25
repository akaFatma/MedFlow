import { Component} from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { OnSameUrlNavigation, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

interface SoinsData {
  etatPatient: string;
  medicaments: string;
  autres: string;
}

@Component({
  selector: 'app-rediger-soins',
  imports: [ReactiveFormsModule , CommonModule],
  templateUrl: './rediger-soins.component.html',
  styleUrl: './rediger-soins.component.scss'
})
export class RedigerSoinsComponent  {

  soinsForm: FormGroup;
  isSubmitting = false;

  constructor (
    private  fb : FormBuilder,
    private http  :  HttpClient,
    private router : Router
  ){
    this.soinsForm = this.fb.group({
      etatPatient: ['', Validators.required],
      medicaments: ['', Validators.required],
      autres: ['', Validators.required]
    });
  }
  onSubmit(): void {
    if (this.soinsForm.valid && !this.isSubmitting) {
      this.isSubmitting = true;

      const soinsData: SoinsData = {
        etatPatient: this.soinsForm.get('etatPatient')?.value,
        medicaments: this.soinsForm.get('medicaments')?.value,
        autres: this.soinsForm.get('autres')?.value
      };

      
      this.http.post<any>('/api/soins', soinsData) //replace bel endpoints
        .subscribe({
          next: (response) => {
            console.log('Soins submitted successfully:', response);
            this.router.navigate(['/previous-page']);
          },
          error: (error) => {
            console.error('Error submitting soins:', error);
            this.isSubmitting = false;
            alert('Une erreur est survenue. Veuillez réessayer.');
          },
          complete: () => {
            this.isSubmitting = false;
          }
        });
    }
  }

  onRetour(): void {
    this.router.navigate(['/previous-page']);
  }

  //check if a field is invalid
  isFieldInvalid(fieldName: string): boolean {
    const field = this.soinsForm.get(fieldName);
    return field ? (field.invalid && (field.dirty || field.touched)) : false;
  }
  

}




