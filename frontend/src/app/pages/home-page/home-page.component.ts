import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-home-page',
  imports: [CommonModule],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.scss'
})
export class HomePageComponent {
  titre = 'Bienvenue sur MedFlow';
  sousTitre = 'Gestion du Dossier Patient Informatisé (DPI)';

  
}
