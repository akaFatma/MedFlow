import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { SideBarComponent } from '../../components/side-bar/side-bar.component';
import { BienvenuComponentComponent } from '../../components/bienvenu-component/bienvenu-component.component';
import { SearchBarComponent } from '../../components/search-bar/search-bar.component';
import { MedecinTableComponent } from '../../components/medecin-table/medecin-table.component';

@Component({
  selector: 'app-medecin-landing-page',
  imports: [
    CommonModule,
    SideBarComponent,
    BienvenuComponentComponent,
    SearchBarComponent,
    MedecinTableComponent
  ],
  templateUrl: './medecin-landing-page.component.html',
  styleUrl: './medecin-landing-page.component.scss'
})
export class MedecinLandingPageComponent {

  currentUser = 'Name'; //hna idk how to get the username
  searchTerm: number =0 ; 
 
  onSearch(value: number) {
    this.searchTerm = value;
  }
 
  onScanQR() {
   //hna idk 
  }
}
