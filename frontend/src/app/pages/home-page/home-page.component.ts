import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-home-page',
  standalone: true, // Needed if you are using `imports` for standalone components
  imports: [CommonModule, RouterModule], // Add `RouterModule` if you're using routerLink in the template
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss'] // Corrected `styleUrl` to `styleUrls` (plural)
})
export class HomePageComponent {
  titre = 'Bienvenue sur MedFlow';
  sousTitre = 'Gestion du Dossier Patient Informatisé (DPI)';
}
