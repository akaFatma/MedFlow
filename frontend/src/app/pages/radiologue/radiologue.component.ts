
import { RadioTableComponent } from '../../components/radio-table/radio-table.component';
import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-radiologue',
  imports: [ RadioTableComponent], // Updated to radio-table
  templateUrl: './radiologue.component.html',
  styleUrls: ['./radiologue.component.scss'],
})
export class RadiologueComponent {
  constructor(private router: Router) {}

  goToHomePage() {
    if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
      this.router.navigate(['/HomePage']);
    }
  }
}
