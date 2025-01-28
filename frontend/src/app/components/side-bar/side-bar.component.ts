import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-side-bar',
  standalone: true,  
  imports: [RouterLinkActive],
  templateUrl: './side-bar.component.html',
  styleUrls: ['./side-bar.component.scss']
})
export class SideBarComponent {

  constructor(private router: Router) {}

  navigateTo(route: string) {
    this.router.navigate([route]);
  }
  goToHomePage() {
    if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
      this.router.navigate(['/HomePage']);
    }
  }
}


