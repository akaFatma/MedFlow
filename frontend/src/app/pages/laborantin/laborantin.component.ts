import { Component } from '@angular/core';
import { HeaderComponent } from '../../components/header/header.component';
import { LaboTableComponent } from '../../components/labo-table/labo-table.component';
import { Router } from '@angular/router';

@Component({
  selector: 'app-laborantin',
  standalone: true,
  imports: [HeaderComponent, LaboTableComponent],
  templateUrl: './laborantin.component.html',
  styleUrls: ['./laborantin.component.scss'],
})
export class LaborantinComponent {
  constructor(private router: Router) {}

  goToHomePage() {
    if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
      this.router.navigate(['/HomePage']);
    }
}
}
