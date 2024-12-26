import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { InfermierService } from '../../services/infermier.service';


interface patient {
 nom :string;
 prenom :string;
 nss: number;
}

@Component({
  selector: 'app-infermier-table',
  imports: [CommonModule],
  templateUrl: './infermier-table.component.html',
  styleUrl: './infermier-table.component.scss'
})
/*export class InfermierTableComponent {

  patients: patient[] = [];
  errorMessage: string = '';

  constructor(private infermierService: InfermierService) {}

  ngOnInit(): void {
    this.loadTable();
  }

  loadTable(): void {
    this.infermierService.getTable().subscribe({
      next: (data) => {
        this.patients = data;
      },
      error: (error) => {
        this.errorMessage = error.message;
        console.error('Error fetching consultations:', error);
      }
    });
  }











}*/
export class InfermierTableComponent {
  patient: patient[] = [
    { nom: 'Falak', prenom: 'Salhi', nss: 123456789 },
    { nom: 'Nassim', prenom: 'fellah', nss: 987654321 },
    { nom: 'Sofiane', prenom: 'Bouzidi', nss: 123456789 }
    
  ];
}
