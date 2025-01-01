import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-consult-patient',
  templateUrl: './consult-patient.component.html',
  styleUrls: ['./consult-patient.component.scss'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
})
export class ConsultPatientComponent {
  // Your component logic here
}
