import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

interface MedicationEntry {
  medication: string;
  dose: string;
  instructions: string;
}

@Component({
  selector: 'app-ordonnance',
  imports : [FormsModule , CommonModule],
  templateUrl: './ordonnance.component.html',
  styleUrls: ['./ordonnance.component.scss']
})
export class OrdonnanceComponent {
  medicationEntries: MedicationEntry[] = [
    { medication: '', dose: '', instructions: '' }
  ];
  isConfirmed: boolean = false;

  addNewLine() {
    if (!this.isConfirmed) {
      this.medicationEntries.push({
        medication: '',
        dose: '',
        instructions: ''
      });
    }
  }
  confirmPrescription() {
    this.isConfirmed = true; // This will hide the button by updating the *ngIf directive
  }

}