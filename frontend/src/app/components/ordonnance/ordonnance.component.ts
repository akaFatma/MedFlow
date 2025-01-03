import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormArray, FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MedecinService } from '../../services/medecin.service';
@Component({
  selector: 'app-ordonnance',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './ordonnance.component.html',
  styleUrls: ['./ordonnance.component.scss']
})
export class OrdonnanceComponent implements OnInit {
  @Input() parentForm!: FormGroup;
  isConfirmed = false;
  medecin: {first_name: string; last_name: string; specialite: string } = {first_name: '', last_name: '', specialite: '' };
  error: string | null = null;
  constructor(private fb: FormBuilder, private medecinService : MedecinService) {
    
  }

  ngOnInit() {
    this.medecin = { first_name: 'John', last_name: 'Doe', specialite: 'Cardiologist' };
    const username = localStorage.getItem('user_name');
    console.log(username)
    if (!username) {
      this.error = 'No username found in local storage';
      return;
    }
    console.log(username)
    this.medecinService.getMedecinInfo(username).subscribe({
      next: (data) => {
        console.log(data)
        this.medecin = data;
      },
      error: (err) => {
        console.error('Error:', err);
        this.error = err.message || 'An error occurred while fetching Medecin info';
      },
    });
    // Add initial medication line if needed
    if (this.medications.length === 0) {
      this.addNewLine();
    }
  }

  get ordonnanceForm(): FormGroup {
    return this.parentForm.get('ordonnance') as FormGroup;
  }

  get medications(): FormArray {
    return this.ordonnanceForm.get('medications') as FormArray;
  }

  createMedicationEntry(): FormGroup {
    return this.fb.group({
      medication: ['', Validators.required],
      dose: ['', Validators.required],
      instructions: ['', Validators.required],
    });
  }

  addNewLine(): void {
    if (!this.isConfirmed) {
      this.medications.push(this.createMedicationEntry());
    }
  }

  confirmPrescription(): void {
    this.isConfirmed = true;
    // this.ordonnanceForm.disable();
  }
}