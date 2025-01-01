import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup } from '@angular/forms';
import { Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-resume',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './resume.component.html',
  styleUrls: ['./resume.component.scss']
})
export class ResumeComponent implements OnInit {
  @Output() formSubmit = new EventEmitter<string>();  
  resumeForm!: FormGroup;
  isConfirmed: boolean = false;

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    // Initialize form with one text input for resume text
    this.resumeForm = this.fb.group({
      resumeText: [''] // The resume text control
    });
  }

  // Method to confirm and disable the form after submission
  confirmResume(): void {
    if (this.resumeForm.get('resumeText')?.value.trim()) {
      this.isConfirmed = true;
    }
  }

  // Method to submit the resume form
  submitResume(): void {
    if (this.resumeForm.get('resumeText')?.value.trim()) {
      this.formSubmit.emit(this.resumeForm.get('resumeText')?.value);  // Emit the resume text value
    }
  }
}
