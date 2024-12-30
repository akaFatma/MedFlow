import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { Output , EventEmitter } from '@angular/core';

@Component({
  selector: 'app-bilan',
  imports : [CommonModule,ReactiveFormsModule,FormsModule],
  templateUrl: './bilan.component.html',
  styleUrls: ['./bilan.component.scss']
})
export class BilanComponent {
  @Output() formSubmit = new EventEmitter<any>();
  bilans: string[] = [''];  // Start with one empty input
  isConfirmed: boolean = false;

  trackByIndex(index: number): number {
    return index;
  }

  addBilan(index: number): void {
    if (index === this.bilans.length - 1) {  // Only add new line if we're at the last input
      this.bilans.push('');  // Add new empty input
    }
  }

  confirmBilans(): void {
    this.isConfirmed = true;
  }
  
  submitBilan(): void {
    this.formSubmit.emit({ bilans: this.bilans });
  }
}