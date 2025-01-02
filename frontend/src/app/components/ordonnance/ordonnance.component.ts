import { Component, Input, OnInit } from '@angular/core';
import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormArray, FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';

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

  constructor(private fb: FormBuilder) {}

  ngOnInit() {
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