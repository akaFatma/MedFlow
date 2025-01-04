import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common'; // Import CommonModule
import { Router } from '@angular/router';
import { LaborantinService } from '../../services/laborantin.service';

interface Bilan {
  nom: string;
  prenom: string;
  date: Date;
  id: string;
  etat: 'fait' | 'en attente';
}

@Component({
  selector: 'app-labo-table',
  standalone: true,
  imports: [CommonModule], // Include CommonModule here
  templateUrl: './labo-table.component.html',
  styleUrls: ['./labo-table.component.scss'],
})
export class LaboTableComponent  implements OnInit {
  errorMessage = '';
  bilans: any;

 constructor(private laborantinService: LaborantinService, private router: Router
  ) {}

  ngOnInit(): void {
    this.loadBilans();
  }

  loadBilans(): void {
    this.laborantinService.getBilans().subscribe({
      next: (data) => {
        this.bilans = data;
        console.log('Soins:', this.bilans);
      },
      error: (error) => {
        this.errorMessage = error.message;
        console.error('Error fetching Soins:', error);
      }
    });
  }
  onCompleterBilan(bilanId: string): void {
    this.router.navigate(['/saisie-bilan'], { queryParams: { id: bilanId } });
  }
}

