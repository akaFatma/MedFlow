import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgFor } from '@angular/common';

interface Consultation {
  
  date : string ;
  doctor : string ;
  specialty : string ;

}



@Component({
  selector: 'app-medical-history',
  imports: [CommonModule,NgFor],
  templateUrl: './medical-history.component.html',
  styleUrl: './medical-history.component.scss'
})
export class MedicalHistoryComponent {
  consultations: Consultation[] = [
    { date: '2024-12-20', doctor: 'Dr. TOUAT', specialty: 'Cardiologue' },
    { date: '2024-12-10', doctor: 'Dr. SENNANE', specialty: 'Dermatologue' },
    { date: '2024-12-05', doctor: 'Dr. FELKIR', specialty: 'Neurologue' }
  ];
}
