import { Component } from '@angular/core'; // Import Component decorator
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome'; // Import FontAwesomeModule
import { faHome, faUserGear } from '@fortawesome/free-solid-svg-icons'; // Import the icons

@Component({
  selector: 'app-sidebar', // Component selector
  standalone: true, // Declare as a standalone component
  imports: [FontAwesomeModule], // Import FontAwesomeModule for icons
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss'],
})
export class SidebarComponent {
  // Define FontAwesome icons for the menu
  faHome = faHome; // Dashboard icon
  faUserGear = faUserGear; // Gestion des patients icon
}

