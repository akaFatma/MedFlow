import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Output , EventEmitter } from '@angular/core';

@Component({
  selector: 'app-ordonnance',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './ordonnance.component.html',
  styleUrls: ['./ordonnance.component.scss'],
})
export class OrdonnanceComponent {
  @Output() formSubmit = new EventEmitter<any>(); 
  ordonnanceForm: FormGroup;
  isConfirmed: boolean = false; // Flag to control button visibility and form behavior

  constructor(private fb: FormBuilder) {
    this.ordonnanceForm = this.fb.group({
      date: ['', Validators.required],
      lastName: ['', Validators.required],
      firstName: ['', Validators.required],
      age: ['', [Validators.required, Validators.min(0)]],
      medications: this.fb.array([
        this.createMedicationEntry()
      ])
    });
  }

  // Get the medications FormArray
  get medications(): FormArray {
    return this.ordonnanceForm.get('medications') as FormArray;
  }

  // Create a single medication FormGroup
  createMedicationEntry(): FormGroup {
    return this.fb.group({
      medication: ['', Validators.required],
      dose: ['', Validators.required],
      instructions: ['', Validators.required],
    });
  }

  get medicationControls() {
    return this.ordonnanceForm.get('medications') as FormArray;
  }

  // Add a new medication line
  addNewLine(): void {
    if (!this.isConfirmed) {
      this.medications.push(this.createMedicationEntry());
    }
  }

  // Confirm the prescription
  confirmPrescription(): void {
    this.isConfirmed = true; //disable inputs and hide buttons
    this.ordonnanceForm.disable();
  }
  onSubmit(): void {
    if (this.ordonnanceForm.valid) {
      this.formSubmit.emit(this.ordonnanceForm.value);
    }
  }

}
