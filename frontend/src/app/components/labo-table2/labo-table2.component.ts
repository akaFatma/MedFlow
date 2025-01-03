import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
interface Bilan {
  nom: string;
  prenom: string;
  date: string;
  id: string;
  etat: 'fait' | 'en attente';
}

@Component({
  selector: 'app-labo-table2',
  imports: [CommonModule],
  templateUrl: './labo-table2.component.html',
  styleUrl: './labo-table2.component.scss'
})
export class LaboTable2Component {

 bilans: Bilan[] = [
    { nom: 'Salhi', prenom: 'Fatma', date: '24/12/2024', id: '110720004', etat: 'fait' },
    { nom: 'Salhi', prenom: 'Fatma', date: '24/12/2024', id: '110720005', etat: 'en attente' },
    { nom: 'Salhi', prenom: 'Fatma', date: '24/12/2024', id: '110720006', etat: 'fait' },
    { nom: 'Salhi', prenom: 'Fatma', date: '24/12/2024', id: '110720007', etat: 'en attente' },
  ];

  constructor(private router: Router) {}

  // Navigate to 'SaisieBilan1Component' with a new 'bilanId' as a query parameter
  onCompleterBilan(bilanId: string): void {
    // Here, you can modify the `id` if necessary before passing it
    const newBilanId = `Bilan-${bilanId}`;  // Example of modifying the ID

    // Navigate to the new route with the updated query parameter
    this.router.navigate(['/saisie-bilan'], { queryParams: { id: newBilanId } });
  }
}
