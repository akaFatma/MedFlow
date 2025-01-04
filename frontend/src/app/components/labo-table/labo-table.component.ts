import { Component } from '@angular/core';
import { CommonModule } from '@angular/common'; // Import CommonModule
import { Router } from '@angular/router';

interface Bilan {
  nom: string;
  prenom: string;
  date: string;
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
export class LaboTableComponent {
  bilans: Bilan[] = [
    { nom: 'Salhi', prenom: 'Fatma', date: '24/12/2024', id: '110720004', etat: 'fait' },
    { nom: 'Salhi', prenom: 'Fatma', date: '24/12/2024', id: '110720005', etat: 'en attente' },
    { nom: 'Salhi', prenom: 'Fatma', date: '24/12/2024', id: '110720006', etat: 'fait' },
    { nom: 'Salhi', prenom: 'Fatma', date: '24/12/2024', id: '110720007', etat: 'en attente' },
  ];

  constructor(private router: Router) {}

  onCompleterBilan(bilanId: string): void {
    this.router.navigate(['/saisie-bilan'], { queryParams: { id: bilanId } });
  }
}

