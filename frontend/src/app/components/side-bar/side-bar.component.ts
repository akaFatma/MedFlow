import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-side-bar',
  standalone: true,  // Optional: Use if using Angular 14+ standalone components
  imports: [RouterLinkActive],
  templateUrl: './side-bar.component.html',
  styleUrls: ['./side-bar.component.scss'] // Fixed to 'styleUrls' (plural)
})
export class SideBarComponent {

  constructor(private router: Router) {}

  navigateTo(route: string) {
    this.router.navigate([route]);
  }
}
