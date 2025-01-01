
import { Component } from '@angular/core';
import { SidebarComponent } from '../../components/sidebar/sidebar.component';
import { HeaderComponent } from '../../components/header/header.component';
import { PatientTableComponent } from '../../components/patient-table/patient-table.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faQrcode, faMagnifyingGlass } from '@fortawesome/free-solid-svg-icons';
import { CommonModule } from '@angular/common'; // Import CommonModule

@Component({
  selector: 'app-medecin-landing-page',
  standalone: true,
  imports: [
    SidebarComponent,
    HeaderComponent,
    PatientTableComponent,
    FontAwesomeModule,
    CommonModule, // Add CommonModule here to enable *ngIf
  ],
  templateUrl: './medecin-landing-page.component.html',
  styleUrls: ['./medecin-landing-page.component.scss'],
})
export class MedecinLandingPageComponent {
  faQrcode = faQrcode;
  faMagnifyingGlass = faMagnifyingGlass;

  // Flag to control the visibility of the QR notification modal
  showNotification = false;

  // Show the notification modal when the QR button is clicked
  openQrNotification(): void {
    this.showNotification = true;
  }

  // Close the notification modal
  closeQrNotification(): void {
    this.showNotification = false;
  }
}


