import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-resume',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './resume.component.html',
  styleUrls: ['./resume.component.scss']
})
export class ResumeComponent {
  @Input() parentForm!: FormGroup;
  isConfirmed = false;

  confirmResume(): void {
    const resumeControl = this.parentForm.get('resume');
    this.isConfirmed = true;
  }
}