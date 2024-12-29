import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { InfermierService } from '../../services/infermier.service';
import { Output , EventEmitter , Input } from '@angular/core';
import { SimpleChanges } from '@angular/core';
import { PatientService } from '../../services/patient.services';

 interface patient{
  nom : string,
  prenom : string,
  nss : number
}

@Component({
  selector: 'app-infermier-table',
  imports: [CommonModule],
  templateUrl: './infermier-table.component.html',
  styleUrl: './infermier-table.component.scss'
})
export class InfermierTableComponent {

  @Output() openSoins = new EventEmitter<patient>();  
   errorMessage: string = '';
  @Input() searchResults: patient[] = [];
  displayedPatients: patient[] = [];

  constructor(private patientservice : PatientService) {}
  


   ngOnInit(): void {
      this.loadPatients();
    }
  
    ngOnChanges(changes: SimpleChanges): void {
      if (changes['searchResults']) {
        const currentValue = changes['searchResults'].currentValue;
        if (currentValue && currentValue.length > 0) {
          this.displayedPatients = currentValue;
        } else {
          //load all patients if we don't have search results
          this.loadPatients();
        }
      }
    }

    loadPatients(): void {
      // Replace service call with mock data for testing
      this.displayedPatients = [
        { nom: 'John', prenom: 'Doe', nss: 123456789 },
        { nom: 'Jane', prenom: 'Smith', nss: 987654321 },
        { nom: 'Alice', prenom: 'Johnson', nss: 111222333 },
        { nom: 'Bob', prenom: 'Williams', nss: 444555666 },
        { nom: 'Charlie', prenom: 'Brown', nss: 777888999 }
      ];
    }
    
  
     /*loadPatients(): void {
      this.patientservice.getConsultationHistory().subscribe({
        next: (data) => {
          this.displayedPatients = data;
        },
        error: (error) => {
          this.errorMessage = error.message;
          console.error('Error fetching patients:', error);
        }
      });
    }*/

  openRedigerSoins(patient: patient): void {
    this.openSoins.emit(patient);
  }
}
