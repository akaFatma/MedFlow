import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-bilan',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule],
  templateUrl: './bilan.component.html',
  styleUrls: ['./bilan.component.scss']
})
export class BilanComponent implements OnInit {
  @Output() formSubmit = new EventEmitter<any>();
  bilansForm!: FormGroup;  // Reactive form to hold bilans
  isConfirmed: boolean = false;

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    // Initialize the form with one empty "bilan"
    this.bilansForm = this.fb.group({
      bilans: this.fb.array([this.fb.group({
        bilan: ['', Validators.required]
      })]) // Start with one empty input
    });
  }

  // Getter to access the FormArray controls
  get bilansControls() : FormArray {
    return this.bilansForm.get('bilans') as FormArray;
  }

  // Method to add a new "bilan" input field
  addBilan(index: number): void {
    if (index === this.bilansControls.length - 1) {
      const bilansArray = this.bilansForm.get('bilans') as FormArray;
      bilansArray.push(this.fb.group({
        bilan: ['', Validators.required]
      }));  // Add a new empty control
    }
  }

  // Submit the form when the "Confirmer" button is clicked
  confirmBilans(): void {
    if (this.bilansForm.valid && !this.isConfirmed) {
      this.isConfirmed = true;
      this.formSubmit.emit(this.bilansForm.value.bilans);  // Emit the bilans array
    }
  }
}
