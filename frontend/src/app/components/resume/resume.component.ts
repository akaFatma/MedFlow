import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Output , EventEmitter } from '@angular/core';

@Component({
  selector: 'app-resume',
  imports : [FormsModule,CommonModule],
  templateUrl: './resume.component.html',
  styleUrls: ['./resume.component.scss']
})
export class ResumeComponent {
  @Output() formSubmit = new EventEmitter<string>();  
  resumeText: string = '';
  isConfirmed: boolean = false;

  confirmResume(): void {
    if (this.resumeText.trim()) {
      this.isConfirmed = true;
    }
  }
  submitResume(): void {
    if (this.resumeText.trim()) {
      this.formSubmit.emit(this.resumeText);
    }
  }
}